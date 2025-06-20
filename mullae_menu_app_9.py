import streamlit as st
import time
import pandas as pd
from datetime import datetime
import os
from PIL import Image, ImageDraw, ImageFont
import io

st.set_page_config(page_title="문래역 데이트", page_icon="💌", layout="centered")

SAVE_FILE = "mullae_choice_log.csv"
FONT_PATH = "assets/나눔손글씨_손편지체.ttf"
IMAGE_PATH = "assets/default_poodle.jpg"

st.title("문래역 데이트")

if "step" not in st.session_state:
    st.session_state.step = 0

# STEP 0: 이름 입력
if st.session_state.step == 0:
    st.title("오늘 데이트 주인공은 누구인가요?")
    st.text_input("이름을 입력해주세요", "예린")  # 기본값 "예린"
    if st.button("시작하기"):
        st.session_state.name = "예린"
        st.session_state.step = 1
        st.rerun()

# STEP 1: 1차 메뉴 선택
elif st.session_state.step == 1:
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

    # 이미지 둥글게 처리 함수
    def crop_circle(img):
        size = img.size
        mask = Image.new('L', size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size[0], size[1]), fill=255)
        result = Image.new('RGBA', size)
        result.paste(img, (0, 0), mask=mask)
        return result

    # 카드 이미지 생성
    try:
        font_hand_large = ImageFont.truetype(FONT_PATH, 36)
    except:
        font_hand_large = ImageFont.load_default()
        st.warning("손글씨 폰트를 불러올 수 없어 기본 폰트로 대체했어요.")

    try:
        default_img = Image.open(IMAGE_PATH).resize((240, 240))
        default_img = crop_circle(default_img)
    except:
        st.error("기본 이미지를 불러올 수 없습니다.")
        st.stop()

    card = Image.new("RGB", (800, 600), color=(255, 250, 245))
    draw = ImageDraw.Draw(card)
    draw.text((40, 40), f"{name}와의 문래역 데이트", fill="black", font=font_hand_large)
    draw.text((40, 140), f"[1차] {first_choice}", fill="black", font=font_hand_large)
    draw.text((40, 210), f"[2차] {second_choice}", fill="black", font=font_hand_large)
    draw.text((40, 300), "기대된다 내일 데이트", fill="black", font=font_hand_large)
    card.paste(default_img, (520, 340), default_img)  # 투명 배경 처리된 이미지 붙이기

    # 이미지 출력
    buf = io.BytesIO()
    card.save(buf, format="PNG")
    buf.seek(0)

    st.image(buf.getvalue(), caption="예린이와의 감성 카드", use_container_width=True)
    st.download_button("💾 카드 이미지 저장하기", data=buf.getvalue(), file_name="mullae_date_card.png", mime="image/png")

    # 결과 저장
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

    # 처음으로 돌아가기
    if st.button("처음으로 돌아가기"):
        st.session_state.clear()
        st.rerun()
