import random
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Wedge
import numpy as np

st.set_page_config(page_title="나는야 야구 스카우터!: 강한 팀을 만들어라", page_icon="⚾", layout="centered")

PLAYER_POOL = [
    "강호", "민수", "지훈", "서연", "예린", "도윤", "수아", "현우", "유진", "준호",
    "서준", "하윤", "채원", "시우", "연우", "지민", "태희", "우진", "가은", "승현"
]


def generate_name(seed_index):
    # KBO 스타일의 허구 이름 생성 (실제 선수 이름 사용 안 함)
    surnames = ["김", "이", "박", "최", "정", "강", "윤", "홍", "유", "권", "심", "안"]
    syllable_first = ["민", "준", "현", "재", "시", "동", "성", "영", "우", "지", "태", "승"]
    syllable_second = ["호", "진", "원", "훈", "석", "민", "빈", "윤", "준", "영", "우", "수"]
    f = surnames[seed_index % len(surnames)]
    g1 = syllable_first[(seed_index * 5) % len(syllable_first)]
    g2 = syllable_second[(seed_index * 7) % len(syllable_second)]
    return f + g1 + g2


def generate_candidates(n=18):
    # 18명의 선수 이름 (사용자 제시)
    player_names = [
        "김도영", "강민호", "강백호", "구자욱", "심우준", "김현수", 
        "박민우", "이정후", "송성문", "박건우", "윤동희", "박지환", 
        "최재훈", "박찬호", "박건우", "양의지", "박성한", "나성범"
    ]
    
    # 난이도별로 다른 타율을 생성: 쉬움(첫째자리) → 중간(둘째자리) → 어려움(셋째자리)
    candidates = []
    
    # 난이도별 그룹 (각 6명씩)
    # 그룹 0 (라운드 0-2): 정수부는 같고 소수 첫째 자리만 다름 (쉬움)
    # 그룹 1 (라운드 3-5): 정수부·첫째자리는 같고 둘째 자리만 다름 (중간)
    # 그룹 2 (라운드 6-8): 정수부·첫째·둘째 자리는 같고 셋째 자리까지 다름 (어려움)
    
    for group in range(3):
        for i in range(6):
            idx = group * 6 + i
            name = player_names[idx]
            # 사진 대신 이모티콘 사용 (야구 모자)
            photo = "🧢"
            
            if group == 0:  # 쉬움: 소수 첫째 자리만 다르게
                first_digit = (idx % 10)
                second_digit = 5
                third_digit = 0
                avg_val = 0 + first_digit / 10 + second_digit / 100 + third_digit / 1000
            elif group == 1:  # 중간: 소수 둘째 자리만 다르게
                first_digit = 5
                second_digit = (idx % 10)
                third_digit = 0
                avg_val = 0 + first_digit / 10 + second_digit / 100 + third_digit / 1000
            else:  # 어려움: 소수 셋째 자리만 다르게
                first_digit = 5
                second_digit = 5
                third_digit = (idx % 9) + 1
                avg_val = 0 + first_digit / 10 + second_digit / 100 + third_digit / 1000
            
            avg = f"{avg_val:.3f}"
            candidates.append({"name": name, "avg": avg, "avg_val": avg_val, "photo": photo})
    
    return candidates


def draw_baseball_field(team_players):
    """야구 경기장에 선수 이름을 배치한 그림 생성"""
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # 배경색 (잔디)
    ax.set_xlim(-1, 10)
    ax.set_ylim(-1, 10)
    ax.set_aspect('equal')
    ax.patch.set_facecolor('#2d5016')  # 진한 초록색
    
    # 내야 (다이아몬드)
    diamond = patches.Polygon([[5, 1], [9, 5], [5, 9], [1, 5]], 
                             closed=True, edgecolor='white', 
                             facecolor='#8B7355', linewidth=2)
    ax.add_patch(diamond)
    
    # 홈플레이트
    home = patches.Polygon([[5, 0.8], [4.8, 1.2], [5, 1.4], [5.2, 1.2]], 
                          closed=True, facecolor='white', edgecolor='white')
    ax.add_patch(home)
    
    # 포지션 좌표 (중심 기준)
    # 순서: 0=투수, 1=포수, 2=1루, 3=2루, 4=3루, 5=유격수, 6=좌익, 7=중견, 8=우익
    positions = {
        0: (5, 3.5),      # 투수 (마운드)
        1: (5, 1.3),      # 포수 (홈플레이트 뒤)
        2: (8.5, 5),      # 1루수
        3: (6.5, 6.5),    # 2루수
        4: (3.5, 6.5),    # 3루수
        5: (3.5, 3.5),    # 유격수
        6: (1, 8),        # 좌익수
        7: (5, 8.5),      # 중견수
        8: (9, 8)         # 우익수
    }
    
    # 각 포지션에 선수 이름 표시
    for pos_idx, (x, y) in positions.items():
        if pos_idx < len(team_players):
            player_name = team_players[pos_idx]
            # 선수 위치 표시
            circle = patches.Circle((x, y), 0.35, facecolor='yellow', 
                                   edgecolor='white', linewidth=2)
            ax.add_patch(circle)
            # 선수 이름
            ax.text(x, y, player_name, ha='center', va='center', 
                   fontsize=9, fontweight='bold', color='black')
    
    # 축 제거
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    
    plt.tight_layout()
    return fig

