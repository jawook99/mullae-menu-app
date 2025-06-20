# mullae_menu_app.py
import streamlit as st
import time
import pandas as pd
from datetime import datetime
import os

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

st.title("문래역 데이트 메뉴 선택기")

st.markdown("안녕하세요 소재욱입니다._.")
st.markdown("내일 어떤거 먹을까요!-!")

SAVE_FILE = "mullae_choice_log.csv"

if "step" not in st.session_state:
    st.session_state.step = 1

# STEP 1: 1차 메뉴 선택
if st.session_state.step == 1:_
