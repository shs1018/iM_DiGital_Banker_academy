import streamlit as st
from audiorecorder import audiorecorder
import numpy as np
from openai import OpenAI
import os

# Streamlit 페이지 설정
st.set_page_config(
    page_title="음성 녹음 테스트",
    layout="wide"
)

st.title("🎙️ 음성 녹음 테스트")
st.markdown("---")

# OpenAI API 키 입력
if 'openai_api_key' not in st.session_state:
    st.session_state.openai_api_key = ''
    
api_key = st.text_input(
    "OpenAI API 키를 입력하세요:",
    value=st.session_state.openai_api_key,
    type="password",
    key="api_key_input"
)

st.session_state.openai_api_key = api_key

if not api_key:
    st.warning("OpenAI API 키를 입력해주세요.")
    st.stop()

client = OpenAI(api_key=api_key)

# 오디오 녹음 컴포넌트
st.write("아래 버튼을 눌러 음성을 녹음하세요:")
audio_recorder = audiorecorder("🎙️ 녹음", "⏹️ 정지")

if len(audio_recorder.recording):
    if not os.path.exists("temp"):
        os.makedirs("temp")
        
    # 녹음된 오디오를 파일로 저장
    audio_file = "temp/recorded_audio.wav"
    wav_file = open(audio_file, "wb")
    wav_file.write(audio_recorder.recording.tobytes())
    wav_file.close()
    
    # 오디오 재생
    st.audio(audio_recorder.recording)
    
    # Whisper를 사용한 음성-텍스트 변환
    try:
        with open(audio_file, "rb") as audio:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio,
                response_format="text"
            )
        st.success("음성 인식 결과:")
        st.write(transcript)
        
        # 임시 파일 삭제
        os.remove(audio_file)
        
    except Exception as e:
        st.error(f"음성 인식 중 오류가 발생했습니다: {str(e)}")
