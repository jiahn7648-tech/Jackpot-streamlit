import streamlit as st
import random
import time

# --------------------
# 스타일 (CSS 애니메이션)
# --------------------
st.markdown(
    """
    <style>
    /* 전체 배경/폰트 (옵션) */
    .stApp {
        background: linear-gradient(180deg, #0b0b0b 0%, #ffffff 100%);
    }

    /* 잭팟: 반짝임 + 확대 */
    @keyframes jackpotPulse {
      0% { transform: scale(1); filter: drop-shadow(0 0 0 rgba(255,215,0,0)); opacity: 1; }
      50% { transform: scale(1.12); filter: drop-shadow(0 0 16px rgba(255,215,0,0.9)); opacity: 0.85; }
      100% { transform: scale(1); filter: drop-shadow(0 0 0 rgba(255,215,0,0)); opacity: 1; }
    }
    .jackpot-box {
      border-radius: 12px;
      padding: 18px;
      text-align: center;
      font-weight: 700;
      font-size: 20px;
      background: linear-gradient(90deg, #fff7c2, #fff0a0);
      color: #5a3e00;
      animation: jackpotPulse 0.9s ease-in-out infinite;
      margin-top: 12px;
    }

    /* 파산: 좌우 흔들림 + 빨간 플래시 */
    @keyframes bankruptShake {
      0% { transform: translateX(0); }
      20% { transform: translateX(-8px); }
      40% { transform: translateX(8px); }
      60% { transform: translateX(-6px); }
      80% { transform: translateX(6px); }
      100% { transform: translateX(0); }
    }
    @keyframes bankruptFlash {
      0% { background-color: rgba(255,0,0,0.0); }
      50% { background-color: rgba(255,0,0,0.15); }
      100% { background-color: rgba(255,0,0,0.0); }
    }
    .bankrupt-box {
      border-radius: 12px;
      padding: 18px;
      text-align: center;
      font-weight: 700;
      font-size: 20px;
      background: linear-gradient(90deg, #ffd6d6, #ffb3b3);
      color: #660000;
      animation: bankruptShake 0.45s ease-in-out 0s 3, bankruptFlash 0.9s ease-in-out 0s 2;
      margin-top: 12px;
    }

    /* 중앙 오버레이 (선택) */
    .overlay {
      position: fixed;
      left: 50%;
      top: 20%;
      transform: translateX(-50%);
      z-index: 9999;
      max-width: 480px;
      width: 90%;
    }

    /* 작은 장식 텍스트 */
    .slot-title {
      font-size: 34px;
      font-weight: 800;
      margin-bottom: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------
# 앱 타이틀
# --------------------
st.markdown('<div class="slot-title">🎰 간단 슬롯머신 게임</div>', unsafe_allow_html=True)

# --------------------
# 세션 상태 초기화
# --------------------
if "allcoin" not in st.session_state:
    st.session_state.allcoin = 500
if "last_result" not in st.session_state:
    st.session_state.last_result = None
if "message" not in st.session_state:
    st.session_state.message = ""
# anim_until: 애니메이션이 계속 보일 종료 시각 (epoch seconds)
# anim_type: "jackpot" 또는 "bankrupt" 또는 None
if "anim_until" not in st.session_state:
    st.session_state.anim_until = 0
if "anim_type" not in st.session_state:
    st.session_state.anim_type = None

e = [3, 4, 5]

# --------------------
# 슬롯 돌리기 로직
# --------------------
if st.button("🎮 슬롯 돌리기"):
    if st.session_state.allcoin <= 0:
        # 이미 파산 상태면 애니메이션(또는 경고)만 보여주도록 설정
        st.session_state.anim_type = "bankrupt"
        st.session_state.anim_until = time.time() + 2.0
        # 재실행해서 즉시 애니메이션 보이도록
        st.rerun()
    else:
        fi = random.choice(e)
        se = random.choice(e)
        th = random.choice(e)
        st.session_state.last_result = (fi, se, th)

        if fi == se == th:
            # 잭팟 보상 + 애니메이션
            st.session_state.allcoin += 500
            st.session_state.message = f"🎉 잭팟! +500 코인 (현재: {st.session_state.allcoin})"
            st.session_state.anim_type = "jackpot"
            st.session_state.anim_until = time.time() + 2.2
        else:
            st.session_state.allcoin -= 100
            st.session_state.message = f"아쉽습니다! 현재 코인: {st.session_state.allcoin}"
            # 만약 이로 인해 파산이면 파산 애니메이션
            if st.session_state.allcoin <= 0:
                st.session_state.anim_type = "bankrupt"
                st.session_state.anim_until = time.time() + 2.2

        # 재실행해서 화면이 새로고침되고 애니메이션 표시
        st.rerun()

# --------------------
# 애니메이션 표시 제어 (만료 검사)
# --------------------
now = time.time()
if st.session_state.anim_until and now > st.session_state.anim_until:
    # 애니메이션 시간 지났으면 초기화
    st.session_state.anim_type = None
    st.session_state.anim_until = 0

# --------------------
# 화면 출력
# --------------------
st.write(f"현재 보유 코인: **{st.session_state.allcoin}**")

# 결과 출력 (안전 검사)
if st.session_state.get("last_result"):
    fi, se, th = st.session_state.last_result
    st.write(f"결과: {fi} | {se} | {th}")

# 메시지(텍스트 메시지)는 애니메이션 대신 아래에 깔끔히 표시
if st.session_state.message:
    st.info(st.session_state.message)

# 파산 경고(항상 하이라이트로)
if st.session_state.allcoin <= 0:
    st.error("💀 파산했습니다! '다시하기'를 눌러 재시작하세요.")

st.markdown("---")

# 다시하기 버튼 (정상화)
if st.button("🔄 다시하기"):
    st.session_state.allcoin = 500
    if "last_result" in st.session_state:
        del st.session_state["last_result"]
    st.session_state.message = ""
    st.session_state.anim_type = None
    st.session_state.anim_until = 0
    st.rerun()

# --------------------
# 애니메이션 HTML (오버레이)
# --------------------
# 현재 애니메이션 종류에 따라 HTM

