from openai	import OpenAI
from get_key import get_openai_key

# API 키 입력
OPENAI_API_KEY = get_openai_key()
client = OpenAI(api_key=OPENAI_API_KEY)

# 생성할 파일명
speech_file_path = "speech.mp3"

with client.audio.speech.with_streaming_response.create(
    model="tts-1",
    voice="alloy",
    input="""오늘은 사람들이 좋아하는 것을 만들기에 좋은 날입니다!""",
) as response:
    response.stream_to_file("speech.mp3")