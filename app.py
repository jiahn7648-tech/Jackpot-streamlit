import streamlit as st
import random
import time

st.set_page_config(page_title="슬롯머신", layout="wide")

st.markdown("<h1 style='text-align:center;'>🎰 슬롯머신 게임! 🎰</h1>", unsafe_allow_html=True)

if "allcoin" not in st.session_state:
    st.session_state.allcoin = 1000

if "last_result" not in st.session_state:
    st.session_state.last_result = None
if "message" not in st.session_state:
    st.session_state.message = ""
if "bankrupt_done" not in st.session_state:
    st.session_state.bankrupt_done = False

symbols = ["🍒", "⭐", "7️⃣"]

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

if st.button("🎮 슬롯 돌리기"):
    if st.session_state.allcoin <= 0:
        st.error("💀 파산 상태입니다! 다시하기 버튼을 눌러 재시작하세요.")
    else:
        a = random.choice(symbols)
        b = random.choice(symbols)
        c = random.choice(symbols)

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

        if st.session_state.allcoin <= 0 and not st.session_state.bankrupt_done:
            st.session_state.allcoin = 0
            bankrupt_overlay_animation()
            st.session_state.bankrupt_done = True

        if jackpot:
            jackpot_animation()

st.markdown(
    f"<h2 style='text-align:center; font-size:35px;'>💰 현재 보유 코인: <b>{st.session_state.allcoin}</b></h2>",
    unsafe_allow_html=True
)

if st.session_state.get("last_result"):
    a, b, c = st.session_state.last_result
    st.markdown(f"<h1 style='text-align:center; font-size:70px;'>{a} | {b} | {c}</h1>", unsafe_allow_html=True)
    st.info(st.session_state.message)
else:
    st.markdown("<h1 style='text-align:center; font-size:70px; color:gray;'>0 | 0 | 0</h1>", unsafe_allow_html=True)

# 다시하기를 폼 안에 넣어 submit으로 처리 (버튼 1회 클릭에 안정적 초기화 및 새로고침)
with st.form("reset_form"):
    reset = st.form_submit_button("🔄 다시하기")
    if reset:
        st.session_state.allcoin = 1000
        st.session_state.last_result = None
        st.session_state.message = ""
        st.session_state.bankrupt_done = False
        st.experimental_rerun()

