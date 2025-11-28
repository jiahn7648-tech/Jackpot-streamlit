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
# 게임 상태 관리용: "IDLE" | "BANKRUPT_ANIMATION"
if "game_state" not in st.session_state:
    st.session_state.game_state = "IDLE"

symbols = ["🍒", "⭐", "7️⃣"]

# 잭팟 애니메이션 (현재 스크립트 실행 내에서만 표시)
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

# 슬롯 돌리기 버튼
if st.button("🎮 슬롯 돌리기"):
    
    # 이미 파산 애니메이션 상태라면 버튼 클릭 무시 (이 경우는 메인 스크립트 흐름에서 처리됨)
    if st.session_state.game_state == "BANKRUPT_ANIMATION":
        st.stop()

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

    # 파산 시 상태 변경 후 즉시 재실행
    if st.session_state.allcoin <= 0:
        st.session_state.allcoin = 0
        st.session_state.game_state = "BANKRUPT_ANIMATION"
        st.experimental_rerun() # 이 재실행으로 파산 애니메이션 로직으로 진입

    if jackpot:
        jackpot_animation()
    
# --- 게임 상태별 표시 로직 ---

# 1. 파산 애니메이션 상태 처리
if st.session_state.game_state == "BANKRUPT_ANIMATION":
    
    # 1. 애니메이션 오버레이 표시
    overlay = st.empty()
    overlay.markdown("""
        <div style="
            position: fixed;
            top:0; left:0;
            width:100%; height:100%;
            background-color: rgba(255,0,0,0.8);
            display:flex;
            justify-content:center;
            align-items:center;
            font-size:80px;
            color:white;
            font-weight:bold;
            text-align:center;
            z-index: 1000;
        ">
            💀 파산! 게임을 재시작합니다... 💀
        </div>
    """, unsafe_allow_html=True)
    
    # 2. 애니메이션을 볼 수 있도록 잠시 대기 (Streamlit을 블록합니다)
    time.sleep(1.5) # 1.5초 동안 파산 화면 표시
    
    # 3. 모든 상태 초기화
    st.session_state.allcoin = 1000
    st.session_state.last_result = ("0", "0", "0")
    st.session_state.message = "💀 파산 후 자동 재시작되었습니다! 코인 1000원으로 다시 시작합니다."
    st.session_state.game_state = "IDLE" # 상태를 IDLE로 되돌림
    
    # 4. 재실행하여 오버레이 제거 및 초기화된 게임 화면 표시
    st.experimental_rerun()

# 2. 기본 게임 화면 표시 (IDLE 상태)
# 이 부분은 BANKRUPT_ANIMATION 상태에서는 실행되지 않습니다.
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
