from __future__ import annotations

from collections import Counter
from uuid import uuid4

import folium
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium


st.set_page_config(
    page_title="동네 사용설명서",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded",
)


DISTRICTS = ["종로구", "중구"]
FOLDER_OPTIONS = ["전체", "종로구", "중구"]
PLACE_TYPES = [
    "쉬기 좋은 곳",
    "걷기 좋은 길",
    "기다리기 좋은 곳",
    "만남 장소",
    "계절별 추천 장소",
    "생활 편의 장소",
    "역사·문화 산책길",
    "비 오는 날 피하기 좋은 곳",
    "밤에도 걷기 괜찮은 길",
]
TIME_PERIODS = ["아침", "점심", "저녁", "밤"]
SEASONS = ["봄", "여름", "가을", "겨울", "사계절"]
TAGS = [
    "조용함",
    "그늘 있음",
    "햇빛 좋음",
    "혼자 가기 좋음",
    "친구와 가기 좋음",
    "기다리기 좋음",
    "산책하기 좋음",
    "사진 찍기 좋음",
    "비 피하기 좋음",
    "찾기 쉬움",
    "사람 덜 붐빔",
]

MAP_VIEWS = {
    "전체": {"center": [37.5708, 126.9911], "zoom": 14},
    "종로구": {"center": [37.5758, 126.9862], "zoom": 14},
    "중구": {"center": [37.5628, 126.9944], "zoom": 14},
}

TYPE_STYLES = {
    "쉬기 좋은 곳": {"color": "green", "icon": "tree", "tone": "#eaf7ed"},
    "걷기 좋은 길": {"color": "blue", "icon": "road", "tone": "#eaf2ff"},
    "기다리기 좋은 곳": {"color": "orange", "icon": "clock", "tone": "#fff4df"},
    "만남 장소": {"color": "purple", "icon": "star", "tone": "#f2ebff"},
    "계절별 추천 장소": {"color": "pink", "icon": "heart", "tone": "#fff0f5"},
    "생활 편의 장소": {"color": "cadetblue", "icon": "info", "tone": "#e7f5f5"},
    "역사·문화 산책길": {"color": "darkred", "icon": "landmark", "tone": "#fff0e9"},
    "비 오는 날 피하기 좋은 곳": {"color": "darkblue", "icon": "cloud-rain", "tone": "#eaf3f8"},
    "밤에도 걷기 괜찮은 길": {"color": "darkpurple", "icon": "moon", "tone": "#f0efff"},
}


