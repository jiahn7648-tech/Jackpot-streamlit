import streamlit as st
import random
import time

st.set_page_config(page_title="슬롯머신", layout="wide")

# 제목 중앙 정렬
st.markdown("<h1 style='text-align:center;'>🎰 슬롯머신 게임! 🎰</h1>", unsafe_allow_html=True)

# 초기 코인 설정
if "allcoin" not in st.session_state:
    st.session_state.allcoin = 1000

# 상태 초기화
if "last_result" not in st.session_state:
    st.session_state.last_result = None
if "message" not in st.session_state:
    st.session_state.message = ""
if "bankrupt_done" not in st.session_state:
    st.session_state.bankrupt_done = False

# 슬롯 심볼 리스트
symbols = ["🍒", "⭐", "7️⃣"]

# 잭팟 애니메이션 함수
def jackpot_animation():
    placeholder = st.empty()
    for i in range(6):
        color = "gold" if i % 2 == 0 else "red"
        placeholder.markdown(
            f"<h1 style='text-align:center; font-size:85px; color:{color};'>🎉🎉 7️⃣7️⃣7️⃣ JACKPOT!!! 🎉🎉</h1>",
            unsafe_allow_html=True
        )
        time.sleep(0.2)
    placeholder.empty()
    st.balloons()

# 파산 애니메이션 함수 (화면 전체 빨간 오버레이)
def bankrupt_overlay_animation():
    overlay = st.empty()
    overlay.markdown("""
        <div style="
            position: fixed;
            top:0; left:0;
            width:100%; height:100%;
            background-color: rgba(255,0,0,0.6);
            display:flex;
            justify-content:center;
            align-items:center;
            font-size:80px;
            color:white;
            font-weight:bold;
            text-align:center;
        ">
            💀 파산! 💀
        </div>
    """, unsafe_allow_html=True)
    time.sleep(0.5)
    overlay.empty()

# 슬롯 돌리기 버튼
if st.button("🎮 슬롯 돌리기"):
    if st.session_state.allcoin <= 0:
        st.error("💀 파산 상태입니다! 다시하기 버튼을 눌러 재시작하세요.")
    else:
        a = random.choice(symbols)
        b = random.choice(symbols)
        c = random.choice(symbols)

        # 결과 저장
        st.session_state.last_result = (a, b, c)

        jackpot = False
        if a == "7️⃣" and b == "7️⃣" and c == "7️⃣":
            st.session_state.allcoin += 500
            st.session_state.message = "🎉 JACKPOT!!! 7️⃣7️⃣7️⃣ → +500원!"
            jackpot = True
        elif a == b == c:
            st.session_state.allcoin += 100
            st.session_state.message = "✨ 동일 이모지 3개! +100원"
        else:
            st.session_state.allcoin -= 100
            st.session_state.message = "아쉽습니다! -100원"

        # 파산 체크 및 애니메이션
        if st.session_state.allcoin <= 0 and not st.session_state.bankrupt_done:
            st.session_state.allcoin = 0
            bankrupt_overlay_animation()
            st.session_state.bankrupt_done = True

        # 잭팟 애니메이션
        if jackpot:
            jackpot_animation()

# 현재 코인 표시
st.markdown(
    f"<h2 style='text-align:center; font-size:35px;'>💰 현재 보유 코인: <b>{st.session_state.allcoin}</b></h2>",
    unsafe_allow_html=True
)

# 슬롯 결과 및 메시지 출력 (중복 출력 방지)
if st.session_state.get("last_result"):
    a, b, c = st.session_state.last_result
    st.markdown(f"<h1 style='text-align:center; font-size:70px;'>{a} | {b} | {c}</h1>", unsafe_allow_html=True)
    st.info(st.session_state.message)
else:
    st.markdown("<h1 style='text-align:center; font-size:70px; color:gray;'>0 | 0 | 0</h1>", unsafe_allow_html=True)

# 다시하기 버튼
if st.button("🔄 다시하기"):
    st.session_state.allcoin = 1000
    st.session_state.last_result = None
    st.session_state.message = ""
    st.session_state.bankrupt_done = False
    st.experimental_rerun()
