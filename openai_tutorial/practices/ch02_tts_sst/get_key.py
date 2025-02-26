import os
from pathlib import Path
from dotenv import load_dotenv

def get_openai_key():

    # 현재 파일 위치
    current_path = Path.cwd()
    
    # step10_LLM 디렉토리로 이동 (../../)
    project_root = current_path.parent.parent
    
    # .env 파일 경로
    env_path = project_root / '.env'
    
    # .env 파일이 존재하는지 확인
    if env_path.exists():
        load_dotenv(env_path)
        print(f"Loaded .env from: {env_path}")
    else:
        raise FileNotFoundError(f".env file not found at: {env_path}")
    
    # 실행
    try:
        # 환경 변수 사용
        api_key = os.environ.get('OPENAI_API_KEY')
        if api_key:
            print("API Key loaded successfully")
            # API 키 마스킹하여 출력
            masked_key = f"{api_key[:8]}...{api_key[-4:]}"
            print(f"API Key: {masked_key}")
        else:
            print("API Key not found in .env file")
    except Exception as e:
        print(f"Error loading .env file: {e}")

    return api_key

def get_openai_api_key():
    return "your-api-key-here"