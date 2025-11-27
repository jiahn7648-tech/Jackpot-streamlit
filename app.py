import streamlit as st
import random

st.title("🎰 간단 슬롯머신 게임")

# 초기 코인 설정 (세션에 저장)
if "allcoin" not in st.session_state:
    st.session_state.allcoin = 500

e = [3, 4, 5]

# 슬롯 실행 함수
def play_slot():
    fi = random.choice(e)
    se = random.choice(e)
    th = random.choice(e)
    return fi, se, th

st.write(f"현재 보유 코인: **{st.session_state.allcoin}**")

if st.session_state.allcoin <= 0:
    st.error("파산했습니다! 새로고침하여 다시 시작하세요.")
else:
    if st.button("🎮 슬롯 돌리기"):
        fi, se, th = play_slot()
        st.write(f"결과: {fi} | {se} | {th}")

        if fi == se == th:
            st.success("🎉 축하합니다! 모두 일치했습니다!!")
        else:
            st.session_state.allcoin -= 100
            st.warning(f"아쉽습니다! 현재 코인: {st.session_state.allcoin}")
