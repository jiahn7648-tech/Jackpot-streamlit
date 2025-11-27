import streamlit as st
import random

st.title("🎰 간단 슬롯머신 게임")

# 초기 코인 설정
if "allcoin" not in st.session_state:
    st.session_state.allcoin = 500

e = [3, 4, 5]

# 버튼을 눌렀을 때 먼저 코인 감소/판정 진행
if st.button("🎮 슬롯 돌리기"):
    fi = random.choice(e)
    se = random.choice(e)
    th = random.choice(e)

    st.session_state.last_result = (fi, se, th)

    # 결과 체크
    if fi == se == th:
        st.session_state.message = "🎉 축하합니다! 모두 일치했습니다!!"
    else:
        st.session_state.allcoin -= 100
        st.session_state.message = f"아쉽습니다! 현재 코인: {st.session_state.allcoin}"

# 화면 출력 부분 — 코인 감소 후 계산된 값을 사용
st.write(f"현재 보유 코인: **{st.session_state.allcoin}**")

# 결과 출력
if "last_result" in st.session_state:
    fi, se, th = st.session_state.last_result
    st.write(f"결과: {fi} | {se} | {th}")
    st.warning(st.session_state.message)

# 다시하기 버튼
if st.button("🔄 다시하기"):
    st.session_state.allcoin = 500
    st.session_state.last_result = None
    st.session_state.message = ""
    st.rerun()
