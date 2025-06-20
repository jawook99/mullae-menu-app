import streamlit as st
import time
import pandas as pd
from datetime import datetime
import os
from PIL import Image, ImageDraw, ImageFont, ImageOps
import io

st.set_page_config(page_title="문래역 데이트 with 예린", page_icon="💌", layout="centered")

SAVE_FILE = "mullae_choice_log.csv"
DEFAULT_IMAGE_PATH = "/mnt/data/KakaoTalk_20250619_164018121.jpg"  # 기본 감성 이미지 (하얀 강아지)

if "step" not in st.session_state:
    st.session_state.step = 0

# STEP 0: 이름 입력
if st.session_state.step == 0:
    st.title("오늘 데이트 주인공은 누구인가요?")
    st.text_input("이름을 입력해주세요", "예린")  # 입력은 무시됨
    if st.button("시작하기"):
        st.session_state.name = "예린이"
        st.session_state.step = 1
        st.rerun()

# STEP 1: 1차 메뉴 선택
elif st.session_state.step == 1:
    st.title("문래역 데이트 메뉴 선택기")
    st.markdown(f"안녕하세요 소재욱입니다._.\n{st.session_state.name}씨 내일 어떤거 먹을까요!-!")

    with st.spinner(f"{st.session_state.name}씨 뭐 먹고 싶을지 고민 중..."):
        time.sleep(1)

    choice = st.radio("무엇이 땡겨요?", ["튀긴 족발", "시금치 치킨", "둘 다", "산책하다가 느낌 오는 곳"])

    if st.button("선택 완료"):
        st.session_state["first_choice"] = choice
        st.session_state.step = 2
        st.rerun()

# STEP 2: 1차 결과 + 2차 메뉴 선택
elif st.session_state.step == 2:
    with st.spinner("첫 메뉴 분석 중..."):
        time.sleep(1)

    first_choice = st.session_state["first_choice"]

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
        st.session_state["second_choice"] = second_choice
        st.session_state.step = 3
        st.rerun()

# STEP 3: 결과 출력 + 카드 생성
elif st.session_state.step == 3:
    with st.spinner("2차까지 계산 중..."):
        time.sleep(1)

    name = st.session_state.name
    first_choice = st.session_state["first_choice"]
    second_choice = st.session_state["second_choice"]

    if second_choice == "방아전이랑 칼칼한 전골":
        st.markdown("방아전 그냥 산나물 느낌이래, 전골은 칼칼해서 예린 좋아할거 같아")
    elif second_choice == "다양한 술 테이스팅~":
        st.markdown("분위기도 엄청 좋데, 돼지고기 뽈살 구이._.")

    st.markdown("---")
    st.markdown(f"많이 보고싶어요 **{name}**씨 **내일 너무 너무 재밌게 놀자**")

    # 🔄 사진 업로드 or 기본 이미지 사용
    uploaded_image = st.file_uploader("사진을 올려줘 (선택)", type=["jpg", "jpeg", "png"])

    try:
        user_image = Image.open(uploaded_image).convert("RGB") if uploaded_image else Image.open(DEFAULT_IMAGE_PATH).convert("RGB")
    except:
        st.error("기본 이미지를 불러오는 데 실패했어요.")
        st.stop()

    # ✍️ 카드 생성
    handwriting_font_path = "/mnt/data/나눔손글씨 손편지체.ttf"
    font_hand_large = ImageFont.truetype(handwriting_font_path, 36)

    card = Image.new("RGB", (800, 600), color=(255, 250, 245))
    draw = ImageDraw.Draw(card)
    draw.text((40, 40), f"{name}와의 문래역 데이트", fill="black", font=font_hand_large)
    draw.text((40, 140), f"[1차] {first_choice}", fill="black", font=font_hand_large)
    draw.text((40, 210), f"[2차] {second_choice}", fill="black", font=font_hand_large)
    draw.text((40, 300), "기대된다 내일 데이트", fill="black", font=font_hand_large)

    resized_img = user_image.resize((180, 180))
    mask = Image.new("L", (180, 180), 0)
    ImageDraw.Draw(mask).ellipse([(0, 0), (180, 180)], fill=255)

    circle_img = ImageOps.fit(resized_img, (180, 180))
    circle_img.putalpha(mask)

    border_img = Image.new("RGBA", (190, 190), (255, 255, 255, 0))
    border_img.paste(circle_img, (5, 5), circle_img)
    card.paste(border_img, (580, 390), border_img)

    # 💾 이미지 출력 및 다운로드
    buf = io.BytesIO()
    card.save(buf, format="PNG")
    buf.seek(0)

    st.image(buf.getvalue(), caption="예린이와의 감성 카드", use_column_width=True)
    st.download_button("💾 카드 이미지 저장하기", data=buf.getvalue(), file_name="mullae_date_card.png", mime="image/png")

    # 📦 결과 저장
    if not os.path.exists(SAVE_FILE):
        df = pd.DataFrame(columns=["timestamp", "name", "first_choice", "second_choice"])
    else:
        df = pd.read_csv(SAVE_FILE)

    new_row = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "name": name,
        "first_choice": first_choice,
        "second_choice": second_choice
    }

    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(SAVE_FILE, index=False)

    # 🔁 처음으로 돌아가기
    if st.button("처음으로 돌아가기"):
        st.session_state.clear()
        st.rerun()