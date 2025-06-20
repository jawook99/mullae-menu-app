# mullae_menu_app.py
import streamlit as st
import time
import pandas as pd
from datetime import datetime
import os

# rerun 예외 방식 (버전 상관없이 안전하게 사용 가능)
from streamlit.runtime.scriptrunner import RerunException
from streamlit.runtime.scriptrunner.script_run_context import get_script_run_ctx

def safe_rerun():
    raise RerunException(get_script_run_ctx())

st.set_page_config(page_title="문래역 데이트 with 예린", page_icon="💌", layout="centered")

# 🔊 빗소리 배경음 삽입
st.markdown(
    """
    <audio autoplay loop>
        <source src="https://www.soundjay.com/nature/rain-02.mp3" type="audio/mp3">
    </audio>
    """,
    unsafe_allow_html=True
)

SAVE_FILE = "mullae_choice_log.csv"

# 세션 상태 초기화
if "step" not in st.session_state:
    st.session_state.step = 1

# STEP 1: 1차 메뉴 선택
if st.session_state.step == 1:
    st.title("문래역 데이트 메뉴 선택기")
    st.markdown("안녕하세요 소재욱입니다._.")
    st.markdown("내일 어떤거 먹을까요!-!")

    with st.spinner("예린이 뭐 먹고 싶을지 고민 중..."):
        time.sleep(1)
