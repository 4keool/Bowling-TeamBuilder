import json
import re
import os
import sys

def create_json_with_date(date_str):
    # 폴더 생성 (날짜 기준)
    directory = f"./{date_str}"
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"폴더 '{date_str}'가 생성되었습니다.")
    else:
        print(f"폴더 '{date_str}'가 이미 존재합니다.")

    # input.txt 파일 읽기
    with open('name_list.txt', 'r', encoding='utf-8') as file:
        content = file.read()

    # 정규식으로 JSON 내용만 추출
    pattern = r'{.*}'
    match = re.search(pattern, content, re.DOTALL)

    if match:
        json_str = match.group().replace('""', '"')  # 이중 큰따옴표 수정

        try:
            data = json.loads(json_str)  # JSON 변환
            
            # 원하는 형식으로 문자열 생성
            formatted_json = (
                "{\n"
                '    "fixed_assignments": {},\n'
                '    "players": [\n'
                + ",\n".join(
                    [
                        f'        {json.dumps(player, ensure_ascii=False)}'
                        for player in data["players"]
                    ]
                )
                + "\n    ]\n}"
            )

            # players.json 파일 저장
            output_path = os.path.join(directory, 'players.json')
            with open(output_path, 'w', encoding='utf-8') as file:
                file.write(formatted_json)
            
            print(f"'{output_path}' 파일이 생성되었습니다.")
        
        except json.JSONDecodeError as e:
            print(f"JSON 형식 오류: {e}")
    else:
        print("JSON 데이터를 찾을 수 없습니다.")

# 실행 부분
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("사용법: python3 a.py <날짜>")
        print("예시: python3 a.py 2025-02-09")
    else:
        date_str = sys.argv[1]
        create_json_with_date(date_str)
