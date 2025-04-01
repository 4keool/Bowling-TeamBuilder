FROM python:3.10-slim

RUN apt-get update && apt-get install -y fonts-nanum && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install fastapi uvicorn python-multipart

ENV MPLCONFIGDIR=/app/mplconfig

EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
