from fastapi import FastAPI, UploadFile, File, Form, BackgroundTasks, HTTPException
from fastapi.responses import JSONResponse, FileResponse
import os
import shutil
import uuid
import sys
from main import main as run_algorithm

app = FastAPI()

ALLOWED_USERS = {"jay", "jun", "seokhwan"}
JOBS = {}

@app.post("/run")
async def run_task(
    background_tasks: BackgroundTasks,
    json_file: UploadFile = File(...),
    repeat: int = Form(...),
    num_teams: int = Form(...),
    username: str = Form(...)
):
    if username not in ALLOWED_USERS:
        raise HTTPException(status_code=403, detail="허가된 사용자가 아닙니다.")

    job_id = str(uuid.uuid4())
    work_dir = f"./jobs/{job_id}"
    os.makedirs(work_dir, exist_ok=True)
    input_path = os.path.join(work_dir, "input.json")

    with open(input_path, "wb") as f:
        shutil.copyfileobj(json_file.file, f)

    JOBS[job_id] = {
        "status": "running",
        "input": input_path,
        "repeat": repeat,
        "num_teams": num_teams,
        "username": username,
        "result_json": None
    }

    background_tasks.add_task(execute_job, job_id)

    return {"job_id": job_id, "message": "작업이 시작되었습니다."}

@app.get("/status/{job_id}")
async def get_status(job_id: str):
    if job_id not in JOBS:
        raise HTTPException(status_code=404, detail="작업이 없습니다.")
    return {"status": JOBS[job_id]["status"]}

@app.get("/result/{job_id}")
async def get_result(job_id: str):
    job = JOBS.get(job_id)
    if not job or job["status"] != "completed":
        raise HTTPException(status_code=404, detail="결과를 찾을 수 없습니다.")
    return FileResponse(job["result_json"], filename="result.json")

def execute_job(job_id: str):
    job = JOBS[job_id]
    sys.argv = [
        "main.py",
        "--num_teams", str(job["num_teams"]),
        "--repeat", str(job["repeat"]),
        "--data_path", job["input"]
    ]
    try:
        run_algorithm()
        # 결과 파일 찾기
        result_path = os.path.join(os.path.dirname(job["input"]), "result.json")
        job["result_json"] = result_path
        job["status"] = "completed"
    except Exception as e:
        job["status"] = f"error: {str(e)}"
