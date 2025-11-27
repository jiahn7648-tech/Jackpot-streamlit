import streamlit as st
import random
import time

# --------------------------
# 풍선 애니메이션 CSS
# --------------------------
st.markdown("""
<style>

@keyframes balloonUp {
    0% { transform: translateY(40px) scale(0.8); opacity: 0; }
    30% { opacity: 1; }
    100% { transform: translateY(-180px) scale(1.2); opacity: 0; }
}

.balloon {
    position: fixed;
    left: 50%;
    top: 50%;
    transform: translateX(-50%);
    font-size: 80px;
    animation: balloonUp 2.3s ease-in-out forwards;
    z-index: 99999;
}

</style>
""", unsafe_allow_html=True)

# --------------------------
# 기본 상태 초기화
# --------------------------
if "allcoin" not in st.session_state:
    st.session_state.allcoin = 500
if "result" not in st.session_state:
    st.session_state.result = None

# 애니메이션 상태
if "balloon_until" not in st.session_state:
    st.session_state.balloon_until = 0


# --------------------------
# 슬롯 함수
# --------------------------
def play_slot():
    nums = [3, 4, 5]
    return random.choice(nums), random.choice(nums), random.choice(nums)


st.title("🎰 간단 슬롯머신 게임")

# --------------------------
# 슬롯 돌리기 버튼
# --------------------------
if st.button("🎮 슬롯 돌리기"):
    fi, se, th = play_slot()
    st.session_state.result = (fi, se, th)

    # 잭팟 조건
    if fi == se == th:
        st.session_state.allcoin += 300
        st.session_state.balloon_until = time.time() + 2.0  # 풍선 표시 2초 유지
    else:
        st.session_state.allcoin -= 100

    st.rerun()

# --------------------------
# 풍선 애니메이션 출력
# --------------------------
now = time.time()
if now < st.session_state.balloon_until:
    st.markdown('<div class="balloon">🎈</div>', unsafe_allow_html=True)


# --------------------------
# 표시 UI
# --------------------------
st.write(f"현재 보유 코인: **{st.session_state.allcoin}**")

if st.session_state.result:
    st.write(f"결과: {st.session_state.result[0]} | {st.session_state.result[1]} | {st.session_state.result[2]}")

# 파산
if st.session_state.allcoin <= 0:
    st.error("💀 파산했습니다! 다시하기를 눌러주세요.")

# 다시하기 버튼
if st.button("🔄 다시하기"):
    st.session_state.allcoin = 500
    st.session_state.result = None
    st.session_state.balloon_until = 0
    st.rerun()


