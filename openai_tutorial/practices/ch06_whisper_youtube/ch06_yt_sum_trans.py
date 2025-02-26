##### 기본 정보 입력 ####
# Streamlit 패키기 추가
import streamlit as st

# OpenAI 패키지 추가
import openai

# 유튜브 영상을 다운로드하기 위한 pytube 패키지 추가
from pytubefix import YouTube

# 유튜브 영상을 번역, 요약하기 위한 Langchain 패키지 추가
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI

# 필요한 기본 패키지 추가
import re
import os
import shutil
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

    print("""Returned API Key: """, api_key)
    return api_key

# Whisper를 위해서 client 선언.
api_key = get_openai_key()
client = openai.OpenAI(
    api_key=api_key
)

##### 기능 구현 함수 #####
# 주소를 입력받으면 유튜브 동영상의 음성(mp3)을 추출하는 함수.
def get_audio(url):
    yt = YouTube(url)
    audio = yt.streams.filter(only_audio=True).first()
    audio_file = audio.download(output_path=".")
    base, ext = os.path.splitext(audio_file)
    new_audio_file = base + '.mp3'
    shutil.move(audio_file, new_audio_file)
    return new_audio_file

# 음성 파일 위치를 전달받으면 스크립트를 추출.
def get_transcribe(file_path):
    with open(file_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            response_format="text", # repsone_format을 text로 하면 자막이 아닌 텍스트로 반환.
            file=audio_file
        )
        return transcript

# 영어 입력이 들어오면 한글로 번역 및 불렛포인트 요약을 수행.
def trans(text):
    response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "당신은 영한 번역가이자 요약가입니다. 들어오는 모든 입력을 한국어로 번역하고 불렛 포인트 요약을 사용하여 답변하시오. 반드시 불렛 포인트 요약이어야만 합니다."},
                    {"role": "user", "content": text}
                ]
            )
    return response.choices[0].message.content

# 유튜브 주소의 형태를 정규 표현식(Regex)로 체크하는 함수. (선택적으로 사용하세요. 꼭 있어야 하는 건 아닙니다.)
def youtube_url_check(url):
    pattern = r'^https:\/\/www\.youtube\.com\/watch\?v=([a-zA-Z0-9_-]+)(\&ab_channel=[\w\d]+)?$'
    match = re.match(pattern, url)
    return match is not None

    st.set_page_config(page_title="YouTube Summarize", layout="wide")

##### 메인 함수 #####
def main():
    # session state 초기화
    if "summarize" not in st.session_state:
        st.session_state["summarize"] = ""

    # 메인공간
    st.header(" 📽️ YouTube Summarizer ")
    st.image('ai.png', width=200)
    youtube_video_url = st.text_input("Please write down the YouTube address. 🖋️",placeholder="https://www.youtube.com/watch?v=**********")
    st.markdown('---')

    # URL이 실제로 입력되었을 경우.
    if len(youtube_video_url) > 2:
        # URL을 잘못 입력했을 경우
        if not youtube_url_check(youtube_video_url):
            st.error("YouTube URL을 확인하세요.")
        # URL을 제대로 입력했을 경우
        else:
            # 동영상 재생 화면 물러오기
            width = 50
            side = width/2
            _, container, _ = st.columns([side, width, side])
            container.video(data=youtube_video_url)

            # 영상 속 자막 추출하기. part2.ch02_06_자동 자막 생성 서비스 참고!
            audio_file = get_audio(youtube_video_url)
            transcript = get_transcribe(audio_file)

            st.subheader("Summary Outcome (in English)")
            # 언어모델은 ChatGPT(GPT-3.5-Turbo)를 사용. 또는 gpt-4o를 사용하셔도 무방합니다.
            llm = ChatOpenAI(model_name="gpt-3.5-turbo",
                            openai_api_key=api_key
            )
            # 맵 프롬프트 설정: 1단계 요약에서 사용.
            prompt = PromptTemplate(
                template="""백틱으로 둘러싸인 전사본을 이용해 해당 유튜브 비디오를 요약해주세요. \
                ```{text}``` 단, 영어로 작성해주세요.
                """, input_variables=["text"]
            )
            # 컴바인 프롬프트 설정: 2단계 요약에서 사용.
            combine_prompt = PromptTemplate(
                template="""백틱으로 둘러싸인 유튜브 스크립트를 모두 조합하여 \
                ```{text}```
                10문장 내외의 간결한 요약문을 제공해주세요. 단, 영어로 작성해주세요.
                """, input_variables=["text"]
            )
            # LangChain을 활용하여 긴 글 요약하기
            # 긴 문서를 문자열 길이 3000을 기준 길이로 하여 분할한다.
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=3000, chunk_overlap=0)

            # 분할된 문서들은 pages라는 문자열 리스트로 저장되어져 있다
            # ex)
            # pages = ["텍스트1", "텍스트2", "텍스트3", "텍스트4"]
            pages = text_splitter.split_text(transcript)

            # pages를 load_summarize_chain이라는 Langchain 도구에서 처리 가능한 형식으로 변환.
            # 변환 후에는 더 이상 문자열 타입이 아닌 Langchain에서 제공하는 타입의 리스트로 변환됨.
            # ex)
            # text = [Document(page_content="텍스트1"), Document(page_content="텍스트2"),
            #         Document(page_content="텍스트3"), Document(page_content="텍스트4")]
            # 이렇게 Langchain에서 원하는 다소 특이한 형태로 변환해주어야 아래에서 처리 가능!
            text = text_splitter.create_documents(pages)

            # 위에서 준비한 map_prompt와 combine_prompt를 이용하여 두 단계 요약을 준비. run() 해야 실행.
            chain = load_summarize_chain(llm, chain_type="map_reduce", verbose=False,
                                            map_prompt=prompt, combine_prompt=combine_prompt)

            # 두 단계 요약의 결과를 저장.
            st.session_state["summarize"] = chain.run(text)
            st.success(st.session_state["summarize"])
            transe = trans(st.session_state["summarize"])
            st.subheader("Final Analysis Result (Reply in Korean)")
            st.info(transe)

if __name__=="__main__":
    main()