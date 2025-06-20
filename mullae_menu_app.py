# mullae_menu_app.py
import streamlit as st

st.set_page_config(page_title="문래역 데이트 with 예린", page_icon="💌", layout="centered")

st.title("문래역 데이트 메뉴 선택기")

st.markdown("안녕하세요 소재욱입니다._.")
st.markdown("내일 어떤거 먹을까요!-!")

st.subheader("1차 메뉴 후보")
choice = st.radio("예린 어떤거 먹을까 ?", ["튀긴 족발", "시금치 치킨", "둘 다", "산책하다가 느낌 오는 곳"])

if choice == "튀긴 족발":
    st.markdown("후후.. 계획대로..")
elif choice == "시금치 치킨":
    st.markdown("전기통닭 구이라 계획은 실패네요._.")
elif choice == "둘 다":
    st.markdown("예린이 납치계획 출범 !-!")
elif choice == "산책하다가 느낌 오는 곳":
    st.markdown("산책 좋아._. 플리 준비할게욤")

st.subheader("2차는?")
second_choice = st.radio("뭐가 좋을까?", ["방아전이랑 칼칼한 전골", "다양한 술 테이스팅~"])

if second_choice == "방아전이랑 칼칼한 전골":
    st.markdown("방아전 그냥 산나물
