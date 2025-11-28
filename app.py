import streamlit as st
import random

st.title("🎰 슬롯머신 게임!")

# 초기 코인 설정
if "allcoin" not in st.session_state:
    st.session_state.allcoin = 500

# 초기화할 상태값들 기본값
if "last_result" not in st.session_state:
    st.session_state.last_result = None
if "message" not in st.session_state:
    st.session_state.message = ""

e = [3, 4, 5]

# 슬롯 돌리기 버튼
if st.button("🎮 슬롯 돌리기"):
    if st.session_state.allcoin <= 0:
        st.warning("이미 파산 상태입니다! 다시하기를 눌러주세요.")
    else:
        fi = random.choice(e)
        se = random.choice(e)
        th = random.choice(e)

        st.session_state.last_result = (fi, se, th)

        if fi == se == th:
            st.session_state.message = "🎉 축하합니다! 모두 일치했습니다!!"
        else:
            st.session_state.allcoin -= 100
            st.session_state.message = f"아쉽습니다! 현재 코인: {st.session_state.allcoin}"

# 🔥 파산 체크
if st.session_state.allcoin <= 0:
    st.error("💀 파산했습니다! 다시하기 버튼을 눌러 재시작하세요.")

# 🔥 현재 보유 코인 — 크게 중앙에 표시
st.markdown(
    f"""
    <h2 style='text-align:center; font-size:35px;'>
        현재 보유 코인: <b>{st.session_state.allcoin}</b>
    </h2>
    """,
    unsafe_allow_html=True
)

# 🔥 슬롯 결과 표시 (또는 기본 화면 000 표시)
if st.session_state.get("last_result"):
    fi, se, th = st.session_state.last_result
    st.markdown(
        f"<h1 style='text-align:center; font-size:70px;'>{fi} | {se} | {th}</h1>",
        unsafe_allow_html=True
    )
    st.warning(st.session_state.message)
else:
    # 처음 화면 또는 초기화 화면 — 000 표시
    st.markdown(
        "<h1 style='text-align:center; font-size:70px; color:gray;'>0 | 0 | 0</h1>",
        unsafe_allow_html=True
    )

# 다시하기 버튼
if st.button("🔄 다시하기"):
    st.session_state.allcoin = 500
    st.session_state.last_result = None
    st.session_state.message = ""
    st.rerun()


