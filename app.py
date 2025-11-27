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
    # 이미 파산 상태면 실행하지 않기
    if st.session_state.allcoin <= 0:
        st.warning("이미 파산 상태입니다! 다시하기를 눌러주세요.")
    else:
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

# 🔥 파산 체크
if st.session_state.allcoin <= 0:
    st.error("💀 파산했습니다! 다시하기 버튼을 눌러 재시작하세요.")

# 화면 표시
st.write(f"현재 보유 코인: **{st.session_state.allcoin}**")

# 안전하게 출력
if st.session_state.get("last_result"):
    fi, se, th = st.session_state.last_result
    st.write(f"결과: {fi} | {se} | {th}")
    st.warning(st.session_state.message)

# 다시하기 버튼
if st.button("🔄 다시하기"):
    st.session_state.allcoin = 500
    if "last_result" in st.session_state:
        del st.session_state["last_result"]
    st.session_state.message = ""
    st.rerun()  # 🔥 Streamlit Cloud에서 완전히 정상 작동!