def inject_style() -> None:
    st.markdown(
        """
        <style>
        :root {
            --ink: #202124;
            --muted: #686f76;
            --line: #dde3e8;
            --paper: #fbfcf8;
            --soft-green: #eef7ee;
            --soft-blue: #edf4fb;
            --accent: #2f7d63;
        }

        .stApp {
            background:
                linear-gradient(180deg, #f8fbf6 0%, #f7f8f4 38%, #f4f7f8 100%);
            color: var(--ink);
        }

        section[data-testid="stSidebar"] {
            background: #f6f8f3;
            border-right: 1px solid var(--line);
        }

        .block-container {
            padding-top: 2.1rem;
            padding-bottom: 3rem;
            max-width: 1320px;
        }

        h1, h2, h3 {
            letter-spacing: 0;
        }

        div[data-testid="stMetric"] {
            background: rgba(255, 255, 255, 0.72);
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: 14px 16px;
        }

        .hero {
            border: 1px solid #d8e4dc;
            background:
                linear-gradient(120deg, rgba(239, 248, 235, 0.98), rgba(238, 245, 250, 0.98)),
                radial-gradient(circle at 92% 14%, rgba(47, 125, 99, 0.10), transparent 30%);
            border-radius: 8px;
            padding: 28px 30px;
            margin-bottom: 18px;
        }

        .hero-kicker {
            color: #2f7d63;
            font-weight: 700;
            font-size: 0.92rem;
            margin-bottom: 8px;
        }

        .hero-title {
            color: #202124;
            font-size: 2.45rem;
            font-weight: 800;
            line-height: 1.14;
            margin: 0 0 8px 0;
        }

        .hero-copy {
            color: #4c555d;
            font-size: 1.04rem;
            line-height: 1.68;
            max-width: 820px;
            margin: 0;
        }

        .folder-card {
            border: 1px solid var(--line);
            background: rgba(255, 255, 255, 0.82);
            border-radius: 8px;
            padding: 16px 17px;
            min-height: 138px;
        }

        .folder-title {
            font-size: 1.05rem;
            font-weight: 800;
            margin: 0 0 8px 0;
        }

        .folder-meta {
            color: var(--muted);
            font-size: 0.9rem;
            line-height: 1.5;
            margin: 0;
        }

        .folder-number {
            font-size: 1.9rem;
            font-weight: 800;
            color: #2f7d63;
            margin: 8px 0 2px 0;
        }

        .place-card {
            border: 1px solid var(--line);
            background: rgba(255, 255, 255, 0.86);
            border-radius: 8px;
            padding: 15px 16px 13px 16px;
            margin-bottom: 10px;
        }

        .place-card:hover {
            border-color: #b7cbc0;
            background: #ffffff;
        }

        .place-topline {
            display: flex;
            justify-content: space-between;
            gap: 12px;
            align-items: flex-start;
        }

        .place-title {
            font-weight: 800;
            font-size: 1.02rem;
            margin: 0;
        }

        .place-district {
            color: #2f7d63;
            font-size: 0.82rem;
            font-weight: 700;
            white-space: nowrap;
        }

        .place-meta {
            color: var(--muted);
            font-size: 0.86rem;
            margin: 7px 0 9px 0;
            line-height: 1.45;
        }

        .place-desc {
            color: #30363b;
            font-size: 0.95rem;
            line-height: 1.55;
            margin: 0 0 10px 0;
        }

        .tag {
            display: inline-block;
            border: 1px solid #d7e3dc;
            background: #f6faf6;
            border-radius: 999px;
            padding: 3px 8px;
            margin: 0 4px 5px 0;
            color: #37584d;
            font-size: 0.78rem;
        }

        .type-chip {
            display: inline-block;
            border-radius: 999px;
            padding: 4px 9px;
            font-weight: 700;
            font-size: 0.78rem;
            color: #25302c;
            margin-bottom: 8px;
        }

        .section-note {
            color: var(--muted);
            font-size: 0.92rem;
            line-height: 1.55;
            margin-top: -6px;
            margin-bottom: 14px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def base_place_folders() -> dict[str, list[dict]]:
    return {
        "종로구": [
            {
                "id": "jongno-001",
                "district": "종로구",
                "place_name": "청계천 광교 아래 그늘길",
                "latitude": 37.5692,
                "longitude": 126.9825,
                "place_type": "걷기 좋은 길",
                "time_period": ["점심", "저녁"],
                "season": ["여름", "가을"],
                "tags": ["그늘 있음", "산책하기 좋음", "혼자 가기 좋음", "사람 덜 붐빔"],
                "description": "여름 점심 이후 다리 아래 그늘이 이어져 짧게 걷고 숨 고르기 좋음",
                "likes": 18,
            },
            {
                "id": "jongno-002",
                "district": "종로구",
                "place_name": "광화문역 7번 출구 앞 넓은 보도",
                "latitude": 37.5718,
                "longitude": 126.9769,
                "place_type": "만남 장소",
                "time_period": ["점심", "저녁"],
                "season": ["사계절"],
                "tags": ["찾기 쉬움", "친구와 가기 좋음", "기다리기 좋음"],
                "description": "처음 오는 사람도 설명하기 쉬워 약속 전 짧게 모이기 좋음",
                "likes": 25,
            },
            {
                "id": "jongno-003",
                "district": "종로구",
                "place_name": "서촌 골목 낮은 담장길",
                "latitude": 37.5795,
                "longitude": 126.9706,
                "place_type": "역사·문화 산책길",
                "time_period": ["아침", "점심"],
                "season": ["봄", "가을"],
                "tags": ["조용함", "산책하기 좋음", "사진 찍기 좋음", "혼자 가기 좋음"],
                "description": "이른 시간에 걸으면 골목의 생활감과 오래된 담장 분위기를 천천히 볼 수 있음",
                "likes": 31,
            },
            {
                "id": "jongno-004",
                "district": "종로구",
                "place_name": "익선동 골목 입구 처마 아래",
                "latitude": 37.5741,
                "longitude": 126.9896,
                "place_type": "비 오는 날 피하기 좋은 곳",
                "time_period": ["점심", "저녁"],
                "season": ["여름", "사계절"],
                "tags": ["비 피하기 좋음", "기다리기 좋음", "찾기 쉬움"],
                "description": "비가 갑자기 올 때 골목 들어가기 전 우산을 정리하거나 일행을 기다리기 좋음",
                "likes": 12,
            },
            {
                "id": "jongno-005",
                "district": "종로구",
                "place_name": "낙산 성곽길 완만한 구간",
                "latitude": 37.5807,
                "longitude": 127.0077,
                "place_type": "밤에도 걷기 괜찮은 길",
                "time_period": ["저녁", "밤"],
                "season": ["봄", "가을", "사계절"],
                "tags": ["산책하기 좋음", "혼자 가기 좋음", "사진 찍기 좋음"],
                "description": "조명이 이어지는 구간이라 저녁에 짧게 걷고 도심 야경을 보기 좋음",
                "likes": 28,
            },
            {
                "id": "jongno-006",
                "district": "종로구",
                "place_name": "북촌 초입 조용한 골목 쉼터",
                "latitude": 37.5814,
                "longitude": 126.9848,
                "place_type": "쉬기 좋은 곳",
                "time_period": ["아침", "점심"],
                "season": ["봄", "가을"],
                "tags": ["조용함", "혼자 가기 좋음", "사람 덜 붐빔"],
                "description": "사람이 몰리는 길에서 조금 벗어나 조용히 숨을 돌리기 좋음",
                "likes": 17,
            },
        ],
        "중구": [
            {
                "id": "jung-001",
                "district": "중구",
                "place_name": "을지로입구 지하보도 연결부",
                "latitude": 37.5661,
                "longitude": 126.9826,
                "place_type": "기다리기 좋은 곳",
                "time_period": ["점심", "저녁"],
                "season": ["겨울", "여름", "사계절"],
                "tags": ["비 피하기 좋음", "기다리기 좋음", "찾기 쉬움"],
                "description": "비 오거나 추울 때 지상으로 바로 나가지 않고 약속 전 10분 기다리기 좋음",
                "likes": 22,
            },
            {
                "id": "jung-002",
                "district": "중구",
                "place_name": "정동길 은행나무 그늘",
                "latitude": 37.5669,
                "longitude": 126.9728,
                "place_type": "계절별 추천 장소",
                "time_period": ["아침", "점심"],
                "season": ["여름", "가을"],
                "tags": ["그늘 있음", "조용함", "산책하기 좋음", "사진 찍기 좋음"],
                "description": "여름에는 그늘이 좋고 가을에는 길 분위기가 좋아 천천히 걷기 좋음",
                "likes": 36,
            },
            {
                "id": "jung-003",
                "district": "중구",
                "place_name": "서울도서관 옆 쉬어가는 벤치",
                "latitude": 37.5664,
                "longitude": 126.9779,
                "place_type": "쉬기 좋은 곳",
                "time_period": ["점심", "저녁"],
                "season": ["봄", "가을", "사계절"],
                "tags": ["햇빛 좋음", "기다리기 좋음", "친구와 가기 좋음"],
                "description": "시청 주변 이동 중 잠깐 앉아 일정을 정리하거나 일행을 기다리기 좋음",
                "likes": 15,
            },
            {
                "id": "jung-004",
                "district": "중구",
                "place_name": "남산골 한옥마을 바깥 산책로",
                "latitude": 37.5593,
                "longitude": 126.9946,
                "place_type": "역사·문화 산책길",
                "time_period": ["아침", "점심", "저녁"],
                "season": ["봄", "가을"],
                "tags": ["조용함", "산책하기 좋음", "사진 찍기 좋음", "사람 덜 붐빔"],
                "description": "관광지 안쪽보다 바깥 산책로가 차분해서 생활 산책 느낌으로 걷기 좋음",
                "likes": 20,
            },
            {
                "id": "jung-005",
                "district": "중구",
                "place_name": "동대문디자인플라자 주변 밝은 보행로",
                "latitude": 37.5668,
                "longitude": 127.0096,
                "place_type": "밤에도 걷기 괜찮은 길",
                "time_period": ["저녁", "밤"],
                "season": ["사계절"],
                "tags": ["찾기 쉬움", "친구와 가기 좋음", "사진 찍기 좋음"],
                "description": "밤에도 주변이 밝고 길 찾기가 쉬워 전시나 약속 뒤 이동하기 괜찮음",
                "likes": 19,
            },
            {
                "id": "jung-006",
                "district": "중구",
                "place_name": "충무로역 근처 편의시설 모임점",
                "latitude": 37.5614,
                "longitude": 126.9940,
                "place_type": "생활 편의 장소",
                "time_period": ["아침", "점심", "저녁"],
                "season": ["사계절"],
                "tags": ["찾기 쉬움", "기다리기 좋음", "친구와 가기 좋음"],
                "description": "지하철 환승 전후로 물을 사거나 일행을 기다리며 동선을 정리하기 좋음",
                "likes": 9,
            },
        ],
    }


COURSES = [
    {
        "district": "종로구",
        "name": "종로 조용한 산책 코스",
        "place_ids": ["jongno-006", "jongno-003", "jongno-001"],
        "description": "북촌과 서촌 골목의 조용한 구간을 지나 청계천으로 내려오는 짧은 생활 산책 코스",
    },
    {
        "district": "종로구",
        "name": "청계천 주변 기다림 코스",
        "place_ids": ["jongno-002", "jongno-001", "jongno-004"],
        "description": "약속 전후로 찾기 쉽고 기다리기 쉬운 장소를 청계천 주변으로 연결한 코스",
    },
    {
        "district": "중구",
        "name": "중구 도심 쉬어가기 코스",
        "place_ids": ["jung-003", "jung-002", "jung-006"],
        "description": "시청과 정동, 충무로 주변에서 잠깐 앉고 걷고 동선을 정리하기 좋은 코스",
    },
    {
        "district": "중구",
        "name": "중구 밤 산책 코스",
        "place_ids": ["jung-001", "jung-005"],
        "description": "지하 이동과 밝은 보행로를 활용해 밤에도 비교적 길 찾기 쉬운 이동 코스",
    },
]


def init_session_state() -> None:
    if "place_folders" not in st.session_state:
        st.session_state.place_folders = base_place_folders()

    defaults = {
        "selected_folder": "종로구",
        "filter_types": [],
        "filter_time": "전체",
        "filter_season": "전체",
        "filter_tags": [],
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


def all_places() -> list[dict]:
    return [place for places in st.session_state.place_folders.values() for place in places]


def folder_places(folder_name: str) -> list[dict]:
    if folder_name == "전체":
        return all_places()
    return st.session_state.place_folders[folder_name]


def folder_dataframe(folder_name: str) -> pd.DataFrame:
    return pd.DataFrame(folder_places(folder_name))


def as_text(value: list[str] | str) -> str:
    if isinstance(value, list):
        return ", ".join(value)
    return str(value)


def apply_preset(types: list[str] | None = None, time: str = "전체", season: str = "전체", tags: list[str] | None = None) -> None:
    st.session_state.filter_types = types or []
    st.session_state.filter_time = time
    st.session_state.filter_season = season
    st.session_state.filter_tags = tags or []


def reset_filters() -> None:
    apply_preset()


def filter_places(df: pd.DataFrame) -> pd.DataFrame:
    filtered = df.copy()

    if st.session_state.filter_types:
        filtered = filtered[filtered["place_type"].isin(st.session_state.filter_types)]

    if st.session_state.filter_time != "전체":
        filtered = filtered[
            filtered["time_period"].apply(lambda values: st.session_state.filter_time in values)
        ]

    if st.session_state.filter_season != "전체":
        filtered = filtered[
            filtered["season"].apply(
                lambda values: st.session_state.filter_season in values or "사계절" in values
            )
        ]

    if st.session_state.filter_tags:
        selected_tags = set(st.session_state.filter_tags)
        filtered = filtered[
            filtered["tags"].apply(lambda values: bool(selected_tags.intersection(values)))
        ]

    return filtered


def type_tone(place_type: str) -> str:
    return TYPE_STYLES.get(place_type, {}).get("tone", "#f4f6f7")


def popup_html(row: pd.Series) -> str:
    return f"""
    <div style="width:260px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;">
        <div style="font-size:12px; color:#2f7d63; font-weight:700;">{row.district} 폴더</div>
        <h4 style="margin:3px 0 8px 0;">{row.place_name}</h4>
        <div style="margin-bottom:6px;"><b>유형</b>: {row.place_type}</div>
        <div><b>추천 시간대</b>: {as_text(row.time_period)}</div>
        <div><b>추천 계절</b>: {as_text(row.season)}</div>
        <div><b>태그</b>: {as_text(row.tags)}</div>
        <div><b>공감</b>: {row.likes}</div>
        <p style="margin:9px 0 0 0; line-height:1.45;">{row.description}</p>
    </div>
    """


def build_map(filtered_df: pd.DataFrame, folder_name: str) -> folium.Map:
    view = MAP_VIEWS[folder_name]
    m = folium.Map(location=view["center"], zoom_start=view["zoom"], tiles="CartoDB positron")

    for _, row in filtered_df.iterrows():
        style = TYPE_STYLES.get(row.place_type, {"color": "gray", "icon": "info"})
        folium.Marker(
            location=[row.latitude, row.longitude],
            tooltip=f"{row.district} | {row.place_name}",
            popup=folium.Popup(popup_html(row), max_width=320),
            icon=folium.Icon(color=style["color"], icon=style["icon"], prefix="fa"),
        ).add_to(m)

    if not filtered_df.empty:
        m.fit_bounds(filtered_df[["latitude", "longitude"]].values.tolist(), padding=(30, 30))

    return m


def render_hero() -> None:
    st.markdown(
        """
        <div class="hero">
            <div class="hero-kicker">PGIS 기반 주민 참여형 생활경험 지도</div>
            <div class="hero-title">동네 사용설명서</div>
            <p class="hero-copy">
                지도에는 없지만 주민은 알고 있는 장소들. 종로구와 중구의 골목, 광장,
                산책길, 기다림의 장소를 시간대와 계절, 상황 중심으로 기록합니다.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar() -> None:
    st.sidebar.header("빠른 추천")
    st.sidebar.button(
        "여름 그늘길 보기",
        use_container_width=True,
        on_click=apply_preset,
        kwargs={"types": ["걷기 좋은 길", "쉬기 좋은 곳", "계절별 추천 장소"], "season": "여름", "tags": ["그늘 있음"]},
    )
    st.sidebar.button(
        "비 오는 날 피하기 좋은 곳 보기",
        use_container_width=True,
        on_click=apply_preset,
        kwargs={"types": ["비 오는 날 피하기 좋은 곳"], "tags": ["비 피하기 좋음"]},
    )
    st.sidebar.button(
        "약속 전 기다리기 좋은 곳 보기",
        use_container_width=True,
        on_click=apply_preset,
        kwargs={"types": ["기다리기 좋은 곳", "만남 장소"], "tags": ["기다리기 좋음", "찾기 쉬움"]},
    )
    st.sidebar.button(
        "혼자 걷기 좋은 길 보기",
        use_container_width=True,
        on_click=apply_preset,
        kwargs={"types": ["걷기 좋은 길", "역사·문화 산책길"], "tags": ["혼자 가기 좋음", "산책하기 좋음"]},
    )
    st.sidebar.button(
        "밤에도 걷기 괜찮은 길 보기",
        use_container_width=True,
        on_click=apply_preset,
        kwargs={"types": ["밤에도 걷기 괜찮은 길"], "time": "밤"},
    )

    st.sidebar.divider()
    st.sidebar.header("폴더 안 필터")
    st.sidebar.multiselect("장소 유형", PLACE_TYPES, key="filter_types")
    st.sidebar.selectbox("시간대", ["전체"] + TIME_PERIODS, key="filter_time")
    st.sidebar.selectbox("계절", ["전체"] + SEASONS, key="filter_season")
    st.sidebar.multiselect("태그", TAGS, key="filter_tags")

    if st.sidebar.button("필터 초기화", use_container_width=True):
        reset_filters()
        st.rerun()


def render_folder_cards() -> None:
    cols = st.columns(3)
    folder_specs = [
        ("전체", "두 구를 한 번에 비교", all_places()),
        ("종로구", "골목과 산책길 중심", st.session_state.place_folders["종로구"]),
        ("중구", "도심 이동과 기다림 중심", st.session_state.place_folders["중구"]),
    ]

    for col, (name, desc, places) in zip(cols, folder_specs):
        type_counter = Counter(place["place_type"] for place in places)
        tag_counter = Counter(tag for place in places for tag in place["tags"])
        with col:
            st.markdown(
                f"""
                <div class="folder-card">
                    <div class="folder-title">{name} 폴더</div>
                    <p class="folder-meta">{desc}</p>
                    <div class="folder-number">{len(places)}곳</div>
                    <p class="folder-meta">주요 유형: {type_counter.most_common(1)[0][0]}</p>
                    <p class="folder-meta">자주 쓰인 태그: {tag_counter.most_common(1)[0][0]}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_summary(filtered_df: pd.DataFrame) -> None:
    tag_counter = Counter(tag for tags in filtered_df["tags"] for tag in tags) if not filtered_df.empty else Counter()
    type_counter = Counter(filtered_df["place_type"]) if not filtered_df.empty else Counter()
    avg_likes = filtered_df["likes"].mean() if not filtered_df.empty else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("표시 장소", f"{len(filtered_df)}곳")
    col2.metric("많은 유형", type_counter.most_common(1)[0][0] if type_counter else "-")
    col3.metric("많은 태그", tag_counter.most_common(1)[0][0] if tag_counter else "-")
    col4.metric("평균 공감", f"{avg_likes:.1f}")


def render_place_cards(filtered_df: pd.DataFrame) -> None:
    if filtered_df.empty:
        st.info("현재 폴더와 필터에 맞는 장소가 없습니다.")
        return

    sorted_df = filtered_df.sort_values(["likes", "place_name"], ascending=[False, True])
    for _, row in sorted_df.iterrows():
        tags_html = "".join(f'<span class="tag">#{tag}</span>' for tag in row.tags)
        st.markdown(
            f"""
            <div class="place-card">
                <div class="place-topline">
                    <p class="place-title">{row.place_name}</p>
                    <span class="place-district">{row.district}</span>
                </div>
                <span class="type-chip" style="background:{type_tone(row.place_type)};">{row.place_type}</span>
                <p class="place-meta">{as_text(row.time_period)} · {as_text(row.season)} · 공감 {row.likes}</p>
                <p class="place-desc">{row.description}</p>
                <div>{tags_html}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_courses(folder_name: str) -> None:
    visible_courses = [course for course in COURSES if folder_name == "전체" or course["district"] == folder_name]
    lookup = {place["id"]: place["place_name"] for place in all_places()}

    cols = st.columns(2)
    for index, course in enumerate(visible_courses):
        with cols[index % 2]:
            with st.container(border=True):
                route = " -> ".join(lookup[place_id] for place_id in course["place_ids"] if place_id in lookup)
                st.markdown(f"**{course['name']}**")
                st.caption(f"{course['district']} 폴더")
                st.write(course["description"])
                st.caption(route)


def render_place_form() -> None:
    default_district = "종로구" if st.session_state.selected_folder == "전체" else st.session_state.selected_folder

    st.subheader("장소 등록")
    st.markdown(
        '<p class="section-note">등록한 장소는 선택한 구의 장소 폴더에 임시 저장됩니다. 일반 리뷰보다 이 장소를 어떤 상황에서 어떻게 사용하는지 적어주세요.</p>',
        unsafe_allow_html=True,
    )

    with st.form("place_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        district = col1.selectbox("저장할 장소 폴더", DISTRICTS, index=DISTRICTS.index(default_district))
        place_name = col2.text_input("장소 이름", placeholder="예: 정동길 은행나무 그늘")

        col3, col4 = st.columns(2)
        latitude = col3.number_input("위도", min_value=37.45, max_value=37.70, value=37.5708, format="%.6f")
        longitude = col4.number_input("경도", min_value=126.85, max_value=127.10, value=126.9911, format="%.6f")

        col5, col6, col7 = st.columns(3)
        place_type = col5.selectbox("장소 유형", PLACE_TYPES)
        time_period = col6.multiselect("추천 시간대", TIME_PERIODS, default=["점심"])
        season = col7.multiselect("추천 계절", SEASONS, default=["사계절"])

        tags = st.multiselect("태그", TAGS, default=["기다리기 좋음"])
        description = st.text_input(
            "한 줄 설명",
            placeholder="예: 을지로에서 약속 전 10분 정도 기다리기 좋음",
        )

        submitted = st.form_submit_button("장소 폴더에 임시 등록")

    if submitted:
        if not place_name or not description or not time_period or not season or not tags:
            st.warning("장소 이름, 시간대, 계절, 태그, 한 줄 설명을 모두 입력해주세요.")
            return

        st.session_state.place_folders[district].append(
            {
                "id": f"{district}-{uuid4().hex[:8]}",
                "district": district,
                "place_name": place_name,
                "latitude": latitude,
                "longitude": longitude,
                "place_type": place_type,
                "time_period": time_period,
                "season": season,
                "tags": tags,
                "description": description,
                "likes": 0,
            }
        )
        st.success(f"{district} 폴더에 장소가 임시 등록되었습니다. 새로고침하면 사라질 수 있습니다.")


def render_principles() -> None:
    with st.expander("개인정보 및 운영 원칙"):
        st.write(
            """
            - 이 서비스는 신고나 비판이 아니라 생활정보 공유를 위한 지도입니다.
            - 사람의 얼굴, 차량번호, 상세 주거지 정보가 드러나는 사진은 올리지 말아주세요.
            - 특정 개인, 상점, 건물에 대한 비방 표현은 제한됩니다.
            - 장소 설명은 긍정적이고 중립적인 생활 팁 중심으로 작성해주세요.
            """
        )


def main() -> None:
    init_session_state()
    inject_style()
    render_sidebar()
    render_hero()
    render_folder_cards()

    st.divider()
    st.radio(
        "장소 폴더 선택",
        FOLDER_OPTIONS,
        key="selected_folder",
        horizontal=True,
        help="선택한 폴더 안의 장소만 지도와 목록에 표시됩니다.",
    )

    folder_name = st.session_state.selected_folder
    folder_df = folder_dataframe(folder_name)
    filtered_df = filter_places(folder_df)

    st.markdown(f"### {folder_name} 폴더")
    st.markdown(
        '<p class="section-note">생활 경험이 기록된 장소를 지도와 카드 목록으로 함께 확인합니다.</p>',
        unsafe_allow_html=True,
    )
    render_summary(filtered_df)

    map_col, list_col = st.columns([1.45, 1], gap="large")
    with map_col:
        st_folium(build_map(filtered_df, folder_name), width=None, height=575)

    with list_col:
        render_place_cards(filtered_df)

    with st.expander("표로 자세히 보기", expanded=False):
        table_df = filtered_df.copy()
        if not table_df.empty:
            table_df["time_period"] = table_df["time_period"].apply(as_text)
            table_df["season"] = table_df["season"].apply(as_text)
            table_df["tags"] = table_df["tags"].apply(as_text)
        st.dataframe(
            table_df[
                [
                    "district",
                    "place_name",
                    "place_type",
                    "time_period",
                    "season",
                    "tags",
                    "description",
                    "likes",
                ]
            ],
            use_container_width=True,
            hide_index=True,
        )

    st.divider()
    st.subheader("추천 코스 예시")
    render_courses(folder_name)

    st.divider()
    render_place_form()

    st.divider()
    render_principles()


if __name__ == "__main__":
    main()
