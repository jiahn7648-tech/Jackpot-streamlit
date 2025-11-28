import streamlit as st
import random

st.title("🎰 슬롯머신 게임!")

# 초기 코인
if "allcoin" not in st.session_state:
    st.session_state.allcoin = 500

# 상태값 초기화
if "last_result" not in st.session_state:
    st.session_state.last_result = None
if "message" not in st.session_state:
    st.session_state.message = ""

# 슬롯 심볼 (3개만 사용)
symbols = ["🍒", "⭐", "7️⃣"]


# 🎮 슬롯 돌리기 버튼
if st.button("🎮 슬롯 돌리기"):
    if st.session_state.allcoin <= 0:
        st.warning("이미 파산 상태입니다! 다시하기를 눌러주세요.")
    else:
        a = random.choice(symbols)
        b = random.choice(symbols)
        c = random.choice(symbols)

        st.session_state.last_result = (a, b, c)

        # 보상 규칙
        if a == "7️⃣" and b == "7️⃣" and c == "7️⃣":
            st.session_state.allcoin += 1000
            st.session_state.message = "🎉 JACKPOT!!! 7️⃣7️⃣7️⃣ → +1000원!"
        elif a == b == c:
            st.session_state.allcoin += 100
            st.session_state.message = f"✨ 동일 이모지 3개! +100원"
        else:
            st.session_state.allcoin -= 100
            st.session_state.message = "아쉽습니다! -100원"


# 💰 현재 코인 큰 글씨 표시
st.markdown(
    f"""
    <h2 style='text-align:center; font-size:35px;'>
        💰 현재 보유 코인: <b>{st.session_state.allcoin}</b>
    </h2>
    """,
    unsafe_allow_html=True
)


# 🎞️ 슬롯 결과 표시
if st.session_state.get("last_result"):
    a, b, c = st.session_state.last_result
    st.markdown(
        f"<h1 style='text-align:center; font-size:70px;'>{a} | {b} | {c}</h1>",
        unsafe_allow_html=True
    )
    st.info(st.session_state.message)
else:
    # 처음 화면 초기 출력
    st.markdown(
        "<h1 style='text-align:center; font-size:70px; color:gray;'>0 | 0 | 0</h1>",
        unsafe_allow_html=True
    )


# 🔄 다시하기 버튼
if st.button("🔄 다시하기"):
    st.session_state.allcoin = 500
    st.session_state.last_result = None
    st.session_state.message = ""
    st.rerun()


