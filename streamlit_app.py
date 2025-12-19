import random
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Wedge
from matplotlib.font_manager import FontProperties
import numpy as np
import os
import base64

st.set_page_config(page_title="나는야 야구 스카우터!: 강한 팀을 만들어라", page_icon="⚾", layout="centered")

# 페이지 전반 색감 및 버튼/컨테이너 스타일을 야구 느낌으로 개선
# 로컬 일러스트(우선순위: ./backgroundimages/baseball_field.avif → ./assets/)를 사용하고, 없으면 그라데이션을 사용
def _build_background_css():
    # 우선 순위: backgroundimages/baseball_field.avif → assets/ 내 파일들
    candidates = [
        os.path.join(os.getcwd(), "backgroundimages", "baseball_field.avif"),
        os.path.join(os.getcwd(), "assets", "field_bg.png"),
        os.path.join(os.getcwd(), "assets", "field_bg.jpg"),
        os.path.join(os.getcwd(), "assets", "field_bg.jpeg"),
        os.path.join(os.getcwd(), "assets", "field_bg.svg"),
    ]
    found = None
    for path in candidates:
        if os.path.isfile(path):
            found = path
            break

    if found:
        try:
            with open(found, "rb") as f:
                data = f.read()
            b64 = base64.b64encode(data).decode()
            mime = "image/png"
            if found.lower().endswith(".jpg") or found.lower().endswith(".jpeg"):
                mime = "image/jpeg"
            if found.lower().endswith(".svg"):
                mime = "image/svg+xml"
            bg_url = f"data:{mime};base64,{b64}"
            return f"""
            <style>
            .stApp {{ background-image: url('{bg_url}'); background-size: contain; background-position: center top; background-repeat: no-repeat; background-attachment: fixed; }}
            .block-container {{ background-color: rgba(255,255,255,0.82); border-radius: 12px; padding: 1.2rem 1.4rem; }}
            button.stButton>button {{ background-color: #1f618d; color: white; border-radius: 8px; }}
            .stProgress>div>div>div {{ background: #1f618d; }}
            h1, h2, h3 {{ color: #0b3d91; }}
            </style>
            """
        except Exception:
            # 파일 읽기 실패 시 폴백
            pass

    # 기본 그라데이션 폴백
    return """
    <style>
    .stApp { background: linear-gradient(180deg, #eaf6ff 0%, #d6f0ff 100%); }
    .css-1d391kg { background-color: rgba(255,255,255,0.6); }
    .block-container { border-radius: 12px; padding: 1.2rem 1.4rem; }
    button.stButton>button { background-color: #1f618d; color: white; border-radius: 8px; }
    .stProgress>div>div>div { background: #1f618d; }
    h1, h2, h3 { color: #0b3d91; }
    </style>
    """