def make_hint(left, right):
    # 소수 비교 힌트 생성: 어떤 자리에서 차이가 나는지 알려줌(정답 직접 노출 X)
    la = left['avg_val']
    ra = right['avg_val']
    # 정수 부분
    lint = int(la)
    rint = int(ra)
    if lint != rint:
        return f"다시 생각해보세요! 정수 부분을 먼저 비교하세요. 왼쪽: {lint}, 오른쪽: {rint}"
    # 소수 첫째 자리
    l1 = int(la * 10) % 10
    r1 = int(ra * 10) % 10
    if l1 != r1:
        return f"다시 생각해보세요! 정수 부분은 같습니다. 소수 첫째 자리(0.1)를 비교하세요. 왼쪽: {l1}, 오른쪽: {r1}"
    # 소수 둘째 자리
    l2 = int(la * 100) % 10
    r2 = int(ra * 100) % 10
    if l2 != r2:
        return f"다시 생각해보세요! 첫째 자리도 같습니다. 소수 둘째 자리(0.01)를 비교하세요. 왼쪽: {l2}, 오른쪽: {r2}"
    return "다시 생각해보세요! 두 선수의 타율이 아주 비슷합니다. 소수 셋째 자리까지 확인해 보세요."


# 초기 상태 설정
if 'started' not in st.session_state:
    st.session_state.started = False
    st.session_state.score = 0
    st.session_state.team = []
    st.session_state.round = 0
    st.session_state.candidates = []
    st.session_state.message = ""
    st.session_state.awaiting_next = False

st.title("⚾ 나는야 야구 스카우터!: 강한 팀을 만들어라")

if not st.session_state.started:
    st.markdown(
        """
        여러분은 프로야구팀의 스카우터입니다. 선수들의 타율을 비교하여 더 뛰어난 유망주들을 찾아 팀에 영입해야합니다. 총 9명의 선수를 영입하는 것이 목표입니다.

        **스카우터와 타율이란?!**
        - **스카우터**: 경기를 보고 선수의 기량을 판단해 팀에 추천하는 사람입니다.
        - **타율**: 타자가 안타를 얼마나 잘 치는지를 나타내는 수로 보통 소수로 적습니다. 소수가 클수록 더 높은 타율입니다.
        """
    )

    if st.button("스카우트 참여하기"):
        st.session_state.started = True
        st.session_state.score = 0
        st.session_state.team = []
        st.session_state.round = 0
        st.session_state.candidates = generate_candidates(18)
        st.session_state.message = ""
        st.session_state.awaiting_next = False

else:
    # 게임 진행 화면
    candidates = st.session_state.candidates
    st.subheader(f"현재 팀: {len(st.session_state.team)}/9명")
    if st.session_state.team:
        st.write("영입 선수:", ", ".join(st.session_state.team))

    # 모든 라운드 완료 시
    if st.session_state.round >= 9:
        st.success("축하합니다! 팀 완성🎉 모든 포지션을 채웠습니다.")
        
        st.markdown("## ⚾ 당신의 스카우팅 팀 라인업")
        
        # 야구 경기장 그림 생성 및 표시
        team_players = st.session_state.team
        fig = draw_baseball_field(team_players)
        st.pyplot(fig)
        
        st.markdown("---")
        st.info("당신의 스카우팅이 완료되었습니다! 당신은 뛰어난 스카우터입니다! ⭐")
    else:
        idx = st.session_state.round * 2
        left = candidates[idx]
        right = candidates[idx + 1]

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"<h1 style='text-align: center;'>{left['photo']}</h1>", unsafe_allow_html=True)
            st.markdown(f"**{left['name']}**")
            st.write(f"타율: {left['avg']}")
        with col2:
            st.markdown(f"<h1 style='text-align: center;'>{right['photo']}</h1>", unsafe_allow_html=True)
            st.markdown(f"**{right['name']}**")
            st.write(f"타율: {right['avg']}")

        st.write(f"라운드 {st.session_state.round + 1} — 두 선수 중 타율이 더 높은 선수를 고르세요.")
        choice = st.radio("누구를 선택하겠어요?", (left['name'], right['name']))

        # 항상 제출 버튼을 렌더링하되, 클릭 처리 시 awaiting_next 상태를 확인
        submit_clicked = st.button("정답 제출", key=f"submit_{st.session_state.round}")
        if submit_clicked and (not st.session_state.awaiting_next):
            # 정답 판정 but do not advance round yet; show hint on wrong
            if left['avg_val'] > right['avg_val']:
                correct = left
            elif left['avg_val'] < right['avg_val']:
                correct = right
            else:
                correct = None

            if correct is None:
                # 무승부는 다음으로 넘어가도록 처리
                st.session_state.message = "두 선수의 타율이 같습니다. 무승부입니다."
                st.session_state.awaiting_next = True
            else:
                if choice == correct['name']:
                    st.session_state.team.append(correct['name'])
                    st.session_state.score += 1
                    st.session_state.message = f"정답! {correct['name']}(타율 {correct['avg']}) 선수를 영입했습니다."
                    st.session_state.awaiting_next = True
                else:
                    # 틀렸을 때는 정답을 바로 알려주지 않고 힌트를 준다
                    st.session_state.message = make_hint(left, right)
                    # awaiting_next는 True로 설정하지 않아 사용자가 다시 시도할 수 있도록 함

        if st.session_state.message:
            st.info(st.session_state.message)

        # 다음 라운드 버튼: 제출(정답 또는 무승부) 후에만 보인다
        if st.session_state.awaiting_next:
            if st.button("다음 라운드", key=f"next_{st.session_state.round}"):
                st.session_state.round += 1
                st.session_state.message = ""
                st.session_state.awaiting_next = False
                st.rerun()  # 즉시 새 라운드로 리프레시

    # 사이드바 상태 표시 제거(요청에 따라 숨김)

