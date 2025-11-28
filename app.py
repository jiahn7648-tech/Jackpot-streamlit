import streamlit as st
import random
import time

st.set_page_config(page_title="슬롯머신", layout="wide")

st.title("🎰 슬롯머신 게임!")

# 초기 코인
if "allcoin" not in st.session_state:
    st.session_state.allcoin = 1000  # 초기 코인

# 상태값 초기화
if "last_result" not in st.session_state:
    st.session_state.last_result = None
if "message" not in st.session_state:
    st.session_state.message = ""

# 슬롯 심볼
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

# 파산 애니메이션 (화면 전체 빨강 오버레이)
def bankrupt_overlay_animation():
    overlay_html = """
    <div id="overlay" style="
        position: fixed;
        top: 0; left: 0;
        width: 100%; height: 100%;
        background-color: rgba(255,0,0,0.6);
        z-index: 9999;
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
    """
    st.markdown(overlay_html, unsafe_allow_html=True)
    for i in range(10, -1, -1):
        st.markdown(f"""
        <style>
        #overlay {{
            opacity: {i/10};
            transition: opacity 0.1s;
        }}
        </style>
        """, unsafe_allow_html=True)
        time.sleep(0.1)
    st.markdown("""
    <style>
    #overlay {display:none;}
    </style>
    """, unsafe_allow_html=True)

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

        # 결과 계산
        jackpot = False
        if a == "7️⃣" and b == "7️⃣" and c == "7️⃣":
            st.session_state.allcoin += 1000
            st.session_state.message = "🎉 JACKPOT!!! 7️⃣7️⃣7️⃣ → +1000원!"
            jackpot = True
        elif a == b == c:
            st.session_state.allcoin += 100
            st.session_state.message = "✨ 동일 이모지 3개! +100원"
        else:
            st.session_state.allcoin -= 100
            st.session_state.message = "아쉽습니다! -100원"

        # 슬롯 심볼 먼저 화면에 표시
        a, b, c = st.session_state.last_result
        st.markdown(
            f"<h1 style='text-align:center; font-size:70px;'>{a} | {b} | {c}</h1>",
            unsafe_allow_html=True
        )
        st.info(st.session_state.message)

        # 코인 0 체크
        if st.session_state.allcoin <= 0:
            st.session_state.allcoin = 0
            bankrupt_overlay_animation()  # 화면 전체 빨강 애니메이션

        # 잭팟 애니메이션
        if jackpot:
            jackpot_animation()

# 현재 코인 크게 표시
st.markdown(
    f"<h2 style='text-align:center; font-size:35px;'>💰 현재 보유 코인: <b>{st.session_state.allcoin}</b></h2>",
    unsafe_allow_html=True
)

# 처음 화면 기본 슬롯
if not st.session_state.get("last_result"):
    st.markdown(
        "<h1 style='text-align:center; font-size:70px; color:gray;'>0 | 0 | 0</h1>",
        unsafe_allow_html=True
    )

# 다시하기 버튼
if st.button("🔄 다시하기"):
    st.session_state.allcoin = 1000
    st.session_state.last_result = None
    st.session_state.message = ""
    st.rerun()
