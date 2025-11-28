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
# bankrupt_animation_done은 애니메이션 중복 실행 방지용으로 유지
if "bankrupt_animation_done" not in st.session_state:
    st.session_state.bankrupt_animation_done = False
# bankrupt_flag: 파산 상태에 진입했음을 알리는 플래그 추가
if "bankrupt_flag" not in st.session_state:
    st.session_state.bankrupt_flag = False

symbols = ["🍒", "⭐", "7️⃣"]

# 잭팟 애니메이션 (콜백 함수 내에서 st.rerun 전에 실행되므로 st.time.sleep 사용 가능)
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

# --- 파산 처리 함수 ---
# 파산 애니메이션만 표시하고 상태 변경 플래그만 설정
def trigger_bankrupt_process():
    st.session_state.allcoin = 0 # 파산 금액 확정
    st.session_state.bankrupt_flag = True # 파산 처리 시작 플래그
    # bankrupt_animation_done은 애니메이션 중복 실행 방지용
    st.session_state.bankrupt_animation_done = False 

# 슬롯 돌리기 버튼
if st.button("🎮 슬롯 돌리기"):
    # 파산 상태에서는 버튼 작동을 막기 위해 early exit
    if st.session_state.bankrupt_flag:
        st.warning("먼저 '재시작' 버튼을 눌러주세요.")
        st.stop() # 슬롯 로직 실행 방지

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

    # 파산 조건 확인
    if st.session_state.allcoin <= 0:
        trigger_bankrupt_process() # 파산 플래그만 설정

    if jackpot:
        jackpot_animation()
    
    # 파산 플래그가 설정되었다면, 메인 루프에서 처리되도록 버튼 클릭 후에는 rerun을 하지 않습니다.
    # st.experimental_rerun() # 불필요

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

# --- 파산 상태 처리 (메인 스크립트 흐름에서 처리) ---
if st.session_state.bankrupt_flag:
    # 애니메이션이 아직 실행되지 않았다면 실행
    if not st.session_state.bankrupt_animation_done:
        # 애니메이션 표시
        overlay = st.empty()
        overlay.markdown("""
            <div style="
                position: fixed;
                top:0; left:0;
                width:100%; height:100%;
                background-color: rgba(255,0,0,0.8); /* 배경 불투명도 증가 */
                display:flex;
                flex-direction: column;
                justify-content:center;
                align-items:center;
                font-size:80px;
                color:white;
                font-weight:bold;
                text-align:center;
                z-index: 1000; /* 다른 요소 위에 표시 */
            ">
                💀 파산! 💀
                <div style="font-size:30px; margin-top: 20px;">재시작 버튼을 눌러주세요.</div>
            </div>
        """, unsafe_allow_html=True)
        
        # 애니메이션이 한 번 실행되었음을 표시
        st.session_state.bankrupt_animation_done = True
        
        # 사용자에게 재시작 버튼을 클릭하도록 유도
        st.markdown("<br><br>", unsafe_allow_html=True) # 공백 추가
        if st.button("🔄 게임 재시작 (코인 1000원)"):
            # 상태 초기화
            st.session_state.allcoin = 1000
            st.session_state.last_result = ("0", "0", "0")
            st.session_state.message = "게임이 초기화되었습니다! 다시 시작하세요."
            st.session_state.bankrupt_flag = False
            st.session_state.bankrupt_animation_done = False
            st.experimental_rerun() # 재실행하여 오버레이 제거

    # 파산 애니메이션이 표시된 후에는 '슬롯 돌리기' 버튼을 비활성화하고 재시작 버튼을 표시
