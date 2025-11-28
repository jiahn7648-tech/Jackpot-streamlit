import streamlit as st
import random
import time

st.set_page_config(page_title="슬롯머신", layout="wide")

# 제목
st.markdown("<h1 style='text-align:center;'>🎰 슬롯머신 게임! 🎰</h1>", unsafe_allow_html=True)

# 초기 상태 설정
if "allcoin" not in st.session_state:
    st.session_state.allcoin = 1000
if "last_result" not in st.session_state:
    st.session_state.last_result = ("0", "0", "0")
if "message" not in st.session_state:
    st.session_state.message = ""
if "bankrupt_animation_done" not in st.session_state:
    st.session_state.bankrupt_animation_done = False

symbols = ["🍒", "⭐", "7️⃣"]

# 잭팟 애니메이션
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

# 파산 애니메이션 (완전히 끝난 후 초기화)
def bankrupt_animation_and_reset():
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
    time.sleep(1.0)  # 애니메이션 시간
    overlay.empty()
    
    # 애니메이션이 끝나면 상태 초기화 후 rerun
    st.session_state.allcoin = 1000
    st.session_state.last_result = ("0", "0", "0")
    st.session_state.message = ""
    st.session_state.bankrupt_animation_done = False
    st.experimental_rerun()

# 슬롯 돌리기
if st.button("🎮 슬롯 돌리기"):
    a, b, c = random.choice(symbols), random.choice(symbols), random.choice(symbols)
    st.session_state.last_result = (a, b, c)

    jackpot = False
    if a == b == c == "7️⃣":
        st.session_state.allcoin += 500
        st.session_state.message = "🎉 JACKPOT!!! 7️⃣7️⃣7️⃣ → +500원!"
        jackpot = True
    elif a == b == c:
        st.session_state.allcoin += 100
        st.session_state.message = "✨ 동일 이모지 3개! +100원"
    else:
        st.session_state.allcoin -= 100
        st.session_state.message = "아쉽습니다! -100원"

    # 파산 시 애니메이션 진행 후 자동 초기화
    if st.session_state.allcoin <= 0 and not st.session_state.bankrupt_animation_done:
        st.session_state.allcoin = 0
        st.session_state.bankrupt_animation_done = True
        bankrupt_animation_and_reset()

    if jackpot:
        jackpot_animation()

# 현재 코인 표시
st.markdown(
    f"<h2 style='text-align:center; font-size:35px;'>💰 현재 보유 코인: <b>{st.session_state.allcoin}</b></h2>",
    unsafe_allow_html=True
)

# 슬롯 결과 표시
a, b, c = st.session_state.last_result
st.markdown(f"<h1 style='text-align:center; font-size:70px;'>{a} | {b} | {c}</h1>", unsafe_allow_html=True)
if st.session_state.message:
    st.info(st.session_state.message)
