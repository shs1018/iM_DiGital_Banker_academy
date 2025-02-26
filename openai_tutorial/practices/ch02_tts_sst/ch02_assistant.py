##### 기본 정보 입력 ####
# Streamlit 패키지 추가
import streamlit as st

# OpenAI 패키지 추가
from openai import OpenAI

# 채팅 시간을 기록하기 위한 패키지
from datetime import datetime

# 음성 녹음을 관리하기 위한 패키지
import pyaudio
import wave
import pygame

# 파이썬 기본 패키지
import os
import numpy as np
import base64

# API 키 가져오기 라인 제거
from get_key import get_openai_key  # 이 라인 삭제

##### 기능 구현 함수 #####
def record_audio(duration=5, sample_rate=44100):
    """Record audio for a specified duration"""
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    
    p = pyaudio.PyAudio()
    
    stream = p.open(format=FORMAT,
                   channels=CHANNELS,
                   rate=sample_rate,
                   input=True,
                   frames_per_buffer=CHUNK)
    
    print("Recording...")
    frames = []
    
    for i in range(0, int(sample_rate / CHUNK * duration)):
        data = stream.read(CHUNK)
        frames.append(data)
    
    print("Recording finished")
    
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    filename = 'input.wav'
    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(sample_rate)
    wf.writeframes(b''.join(frames))
    wf.close()
    
    return filename

def STT(audio_file, client):
    # 음성 파일 열기
    audio_file = open(audio_file, "rb")
    # Whisper 모델을 활용해 텍스트 얻기
    try:
        # openai의 whisper API를 활용하여 텍스트를 추출합니다.
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="text"
        )
        # Whisper로 STT가 끝났으니 이제 파일을 다시 삭제합니다.
        audio_file.close()
        os.remove(audio_file.name)
        return transcript
    except Exception as e:
        st.error(f"음성 인식 중 오류가 발생했습니다: {str(e)}")
        return "음성 인식에 실패했습니다."

def TTS(response):    
    try:
        # UTF-8로 인코딩하여 한글 처리
        response = response.encode('utf-8').decode('utf-8')
        
        # TTS를 활용하여 만든 음성을 파일로 저장
        with client.audio.speech.with_streaming_response.create(
            model="tts-1",
            voice="onyx",
            input=response,
        ) as response:
            filename = "output.mp3"
            response.stream_to_file(filename)
        
        # pygame을 사용하여 음성 파일 재생
        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        
        # 음성이 재생되는 동안 대기
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        
        pygame.mixer.quit()
        
        # 폴더에 남지 않도록 파일 삭제
        os.remove(filename)
    except Exception as e:
        st.error(f"TTS 처리 중 오류가 발생했습니다: {str(e)}")

# ChatGPT가 답변을 작성
def ask_gpt(prompt, client):
    try:
        response = client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=prompt
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"GPT 응답 중 오류가 발생했습니다: {str(e)}")
        return "죄송합니다. 응답을 생성하는 중 오류가 발생했습니다."

# Streamlit 페이지 설정
st.set_page_config(
    page_title="음성 비서 프로그램🔊",
    layout="wide"
)

# session state 초기화
if "chat" not in st.session_state:
    st.session_state["chat"] = []

if "check_audio" not in st.session_state:
    st.session_state["check_audio"] = []

if "messages" not in st.session_state:
    st.session_state["messages"] = [{
        "role": "system",
        "content": 'You are a thoughtful assistant. Respond to all input in 25 words and answer in korean'
    }]

# 제목
st.image('ai.png', width=200)
st.header('나만의 인공지능 비서 🔊')
st.markdown('---')
st.subheader('모르는 질문을 하면 답변해줄거에요.🎤')

# OpenAI API 키 입력 UI
if 'openai_api_key' not in st.session_state:
    st.session_state.openai_api_key = ''
    
api_key = st.text_input(
    "OpenAI API 키를 입력하세요:",
    value=st.session_state.openai_api_key,
    type="password",
    key="api_key_input"
)

# 입력된 키 저장
st.session_state.openai_api_key = api_key

# API 키가 입력되지 않은 경우 경고 표시
if not api_key:
    st.warning("OpenAI API 키를 입력해주세요.")
    st.stop()

client = OpenAI(api_key=api_key)

# 음성 입력 확인 Flag
flag_start = False

# 녹음 버튼은 API 키가 입력된 경우에만 표시
if api_key:
    # 기능 구현 공간
    col1, col2 = st.columns(2)
    with col1:
        if st.button("녹음 시작 (5초)"):
            audio_file = record_audio(duration=5)
            question = STT(audio_file, client)
            
            # 채팅 시각화를 위한 질문 내용 저장
            now = datetime.now().strftime("%H:%M")
            st.session_state["chat"].append(("user", now, question))
            
            # GPT 모델에 넣을 프롬프트를 위해 질문 저장
            st.session_state["messages"].append({"role": "user", "content": question})
            flag_start = True

with col2:
    st.subheader('대화기록 ⌨')
    if flag_start:
        # ChatGPT에게 답변 얻기
        response = ask_gpt(st.session_state["messages"], client)
        
        # GPT 모델에 넣을 프롬프트를 위해 답변 내용 저장
        st.session_state["messages"].append({"role": "assistant", "content": response})
        
        # 채팅 시각화를 위한 답변 내용 저장
        now = datetime.now().strftime("%H:%M")
        st.session_state["chat"].append(("bot", now, response))
        
        # 채팅 형식으로 시각화
        for sender, time, message in st.session_state["chat"]:
            if sender == "user":
                st.write(f'<div style="display:flex;align-items:center;"><div style="background-color:#007AFF;color:white;border-radius:12px;padding:8px 12px;margin-right:8px;">{message}</div><div style="font-size:0.8rem;color:gray;">{time}</div></div>', unsafe_allow_html=True)
                st.write("")
            else:
                st.write(f'<div style="display:flex;align-items:center;justify-content:flex-end;"><div style="background-color:lightgray;border-radius:12px;padding:8px 12px;margin-left:8px;">{message}</div><div style="font-size:0.8rem;color:gray;">{time}</div></div>', unsafe_allow_html=True)
                st.write("")
        
        # TTS로 답변 음성 생성 및 재생
        TTS(response)