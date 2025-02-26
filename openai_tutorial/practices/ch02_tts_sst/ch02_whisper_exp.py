from openai import OpenAI	

# API 키 입력
from get_key import get_openai_key

# API 키 입력
OPENAI_API_KEY = get_openai_key()
client = OpenAI(api_key=OPENAI_API_KEY)

# 녹음 파일 열기
audio_file = open("speech.mp3", "rb")

# whisper 모델에 음원 파일 넣기
transcript = client.audio.transcriptions.create(model="whisper-1", file=audio_file, response_format="text")

# 결과 보기
print(transcript)