st.markdown(_build_background_css(), unsafe_allow_html=True)

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
    # 사용자 폰트 로드: 우선적으로 프로젝트의 fonts/NanumGothic-Regular.ttf 사용
    font_prop = None
    try:
        fonts_dir = os.path.join(os.getcwd(), "fonts")
        # 우선 지정된 NanumGothic 파일을 찾는다
        preferred = os.path.join(fonts_dir, "NanumGothic-Regular.ttf")
        if os.path.isfile(preferred):
            font_prop = FontProperties(fname=preferred)
        else:
            # 지정된 파일이 없으면 폴더의 첫번째 ttf/otf를 시도
            if os.path.isdir(fonts_dir):
                ttf_files = [f for f in os.listdir(fonts_dir) if f.lower().endswith((".ttf", ".otf"))]
                if ttf_files:
                    font_path = os.path.join(fonts_dir, ttf_files[0])
                    font_prop = FontProperties(fname=font_path)
    except Exception:
        font_prop = None

    fig, ax = plt.subplots(figsize=(10, 10))
    
    # 배경색 (잔디)
    ax.set_xlim(-1, 10)
    ax.set_ylim(-1, 10)
    ax.set_aspect('equal')
    ax.patch.set_facecolor('#2d5016')  # 진한 초록색
    
    # 내야 (다이아몬드)
    diamond = patches.Polygon([[5, 1], [9, 5], [5, 9], [1, 5]], 
                             closed=True, edgecolor='white', 
                             facecolor='#d2b48c', linewidth=2)
    ax.add_patch(diamond)
    
    # 홈플레이트
    home = patches.Polygon([[5, 0.8], [4.8, 1.2], [5, 1.4], [5.2, 1.2]], 
                          closed=True, facecolor='white', edgecolor='white')
    ax.add_patch(home)
    
    # 포지션 좌표 (중심 기준)
    # 순서: 0=지명타자(DH), 1=포수, 2=1루, 3=2루, 4=3루, 5=유격수, 6=좌익, 7=중견, 8=우익
    positions = {
        # DH은 투수를 대신하는 자리로 홈 근처 측면에 배치
        0: (5, 2.2),      # 지명타자 (DH)
        1: (5, 1.3),      # 포수 (홈플레이트 뒤)
        2: (8.5, 5),      # 1루수
        3: (6.5, 6.5),    # 2루수
        4: (3.5, 7.2),    # 3루수 (조금 더 위쪽으로 이동)
        5: (3.5, 3.5),    # 유격수
        6: (1, 8),        # 좌익수
        7: (5, 8.5),      # 중견수
        8: (9, 8)         # 우익수
    }

    # 특정 선수의 위치를 고정/조정하는 규칙
    # 1) '박지환'이 팀에 있으면 왼쪽 꼭짓점(다이아몬드의 왼쪽 꼭지점, (1,5))에 배치
    # 2) '강민호'가 팀에 있으면 '구자욱'의 위치 오른쪽에 배치
    extra_draws = []
    try:
        # 팀 선수 목록이 리스트인지 확인
        if isinstance(team_players, (list, tuple)):
            # 박지환 처리
            if '박지환' in team_players:
                idx_bj = team_players.index('박지환')
                # 왼쪽 다이아몬드 꼭짓점 좌표로 이동
                positions[idx_bj] = (1.0, 5.0)
            else:
                # 팀에 없더라도 왼쪽 꼭짓점에 표시하길 원하면 extra_draws에 추가
                # (사용자가 팀에 항상 포함한다고 가정하지 않음) — 여기서는 팀에 없으면 그리지 않음
                pass

            # 구자욱과 강민호 처리
            if '구자욱' in team_players:
                idx_gj = team_players.index('구자욱')
                # 구자욱의 좌표(이미 positions에 설정되어 있을 것)
                gj_pos = positions.get(idx_gj)
                if gj_pos is not None:
                    gx, gy = gj_pos
                    # 오른쪽 옆(약간의 간격)으로 배치
                    target_x = min(gx + 0.6, 9.5)
                    target_y = gy
                    if '강민호' in team_players:
                        idx_km = team_players.index('강민호')
                        positions[idx_km] = (target_x, target_y)
                    else:
                        # 만약 강민호가 팀에 없다면 extra_draws로 그릴 수 있도록 추가
                        extra_draws.append(('강민호', (target_x, target_y)))
    except Exception:
        # 좌표 조정에서 오류 발생시 안전하게 무시하고 기본 배치 사용
        extra_draws = []
    
    # 각 포지션에 선수 이름 표시
    for pos_idx, (x, y) in positions.items():
        # 안전하게 선수 이름 가져오기
        player_name = ""
        if isinstance(team_players, (list, tuple)) and pos_idx < len(team_players):
            player_name = team_players[pos_idx] or ""

        # 선수 위치 표시
        circle = patches.Circle((x, y), 0.35, facecolor='white', 
                       edgecolor='#003366', linewidth=2)
        ax.add_patch(circle)
        # 선수 이름 (한글 폰트가 로드되면 사용)
        if font_prop is not None:
            ax.text(x, y, player_name, ha='center', va='center', 
                   fontsize=9, fontweight='bold', color='#003366', fontproperties=font_prop)
        else:
            ax.text(x, y, player_name, ha='center', va='center', 
                   fontsize=9, fontweight='bold', color='#003366')
    # extra_draws에 추가된 별도 표시들 (예: 강민호가 팀에 없을 때 구자욱 옆에 표시)
    try:
        for name, (ex, ey) in extra_draws:
            circle = patches.Circle((ex, ey), 0.35, facecolor='white', edgecolor='#003366', linewidth=2)
            ax.add_patch(circle)
            if font_prop is not None:
                ax.text(ex, ey, name, ha='center', va='center', fontsize=9, fontweight='bold', color='#003366', fontproperties=font_prop)
            else:
                ax.text(ex, ey, name, ha='center', va='center', fontsize=9, fontweight='bold', color='#003366')
    except Exception:
        pass
    
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
    # 소수 비교 힌트 생성: 어느 자리(정수/소수 자리)를 보면 좋을지 안내 (숫자 노출 없음)
    la = left['avg_val']
    ra = right['avg_val']
    # 정수 부분
    if int(la) != int(ra):
        return "다시 생각해보세요! 정수 부분을 먼저 비교해 보세요."
    # 소수 첫째 자리
    if int(la * 10) % 10 != int(ra * 10) % 10:
        return "다시 생각해보세요! 소수 첫째자리를 비교해 보세요."
    # 소수 둘째 자리
    if int(la * 100) % 10 != int(ra * 100) % 10:
        return "다시 생각해보세요! 소수 둘째자리를 비교해 보세요."
    return "다시 생각해보세요! 소수 셋째자리를 비교해 보세요."


