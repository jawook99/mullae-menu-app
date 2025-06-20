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

# 세션 상태 초기화
if "step" not in st.session_state:
    st.session_state.step = 1

# STEP 1: 1차 메뉴 선택
if st.session_state.step == 1:
    with st.spinner("예린이 뭐 먹고 싶을지 고민 중..."):
        time.sleep(1)

    choice = st.radio("예린이 뭐 땡겨?", ["튀긴 족발", "시금치 치킨", "둘 다", "산책하다가 느낌 오는 곳"])

    if st.button("선택 완료"):
        st.session_state.first_choice = choice
        st.session_state.step = 2

# STEP 2: 1차 결과 + 2차 메뉴 선택
if st.session_state.step == 2:
    if "first_choice" not in st.session_state:
        st.warning("⚠️ 1차 메뉴 선택이 누락되었어요. 처음부터 다시 시도해주세요.")
        st.session_state.step = 1
    else:
        with st.spinner("첫 메뉴 분석 중..."):
            time.sleep(1)

        first_choice = st.session_state.first_choice

        if first_choice == "튀긴 족발":
            st.markdown("후후.. 계획대로..")
        elif first_choice == "시금치 치킨":
            st.markdown("전기통닭 구이라 계획은 실패네요._.")
        elif first_choice == "둘 다":
            st.markdown("예린이 납치계획 출범 !-!")
        elif first_choice == "산책하다가 느낌 오는 곳":
            st.markdown("산책 좋아._. 플리 준비할게욤")

        second_choice = st.radio("2차는 뭐가 좋을까?", ["방아전이랑 칼칼한 전골", "다양한 술 테이스팅~"])

        if st.button("이걸로 가자"):
            st.session_state.second_choice = second_choice
            st.session_state.step = 2.5

# STEP 2.5: 좋아!-! 버튼 누르면 다음 단계로
if st.session_state.step == 2.5:
    if "second_choice" not in st.session_state:
        st.warning("⚠️ 2차 메뉴 선택이 누락되었어요. 처음부터 다시 시도해주세요.")
        st.session_state.step = 1
    else:
        if st.button("좋아!-!"):
            st.session_state.step = 3

# STEP 3: 결과 출력 + 저장
if st.session_state.step == 3:
    with st.spinner("2차까지 계산 중..."):
        time.sleep(1)

    second_choice = st.session_state.second_choice

    if second_choice == "방아전이랑 칼칼한 전골":
        st.markdown("방아전 그냥 산나물 느낌이래, 전골은 칼칼해서 예린 좋아할거 같아")
    elif second_choice == "다양한 술 테이스팅~":
        st.markdown("분위기도 엄청 좋데, 돼지고기 뽈살 구이._.")

    st.markdown("---")
    st.markdown("많이 보고싶어요 예린씨 **내일 너무 너무 재밌게 놀자**")

    # 결과 저장
    if not os.path.exists(SAVE_FILE):
        df = pd.DataFrame(columns=["timestamp", "first_choice", "second_choice"])
    else:
        df = pd.read_csv(SAVE_FILE)

    new_row = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "first_choice": st.session_state.get("first_choice", ""),
        "second_choice": st.session_state.get("second_choice", "")
    }

    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(SAVE_FILE, index=False)

    st.success("메-모._.")