# Removed draw_fireworks static image (user requested it deleted).


# 초기 상태 설정
if 'started' not in st.session_state:
    st.session_state.started = False
    st.session_state.score = 0
    st.session_state.team = []
    st.session_state.round = 0
    st.session_state.candidates = []
    st.session_state.message = ""
    st.session_state.awaiting_next = False
    st.session_state.pair_swapped = []
    st.session_state.mvp_mode = False
    st.session_state.mvp_season_ratings = {}
    st.session_state.mvp_message = ""
    st.session_state.mvp_awaiting_next = False
    st.session_state.balloons_shown = False

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
        # 각 라운드마다 좌우 배치를 무작위로 섞을 플래그 생성
        st.session_state.pair_swapped = [random.choice([True, False]) for _ in range(9)]

else:
    # 게임 진행 화면
    candidates = st.session_state.candidates
    st.subheader(f"현재 팀: {len(st.session_state.team)}/9명")
    if st.session_state.team:
        st.write("영입 선수:", ", ".join(st.session_state.team))

    # 모든 라운드 완료 시
    if st.session_state.round >= 9 and not st.session_state.mvp_mode:
        st.success("축하합니다! 팀 완성🎉 모든 포지션을 채웠습니다.")
        # 축하 연출: 풍선 애니메이션은 처음에만 한 번 표시
        if not st.session_state.balloons_shown:
            try:
                st.balloons()
                st.session_state.balloons_shown = True
            except Exception:
                pass

        st.markdown("## ⚾ 당신의 스카우팅 팀 라인업")

        # (폭죽 정적 그림은 삭제됨) — 풍선 애니메이션만 표시합니다.

        # 야구 경기장 그림 생성 및 표시
        team_players = st.session_state.team
        fig = draw_baseball_field(team_players)
        st.pyplot(fig)

        st.markdown("---")
        st.info("당신의 스카우팅이 완료되었습니다! 당신은 뛰어난 스카우터입니다! ⭐")

        # MVP 뽑기 버튼
        if st.button("🏆 MVP 뽑기", key="mvp_button"):
            st.session_state.mvp_mode = True
            # 팀 선수들의 시즌 타율을 랜덤으로 생성
            st.session_state.mvp_season_ratings = {}
            for player in st.session_state.team:
                # 시즌 타율: 0.200 ~ 0.400 사이의 랜덤 값
                season_rating = round(random.uniform(0.200, 0.400), 3)
                st.session_state.mvp_season_ratings[player] = season_rating
            st.session_state.mvp_message = ""
            st.session_state.mvp_awaiting_next = False
            st.rerun()  # 즉시 화면 전환

    # MVP 모드
    elif st.session_state.mvp_mode:
        st.markdown("---")
        st.subheader("🏆 시즌이 다 끝났습니다!")
        st.write("**팀의 선수들 시즌 타율:**")

        # 선수들의 시즌 타율을 표로 표시
        if st.session_state.mvp_season_ratings:
            import pandas as pd
            mvp_data = {
                "선수명": list(st.session_state.mvp_season_ratings.keys()),
                "시즌 타율": list(st.session_state.mvp_season_ratings.values()),
            }
            df = pd.DataFrame(mvp_data)
            # HTML 테이블로 직접 생성하여 가운데 정렬 적용
            html_table = "<table style='width: 100%; text-align: center; margin: 0 auto; border-collapse: collapse;'>"
            html_table += "<thead><tr style='background-color: #f0f2f6;'>"
            for col in df.columns:
                html_table += f"<th style='padding: 10px; border: 1px solid #ddd;'>{col}</th>"
            html_table += "</tr></thead>"
            html_table += "<tbody>"
            for _, row in df.iterrows():
                html_table += "<tr>"
                for val in row:
                    html_table += f"<td style='padding: 10px; border: 1px solid #ddd;'>{val}</td>"
                html_table += "</tr>"
            html_table += "</tbody></table>"
            st.markdown(html_table, unsafe_allow_html=True)

            # 최고 타율 선수 찾기
            max_player = max(st.session_state.mvp_season_ratings, 
                           key=st.session_state.mvp_season_ratings.get)
            max_rating = st.session_state.mvp_season_ratings[max_player]

            # 선수 선택
            st.write("**가장 타율이 높은 선수를 고르세요!**")
            choice = st.radio("MVP 후보:", list(st.session_state.mvp_season_ratings.keys()), 
                            key="mvp_choice")

            # 제출 버튼
            if st.button("MVP 선정", key="mvp_submit"):
                if choice == max_player:
                    st.session_state.mvp_message = f"✅ MVP선정이 완료되었습니다! 🎉\n\n**{choice}** 선수가 MVP로 선정되었습니다!"
                    st.session_state.mvp_awaiting_next = True
                else:
                    # 오답일 경우 힌트 제공
                    correct_avg = max_rating
                    selected_avg = st.session_state.mvp_season_ratings[choice]
                    
                    # 간단한 힌트: 소수 자리별 비교 (make_hint 함수 대신 직접 구현)
                    if int(selected_avg) != int(correct_avg):
                        hint_msg = "정수 부분을 먼저 비교해 보세요."
                    elif int(selected_avg * 10) % 10 != int(correct_avg * 10) % 10:
                        hint_msg = "소수 첫째자리를 비교해 보세요."
                    elif int(selected_avg * 100) % 10 != int(correct_avg * 100) % 10:
                        hint_msg = "소수 둘째자리를 비교해 보세요."
                    else:
                        hint_msg = "소수 셋째자리를 비교해 보세요."
                    
                    st.session_state.mvp_message = f"다시 한 번 생각해보세요.\n\n{hint_msg}"
                
                st.rerun()  # 화면 강제 새로고침


            if st.session_state.mvp_message:
                st.info(st.session_state.mvp_message)
    else:
        idx = st.session_state.round * 2
        # 이 라운드에서 좌우를 섞을지 확인
        swap = False
        if isinstance(st.session_state.pair_swapped, (list, tuple)) and len(st.session_state.pair_swapped) > st.session_state.round:
            swap = bool(st.session_state.pair_swapped[st.session_state.round])
        if swap:
            left = candidates[idx + 1]
            right = candidates[idx]
        else:
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

