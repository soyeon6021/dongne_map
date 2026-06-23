from __future__ import annotations

from collections import Counter
from math import atan2, cos, radians, sin, sqrt
from uuid import uuid4

import folium
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium


APP_VERSION = "Railway Sync · 2026-06-23 · food-course-ui"
RAILWAY_URL = "https://web-production-773b0.up.railway.app"


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
    "동네 밥집",
    "간단히 먹기 좋은 곳",
    "혼밥하기 좋은 곳",
    "포장하기 좋은 곳",
    "오래 머물기 좋은 카페",
    "시장 먹거리",
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
    "혼밥하기 좋음",
    "점심에 좋음",
    "저녁에 좋음",
    "간단히 먹기 좋음",
    "포장하기 좋음",
    "비 오는 날 가기 좋음",
    "시장 먹거리",
    "오래 머물기 좋음",
    "길 걷다가 들르기 좋음",
]
COURSE_THEMES = [
    "조용한 산책 코스",
    "여름 그늘 코스",
    "비 오는 날 피하기 코스",
    "약속 전 기다림 코스",
    "밤에도 걷기 괜찮은 코스",
    "역사문화 산책 코스",
    "점심 산책 코스",
    "혼자 보내는 코스",
]

MAP_VIEWS = {
    "전체": {"center": [37.5708, 126.9911], "zoom": 14},
    "종로구": {"center": [37.5758, 126.9862], "zoom": 14},
    "중구": {"center": [37.5628, 126.9944], "zoom": 14},
}

TYPE_STYLES = {
    "쉬기 좋은 곳": {"color": "lightblue", "icon": "pause", "tone": "#eef6ff", "symbol": "pause"},
    "걷기 좋은 길": {"color": "blue", "icon": "road", "tone": "#edf5ff", "symbol": "route"},
    "기다리기 좋은 곳": {"color": "cadetblue", "icon": "clock", "tone": "#f3f7fb", "symbol": "clock"},
    "만남 장소": {"color": "purple", "icon": "star", "tone": "#f4f1ff", "symbol": "pin"},
    "계절별 추천 장소": {"color": "green", "icon": "leaf", "tone": "#f1f8f2", "symbol": "leaf"},
    "생활 편의 장소": {"color": "gray", "icon": "info", "tone": "#f5f6f8", "symbol": "info"},
    "역사·문화 산책길": {"color": "darkred", "icon": "landmark", "tone": "#fff4ef", "symbol": "book"},
    "비 오는 날 피하기 좋은 곳": {"color": "darkblue", "icon": "cloud-rain", "tone": "#eef6fb", "symbol": "rain"},
    "밤에도 걷기 괜찮은 길": {"color": "darkpurple", "icon": "moon", "tone": "#f2f1fb", "symbol": "moon"},
    "동네 밥집": {"color": "beige", "icon": "cutlery", "tone": "#fff7ed", "symbol": "meal"},
    "간단히 먹기 좋은 곳": {"color": "orange", "icon": "bolt", "tone": "#fff7ed", "symbol": "quick"},
    "혼밥하기 좋은 곳": {"color": "lightgray", "icon": "user", "tone": "#f6f7f9", "symbol": "solo"},
    "포장하기 좋은 곳": {"color": "cadetblue", "icon": "shopping-bag", "tone": "#eef7f8", "symbol": "takeout"},
    "오래 머물기 좋은 카페": {"color": "lightblue", "icon": "coffee", "tone": "#f1f7ff", "symbol": "cafe"},
    "시장 먹거리": {"color": "red", "icon": "shopping-basket", "tone": "#fff1f0", "symbol": "market"},
}

SYMBOLS = {
    "pause": "🪑",
    "route": "🚶",
    "clock": "⏳",
    "pin": "🤝",
    "leaf": "🌸",
    "info": "🏪",
    "book": "🏛️",
    "rain": "☔",
    "moon": "🌙",
    "meal": "🍚",
    "quick": "🥪",
    "solo": "🍱",
    "takeout": "🛍️",
    "cafe": "☕",
    "market": "🥟",
}


def inject_style() -> None:
    st.markdown(
        """
        <style>
        :root {
            --ink: #1d1d1f;
            --muted: #6e6e73;
            --faint: #a1a1a6;
            --line: rgba(60, 60, 67, 0.14);
            --panel: rgba(255, 255, 255, 0.76);
            --panel-strong: rgba(255, 255, 255, 0.96);
            --chrome: #f5f5f7;
            --blue: #0066cc;
            --blue-soft: rgba(0, 102, 204, 0.09);
            --shadow: 0 1px 2px rgba(0, 0, 0, 0.04), 0 12px 28px rgba(0, 0, 0, 0.045);
        }

        .stApp {
            background: #f5f5f7;
            color: var(--ink);
            font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Apple SD Gothic Neo", "Segoe UI", sans-serif;
            font-size: 13px;
        }

        section[data-testid="stSidebar"] {
            background: rgba(238, 238, 242, 0.88);
            backdrop-filter: blur(24px) saturate(1.2);
            border-right: 1px solid var(--line);
        }

        section[data-testid="stSidebar"] * {
            font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Apple SD Gothic Neo", "Segoe UI", sans-serif;
        }

        .block-container {
            padding-top: 1rem;
            padding-bottom: 2rem;
            max-width: 1220px;
        }

        h1, h2, h3, p, div, span, label {
            letter-spacing: 0;
        }

        h1, h2, h3 {
            font-weight: 650;
        }

        h2 {
            font-size: 1.05rem !important;
            margin-top: 0.4rem !important;
        }

        h3 {
            font-size: 0.94rem !important;
        }

        button[kind="primary"], div.stButton > button {
            border-radius: 8px;
            border: 1px solid rgba(60, 60, 67, 0.12);
            box-shadow: none;
            transition: all 0.16s ease;
            min-height: 30px;
            font-size: 0.78rem;
        }

        div.stButton > button:hover {
            border-color: rgba(0, 122, 255, 0.35);
            transform: translateY(-1px);
        }

        div[data-testid="stMetric"] {
            background: var(--panel-strong);
            backdrop-filter: blur(14px);
            border: 1px solid var(--line);
            border-radius: 10px;
            padding: 8px 10px;
            box-shadow: none;
        }

        div[data-testid="stMetricValue"] {
            color: #111827;
            font-size: 1.02rem;
            font-weight: 620;
        }

        div[data-testid="stMetricLabel"] {
            font-size: 0.7rem;
        }

        div[data-testid="stSelectbox"] label,
        div[data-testid="stMultiSelect"] label,
        div[data-testid="stSlider"] label,
        div[data-testid="stTextInput"] label,
        div[data-testid="stNumberInput"] label,
        div[data-testid="stRadio"] label {
            font-size: 0.72rem;
            color: var(--muted);
        }

        div[data-baseweb="select"] > div,
        div[data-baseweb="input"] > div {
            border-radius: 8px;
            border-color: rgba(0, 0, 0, 0.10);
            background: rgba(255, 255, 255, 0.86);
            min-height: 30px;
            font-size: 0.78rem;
        }

        div[data-testid="stMarkdownContainer"] p,
        div[data-testid="stCaptionContainer"] {
            font-size: 0.78rem;
        }

        .hero {
            position: relative;
            overflow: hidden;
            border: 1px solid var(--line);
            background: rgba(255, 255, 255, 0.78);
            backdrop-filter: blur(22px) saturate(1.1);
            border-radius: 14px;
            padding: 12px 14px 12px 58px;
            margin-bottom: 10px;
            box-shadow: var(--shadow);
        }

        .hero::after {
            content: "";
            position: absolute;
            left: 14px;
            top: 14px;
            width: 32px;
            height: 32px;
            border-radius: 9px;
            border: 1px solid rgba(60, 60, 67, 0.12);
            background: linear-gradient(180deg, #ffffff 0%, #f2f2f7 100%);
            box-shadow: none;
        }

        .hero-symbol {
            position: absolute;
            left: 21px;
            top: 19px;
            z-index: 2;
            color: var(--blue);
            font-size: 1.05rem;
            font-weight: 620;
        }

        .hero-kicker {
            color: var(--blue);
            font-weight: 600;
            font-size: 0.68rem;
            margin-bottom: 2px;
        }

        .hero-title {
            color: var(--ink);
            font-size: 1.08rem;
            font-weight: 650;
            line-height: 1.22;
            margin: 0 0 3px 0;
        }

        .hero-copy {
            color: var(--muted);
            font-size: 0.78rem;
            line-height: 1.45;
            max-width: 760px;
            margin: 0;
        }

        .sync-pill {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            border: 1px solid rgba(0, 102, 204, 0.16);
            background: rgba(0, 102, 204, 0.07);
            color: var(--blue);
            border-radius: 999px;
            padding: 3px 8px;
            margin-top: 8px;
            font-size: 0.66rem;
            font-weight: 600;
        }

        .folder-card {
            position: relative;
            border: 1px solid var(--line);
            background: rgba(255, 255, 255, 0.80);
            backdrop-filter: blur(12px);
            border-radius: 12px;
            padding: 10px;
            min-height: 102px;
            box-shadow: var(--shadow);
        }

        .folder-icon {
            width: 24px;
            height: 24px;
            border-radius: 8px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(180deg, #ffffff 0%, #f2f2f7 100%);
            border: 1px solid var(--line);
            color: #3a3a3c;
            font-size: 0.86rem;
            font-weight: 620;
            margin-bottom: 7px;
        }

        .folder-title {
            font-size: 0.82rem;
            font-weight: 620;
            margin: 0 0 4px 0;
        }

        .folder-meta {
            color: var(--muted);
            font-size: 0.68rem;
            line-height: 1.36;
            margin: 0;
        }

        .folder-number {
            font-size: 1.02rem;
            font-weight: 620;
            color: var(--ink);
            margin: 3px 0;
        }

        .place-card {
            border: 1px solid var(--line);
            background: var(--panel-strong);
            backdrop-filter: blur(12px);
            border-radius: 12px;
            padding: 10px;
            margin-bottom: 8px;
            box-shadow: none;
        }

        .place-card:hover {
            border-color: rgba(0, 122, 255, 0.22);
            background: #ffffff;
        }

        .place-topline {
            display: flex;
            justify-content: space-between;
            gap: 12px;
            align-items: flex-start;
        }

        .place-title {
            font-weight: 650;
            font-size: 0.82rem;
            margin: 0;
        }

        .place-district {
            color: var(--blue);
            font-size: 0.66rem;
            font-weight: 600;
            white-space: nowrap;
        }

        .place-meta {
            color: var(--muted);
            font-size: 0.68rem;
            margin: 4px 0 6px 0;
            line-height: 1.45;
        }

        .place-desc {
            color: #374151;
            font-size: 0.74rem;
            line-height: 1.42;
            margin: 0 0 7px 0;
        }

        .tag {
            display: inline-block;
            border: 1px solid rgba(0, 122, 255, 0.10);
            background: rgba(0, 122, 255, 0.055);
            border-radius: 999px;
            padding: 2px 6px;
            margin: 0 2px 3px 0;
            color: #1f5f99;
            font-size: 0.64rem;
        }

        .type-chip {
            display: inline-flex;
            align-items: center;
            gap: 5px;
            border-radius: 999px;
            padding: 3px 7px;
            font-weight: 600;
            font-size: 0.65rem;
            color: #25302c;
            margin-bottom: 5px;
        }

        .section-note {
            color: var(--muted);
            font-size: 0.72rem;
            line-height: 1.5;
            margin-top: -4px;
            margin-bottom: 8px;
        }

        .course-box {
            border: 1px solid var(--line);
            background: var(--panel-strong);
            backdrop-filter: blur(12px);
            border-radius: 12px;
            padding: 10px;
            margin-bottom: 8px;
            box-shadow: none;
        }

        .course-title {
            font-size: 0.86rem;
            font-weight: 620;
            margin: 0 0 5px 0;
        }

        .course-desc {
            color: #3d464d;
            font-size: 0.72rem;
            line-height: 1.42;
            margin: 0 0 8px 0;
        }

        .course-step {
            border: 1px solid rgba(0, 122, 255, 0.09);
            border-radius: 9px;
            padding: 7px 8px;
            margin-bottom: 5px;
            background: rgba(247, 250, 255, 0.80);
            font-size: 0.72rem;
        }

        .course-step b {
            color: var(--blue);
        }

        .soft-icon {
            width: 18px;
            height: 18px;
            border-radius: 6px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            background: rgba(0, 122, 255, 0.10);
            color: var(--blue);
            font-size: 0.78rem;
            font-weight: 620;
        }

        iframe {
            border-radius: 12px !important;
            border: 1px solid var(--line) !important;
            box-shadow: var(--shadow);
        }

        div[data-testid="stDataFrame"] {
            border-radius: 16px;
            overflow: hidden;
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
            {
                "id": "jongno-007",
                "district": "종로구",
                "place_name": "정독도서관 주변 낮은 담장길",
                "latitude": 37.5811,
                "longitude": 126.9837,
                "place_type": "역사·문화 산책길",
                "time_period": ["아침", "점심"],
                "season": ["봄", "가을"],
                "tags": ["조용함", "산책하기 좋음", "사진 찍기 좋음", "사람 덜 붐빔"],
                "description": "도서관 주변 담장과 나무 사이를 따라 조용히 걷기 좋은 생활 산책 구간",
                "likes": 21,
            },
            {
                "id": "jongno-008",
                "district": "종로구",
                "place_name": "안국역 지하 연결 통로",
                "latitude": 37.5766,
                "longitude": 126.9855,
                "place_type": "기다리기 좋은 곳",
                "time_period": ["점심", "저녁"],
                "season": ["여름", "겨울", "사계절"],
                "tags": ["비 피하기 좋음", "기다리기 좋음", "찾기 쉬움"],
                "description": "비가 오거나 추울 때 지상으로 바로 나가지 않고 약속 시간을 맞추기 좋음",
                "likes": 16,
            },
            {
                "id": "jongno-009",
                "district": "종로구",
                "place_name": "삼청동 초입 처마 아래",
                "latitude": 37.5797,
                "longitude": 126.9819,
                "place_type": "비 오는 날 피하기 좋은 곳",
                "time_period": ["점심", "저녁"],
                "season": ["여름", "사계절"],
                "tags": ["비 피하기 좋음", "기다리기 좋음", "조용함"],
                "description": "골목으로 들어가기 전 비를 피하며 일행과 동선을 정리하기 좋은 지점",
                "likes": 14,
            },
            {
                "id": "jongno-010",
                "district": "종로구",
                "place_name": "대학로 밝은 보행길",
                "latitude": 37.5818,
                "longitude": 127.0022,
                "place_type": "밤에도 걷기 괜찮은 길",
                "time_period": ["저녁", "밤"],
                "season": ["사계절"],
                "tags": ["산책하기 좋음", "찾기 쉬움", "친구와 가기 좋음"],
                "description": "저녁에도 주변이 밝고 길 찾기가 쉬워 공연 전후 짧게 이동하기 괜찮음",
                "likes": 18,
            },
            {
                "id": "jongno-011",
                "district": "종로구",
                "place_name": "이화동 초입 밝은 골목길",
                "latitude": 37.5794,
                "longitude": 127.0054,
                "place_type": "밤에도 걷기 괜찮은 길",
                "time_period": ["저녁", "밤"],
                "season": ["사계절"],
                "tags": ["산책하기 좋음", "혼자 가기 좋음", "찾기 쉬움"],
                "description": "낙산과 대학로 사이에서 저녁에도 비교적 밝게 이어지는 짧은 보행 구간",
                "likes": 15,
            },
            {
                "id": "jongno-012",
                "district": "종로구",
                "place_name": "북촌 생활문화 골목길",
                "latitude": 37.5804,
                "longitude": 126.9864,
                "place_type": "역사·문화 산책길",
                "time_period": ["아침", "점심"],
                "season": ["봄", "가을"],
                "tags": ["조용함", "산책하기 좋음", "사진 찍기 좋음", "사람 덜 붐빔"],
                "description": "관광 동선에서 살짝 벗어나 오래된 골목 분위기를 조용히 읽으며 걷기 좋음",
                "likes": 19,
            },
            {
                "id": "jongno-food-001",
                "district": "종로구",
                "place_name": "안국역 골목 동네 밥집",
                "latitude": 37.5769,
                "longitude": 126.9851,
                "place_type": "동네 밥집",
                "time_period": ["점심", "저녁"],
                "season": ["사계절"],
                "tags": ["점심에 좋음", "혼밥하기 좋음", "길 걷다가 들르기 좋음"],
                "description": "안국역 주변에서 점심시간에 빠르게 한 끼 해결하기 좋은 생활 식사 장소",
                "likes": 18,
            },
            {
                "id": "jongno-food-002",
                "district": "종로구",
                "place_name": "서촌 작은 포장 식사점",
                "latitude": 37.5784,
                "longitude": 126.9715,
                "place_type": "포장하기 좋은 곳",
                "time_period": ["점심", "저녁"],
                "season": ["사계절"],
                "tags": ["포장하기 좋음", "간단히 먹기 좋음", "점심에 좋음"],
                "description": "서촌을 걷다가 오래 머물지 않고 포장해 이동하기 좋은 골목 식사점",
                "likes": 13,
            },
            {
                "id": "jongno-food-003",
                "district": "종로구",
                "place_name": "광장시장 간단 먹거리 골목",
                "latitude": 37.5701,
                "longitude": 126.9996,
                "place_type": "시장 먹거리",
                "time_period": ["점심", "저녁"],
                "season": ["사계절"],
                "tags": ["시장 먹거리", "간단히 먹기 좋음", "친구와 가기 좋음"],
                "description": "시장 주변을 걷다가 짧게 들러 간단히 먹고 다시 이동하기 좋은 먹거리 구간",
                "likes": 22,
            },
            {
                "id": "jongno-food-004",
                "district": "종로구",
                "place_name": "대학로 조용한 머무름 카페",
                "latitude": 37.5812,
                "longitude": 127.0028,
                "place_type": "오래 머물기 좋은 카페",
                "time_period": ["점심", "저녁"],
                "season": ["사계절"],
                "tags": ["오래 머물기 좋음", "비 오는 날 가기 좋음", "혼자 가기 좋음"],
                "description": "비 오는 날 공연 전후로 잠깐 쉬거나 혼자 시간을 보내기 좋은 카페",
                "likes": 16,
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
            {
                "id": "jung-007",
                "district": "중구",
                "place_name": "덕수궁 돌담길 그늘 구간",
                "latitude": 37.5662,
                "longitude": 126.9751,
                "place_type": "역사·문화 산책길",
                "time_period": ["아침", "점심"],
                "season": ["여름", "가을"],
                "tags": ["그늘 있음", "조용함", "산책하기 좋음", "사진 찍기 좋음"],
                "description": "점심 무렵 짧게 걷기 좋고, 담장 옆 그늘이 생겨 잠깐 속도를 늦추기 좋음",
                "likes": 27,
            },
            {
                "id": "jung-008",
                "district": "중구",
                "place_name": "시청역 지하 연결 대기 지점",
                "latitude": 37.5659,
                "longitude": 126.9766,
                "place_type": "기다리기 좋은 곳",
                "time_period": ["점심", "저녁"],
                "season": ["여름", "겨울", "사계절"],
                "tags": ["비 피하기 좋음", "기다리기 좋음", "찾기 쉬움"],
                "description": "날씨가 좋지 않을 때 지하에서 약속 시간을 맞추고 이동 방향을 정하기 좋음",
                "likes": 18,
            },
            {
                "id": "jung-009",
                "district": "중구",
                "place_name": "을지로입구 밝은 보행 연결길",
                "latitude": 37.5652,
                "longitude": 126.9851,
                "place_type": "밤에도 걷기 괜찮은 길",
                "time_period": ["저녁", "밤"],
                "season": ["사계절"],
                "tags": ["찾기 쉬움", "산책하기 좋음", "친구와 가기 좋음"],
                "description": "저녁 약속 뒤 지하철역까지 밝은 길을 따라 이동하기 괜찮은 생활 보행 구간",
                "likes": 17,
            },
            {
                "id": "jung-010",
                "district": "중구",
                "place_name": "청계천 을지로입구 그늘 계단",
                "latitude": 37.5683,
                "longitude": 126.9841,
                "place_type": "쉬기 좋은 곳",
                "time_period": ["점심", "저녁"],
                "season": ["여름", "가을"],
                "tags": ["그늘 있음", "산책하기 좋음", "기다리기 좋음"],
                "description": "청계천으로 내려가기 전 그늘에서 잠깐 쉬거나 일행을 기다리기 좋음",
                "likes": 20,
            },
            {
                "id": "jung-011",
                "district": "중구",
                "place_name": "명동역 지하 입구 대기 지점",
                "latitude": 37.5609,
                "longitude": 126.9864,
                "place_type": "비 오는 날 피하기 좋은 곳",
                "time_period": ["점심", "저녁"],
                "season": ["여름", "겨울", "사계절"],
                "tags": ["비 피하기 좋음", "기다리기 좋음", "찾기 쉬움"],
                "description": "비 오는 날 지상 혼잡을 피해 잠깐 일행을 기다리고 이동 방향을 정하기 좋음",
                "likes": 16,
            },
            {
                "id": "jung-food-001",
                "district": "중구",
                "place_name": "을지로 골목 혼밥 식사점",
                "latitude": 37.5654,
                "longitude": 126.9893,
                "place_type": "혼밥하기 좋은 곳",
                "time_period": ["점심", "저녁"],
                "season": ["사계절"],
                "tags": ["혼밥하기 좋음", "점심에 좋음", "간단히 먹기 좋음"],
                "description": "을지로 산책이나 업무 이동 중 혼자 들어가기 부담 없는 식사 장소",
                "likes": 19,
            },
            {
                "id": "jung-food-002",
                "district": "중구",
                "place_name": "충무로 빠른 점심 밥집",
                "latitude": 37.5618,
                "longitude": 126.9932,
                "place_type": "간단히 먹기 좋은 곳",
                "time_period": ["점심"],
                "season": ["사계절"],
                "tags": ["점심에 좋음", "간단히 먹기 좋음", "길 걷다가 들르기 좋음"],
                "description": "점심시간에 오래 앉지 않고 빠르게 한 끼 해결하기 좋은 생활 식사 지점",
                "likes": 14,
            },
            {
                "id": "jung-food-003",
                "district": "중구",
                "place_name": "남대문시장 간단 먹거리 줄",
                "latitude": 37.5597,
                "longitude": 126.9770,
                "place_type": "시장 먹거리",
                "time_period": ["점심", "저녁"],
                "season": ["사계절"],
                "tags": ["시장 먹거리", "간단히 먹기 좋음", "친구와 가기 좋음"],
                "description": "시장 동선 중 짧게 멈춰 먹고 다시 걷기 좋은 생활 먹거리 구간",
                "likes": 21,
            },
            {
                "id": "jung-food-004",
                "district": "중구",
                "place_name": "시청 주변 오래 머무는 카페",
                "latitude": 37.5655,
                "longitude": 126.9785,
                "place_type": "오래 머물기 좋은 카페",
                "time_period": ["점심", "저녁"],
                "season": ["사계절"],
                "tags": ["오래 머물기 좋음", "비 오는 날 가기 좋음", "기다리기 좋음"],
                "description": "비 오는 날 이동 전후로 앉아서 일정을 정리하거나 일행을 기다리기 좋은 카페",
                "likes": 17,
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
        "course_district": "종로구",
        "course_theme": "조용한 산책 코스",
        "generated_course": None,
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


def type_symbol(place_type: str) -> str:
    symbol_key = TYPE_STYLES.get(place_type, {}).get("symbol", "info")
    return SYMBOLS.get(symbol_key, "i")


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


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """위도·경도 두 지점 사이의 대략적인 거리(km)를 계산합니다."""
    earth_radius_km = 6371.0
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = (
        sin(dlat / 2) ** 2
        + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    )
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return earth_radius_km * c


def score_place_for_theme(row: pd.Series, theme: str) -> int:
    tags = set(row["tags"])
    seasons = set(row["season"])
    times = set(row["time_period"])
    place_type = row["place_type"]
    score = 0

    if theme == "조용한 산책 코스":
        score += 3 if place_type == "걷기 좋은 길" else 0
        score += 2 if "조용함" in tags else 0
        score += 2 if "산책하기 좋음" in tags else 0
        score += 1 if "사람 덜 붐빔" in tags else 0
    elif theme == "여름 그늘 코스":
        score += 2 if seasons.intersection({"여름", "사계절"}) else 0
        score += 3 if "그늘 있음" in tags else 0
        score += 2 if place_type in {"쉬기 좋은 곳", "걷기 좋은 길"} else 0
    elif theme == "비 오는 날 피하기 코스":
        score += 3 if place_type == "비 오는 날 피하기 좋은 곳" else 0
        score += 3 if "비 피하기 좋음" in tags else 0
        score += 2 if "비 오는 날 가기 좋음" in tags else 0
        score += 1 if place_type == "기다리기 좋은 곳" else 0
        score += 1 if place_type in {"동네 밥집", "오래 머물기 좋은 카페"} else 0
    elif theme == "약속 전 기다림 코스":
        score += 3 if place_type == "기다리기 좋은 곳" else 0
        score += 2 if place_type == "만남 장소" else 0
        score += 3 if "기다리기 좋음" in tags else 0
        score += 1 if "찾기 쉬움" in tags else 0
    elif theme == "밤에도 걷기 괜찮은 코스":
        score += 3 if place_type == "밤에도 걷기 괜찮은 길" else 0
        score += 2 if times.intersection({"밤", "저녁"}) else 0
        score += 1 if "산책하기 좋음" in tags else 0
    elif theme == "역사문화 산책 코스":
        score += 3 if place_type == "역사·문화 산책길" else 0
        score += 1 if "사진 찍기 좋음" in tags else 0
        score += 2 if "산책하기 좋음" in tags else 0
    elif theme == "점심 산책 코스":
        score += 3 if place_type == "동네 밥집" else 0
        score += 2 if place_type in {"걷기 좋은 길", "쉬기 좋은 곳", "간단히 먹기 좋은 곳"} else 0
        score += 2 if "점심에 좋음" in tags else 0
        score += 1 if "길 걷다가 들르기 좋음" in tags else 0
        score += 1 if "산책하기 좋음" in tags else 0
    elif theme == "혼자 보내는 코스":
        score += 3 if place_type == "혼밥하기 좋은 곳" else 0
        score += 2 if place_type in {"걷기 좋은 길", "쉬기 좋은 곳", "오래 머물기 좋은 카페"} else 0
        score += 2 if tags.intersection({"혼밥하기 좋음", "혼자 가기 좋음"}) else 0
        score += 1 if "조용함" in tags else 0
        score += 1 if "오래 머물기 좋음" in tags else 0

    return score


def order_places_by_nearest_neighbor(
    candidate_df: pd.DataFrame,
    max_stops: int = 4,
    max_leg_km: float = 1.2,
) -> tuple[pd.DataFrame, str | None]:
    if candidate_df.empty:
        return candidate_df, "선택한 조건에 맞는 장소가 부족합니다. 필터를 완화하거나 장소를 더 등록해주세요."

    remaining = candidate_df.sort_values("final_score", ascending=False).to_dict("records")
    ordered = [remaining.pop(0)]

    while remaining and len(ordered) < max_stops:
        current = ordered[-1]
        nearest_index = None
        nearest_distance = None

        for index, place in enumerate(remaining):
            distance = haversine_distance(
                current["latitude"],
                current["longitude"],
                place["latitude"],
                place["longitude"],
            )
            if nearest_distance is None or distance < nearest_distance:
                nearest_index = index
                nearest_distance = distance

        if nearest_index is None or nearest_distance is None or nearest_distance > max_leg_km:
            break

        next_place = remaining.pop(nearest_index)
        next_place["distance_from_previous_km"] = nearest_distance
        ordered.append(next_place)

    if len(ordered) < 3:
        return pd.DataFrame(ordered), "선택한 장소들이 서로 멀리 떨어져 있어 걷기 코스로 연결하기 어렵습니다."

    return pd.DataFrame(ordered), None


def generate_course(
    df: pd.DataFrame,
    district: str,
    theme: str,
    max_stops: int = 4,
) -> dict:
    df_course = df[df["district"] == district].copy()
    if len(df_course) < 3:
        return {
            "ok": False,
            "message": "선택한 조건에 맞는 장소가 부족합니다. 필터를 완화하거나 장소를 더 등록해주세요.",
            "course_df": pd.DataFrame(),
        }

    df_course["theme_score"] = df_course.apply(lambda row: score_place_for_theme(row, theme), axis=1)
    df_course = df_course[df_course["theme_score"] > 0].copy()

    if len(df_course) < 3:
        return {
            "ok": False,
            "message": "선택한 조건에 맞는 장소가 부족합니다. 필터를 완화하거나 장소를 더 등록해주세요.",
            "course_df": df_course,
        }

    df_course["final_score"] = df_course["theme_score"] + df_course["likes"].clip(upper=5) * 0.2
    candidates = df_course.sort_values("final_score", ascending=False).head(8)
    course_df, error = order_places_by_nearest_neighbor(candidates, max_stops=max_stops)

    if error:
        return {"ok": False, "message": error, "course_df": course_df}

    course_df = course_df.reset_index(drop=True)
    course_df["course_order"] = course_df.index + 1
    description = build_course_description(course_df, district, theme)

    return {
        "ok": True,
        "message": "",
        "name": f"{district} {theme}",
        "description": description,
        "course_df": course_df,
    }


def build_course_description(course_df: pd.DataFrame, district: str, theme: str) -> str:
    tag_counter = Counter(tag for tags in course_df["tags"] for tag in tags)
    major_tags = [tag for tag, _ in tag_counter.most_common(3)]
    tag_text = ", ".join(major_tags) if major_tags else "생활경험"
    place_count = len(course_df)

    return (
        f"이 코스는 {district} 안에서 '{theme}'에 어울리는 장소 {place_count}곳을 골라 구성했습니다. "
        f"주요 태그는 {tag_text}이며, 테마 점수와 공감 수를 함께 반영했습니다. "
        "선정된 장소는 위도·경도 기준으로 비교적 가까운 순서대로 연결해, "
        "짧게 걸으며 동네의 쉬기 좋은 곳, 걷기 좋은 길, 기다리기 좋은 장소를 경험할 수 있도록 만들었습니다."
    )


def draw_course_on_map(m: folium.Map, course_df: pd.DataFrame) -> folium.Map:
    if course_df.empty:
        return m

    coordinates = course_df[["latitude", "longitude"]].values.tolist()
    popup_text = " -> ".join(course_df["place_name"].tolist())

    folium.PolyLine(
        locations=coordinates,
        color="#007aff",
        weight=5,
        opacity=0.86,
        popup=folium.Popup(popup_text, max_width=360),
    ).add_to(m)

    for _, row in course_df.iterrows():
        folium.Marker(
            location=[row.latitude, row.longitude],
            tooltip=f"{int(row.course_order)}. {row.place_name}",
            popup=folium.Popup(popup_html(row), max_width=320),
            icon=folium.DivIcon(
                html=f"""
                <div style="
                    width:30px;height:30px;border-radius:50%;
                    background:#007aff;color:white;border:3px solid white;
                    box-shadow:0 8px 18px rgba(0,122,255,.28);
                    display:flex;align-items:center;justify-content:center;
                    font-weight:800;font-size:14px;">
                    {int(row.course_order)}
                </div>
                """
            ),
        ).add_to(m)

    m.fit_bounds(coordinates, padding=(34, 34))
    return m


def build_course_map(course_df: pd.DataFrame, district: str) -> folium.Map:
    m = folium.Map(
        location=MAP_VIEWS[district]["center"],
        zoom_start=MAP_VIEWS[district]["zoom"],
        tiles="CartoDB positron",
    )
    return draw_course_on_map(m, course_df)


def render_hero() -> None:
    st.markdown(
        f"""
        <div class="hero">
            <div class="hero-symbol">🗺️</div>
            <div class="hero-kicker">주민 참여형 생활경험 지도</div>
            <div class="hero-title">동네 사용설명서</div>
            <p class="hero-copy">
                지도에는 없지만 주민은 알고 있는 장소들. 종로구와 중구의 골목, 광장,
                산책길, 기다림의 장소, 상황별 식사 장소를 시간대와 계절 중심으로 기록합니다.
            </p>
            <div class="sync-pill">● {APP_VERSION}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar() -> None:
    st.sidebar.caption(f"배포 확인: {APP_VERSION}")
    st.sidebar.caption(RAILWAY_URL)
    st.sidebar.divider()
    st.sidebar.header("Quick Views")
    st.sidebar.button(
        "🌳 여름 그늘길",
        use_container_width=True,
        on_click=apply_preset,
        kwargs={"types": ["걷기 좋은 길", "쉬기 좋은 곳", "계절별 추천 장소"], "season": "여름", "tags": ["그늘 있음"]},
    )
    st.sidebar.button(
        "☔ 비 오는 날",
        use_container_width=True,
        on_click=apply_preset,
        kwargs={"types": ["비 오는 날 피하기 좋은 곳"], "tags": ["비 피하기 좋음"]},
    )
    st.sidebar.button(
        "⏳ 약속 전 기다림",
        use_container_width=True,
        on_click=apply_preset,
        kwargs={"types": ["기다리기 좋은 곳", "만남 장소"], "tags": ["기다리기 좋음", "찾기 쉬움"]},
    )
    st.sidebar.button(
        "🚶 혼자 걷기",
        use_container_width=True,
        on_click=apply_preset,
        kwargs={"types": ["걷기 좋은 길", "역사·문화 산책길"], "tags": ["혼자 가기 좋음", "산책하기 좋음"]},
    )
    st.sidebar.button(
        "🌙 밤 산책",
        use_container_width=True,
        on_click=apply_preset,
        kwargs={"types": ["밤에도 걷기 괜찮은 길"], "time": "밤"},
    )
    st.sidebar.button(
        "🍚 점심 산책",
        use_container_width=True,
        on_click=apply_preset,
        kwargs={"types": ["걷기 좋은 길", "동네 밥집", "간단히 먹기 좋은 곳", "쉬기 좋은 곳"], "time": "점심", "tags": ["점심에 좋음", "길 걷다가 들르기 좋음"]},
    )
    st.sidebar.button(
        "🍱 혼자 보내기",
        use_container_width=True,
        on_click=apply_preset,
        kwargs={"types": ["혼밥하기 좋은 곳", "오래 머물기 좋은 카페", "쉬기 좋은 곳"], "tags": ["혼밥하기 좋음", "혼자 가기 좋음", "오래 머물기 좋음"]},
    )

    st.sidebar.divider()
    st.sidebar.header("Filters")
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
        ("전체", "🗂️", "두 구를 한 번에 비교", all_places()),
        ("종로구", "🚶", "골목과 산책길 중심", st.session_state.place_folders["종로구"]),
        ("중구", "⏳", "도심 이동과 기다림 중심", st.session_state.place_folders["중구"]),
    ]

    for col, (name, icon, desc, places) in zip(cols, folder_specs):
        type_counter = Counter(place["place_type"] for place in places)
        tag_counter = Counter(tag for place in places for tag in place["tags"])
        with col:
            st.markdown(
                f"""
                <div class="folder-card">
                    <div class="folder-icon">{icon}</div>
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
        symbol = type_symbol(row.place_type)
        st.markdown(
            f"""
            <div class="place-card">
                <div class="place-topline">
                    <p class="place-title">{row.place_name}</p>
                    <span class="place-district">{row.district}</span>
                </div>
                <span class="type-chip" style="background:{type_tone(row.place_type)};"><span class="soft-icon">{symbol}</span>{row.place_type}</span>
                <p class="place-meta">{as_text(row.time_period)} · {as_text(row.season)} · 공감 {row.likes}</p>
                <p class="place-desc">{row.description}</p>
                <div>{tags_html}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_course_generator() -> None:
    st.subheader("추천 코스 자동 생성")
    st.markdown(
        '<p class="section-note">같은 구 안의 장소만 사용해 주민 생활경험 기반 코스를 만듭니다. 실제 도보 경로 대신 가까운 장소 순서대로 연결합니다.</p>',
        unsafe_allow_html=True,
    )

    control_col, result_col = st.columns([0.9, 1.4], gap="large")

    with control_col:
        with st.container(border=True):
            st.selectbox("코스 지역 선택", DISTRICTS, key="course_district")
            st.selectbox("코스 테마 선택", COURSE_THEMES, key="course_theme")
            max_stops = st.slider("코스 장소 수", min_value=3, max_value=5, value=4)
            if st.button("코스 생성", type="primary", use_container_width=True):
                all_df = pd.DataFrame(all_places())
                st.session_state.generated_course = generate_course(
                    all_df,
                    st.session_state.course_district,
                    st.session_state.course_theme,
                    max_stops=max_stops,
                )

            st.caption("장소 간 거리가 1.2km 이상이면 걷기 코스로 연결하지 않습니다.")

    with result_col:
        result = st.session_state.generated_course
        if result is None:
            st.info("코스 지역과 테마를 선택한 뒤 코스를 생성해보세요.")
            return

        if not result["ok"]:
            st.warning(result["message"])
            if not result["course_df"].empty:
                st.caption("점수 후보는 있었지만 가까운 순서로 3곳 이상 연결되지 않았습니다.")
            return

        course_df = result["course_df"]
        steps_html = ""
        for _, row in course_df.iterrows():
            distance_text = ""
            if row.get("distance_from_previous_km") and not pd.isna(row.get("distance_from_previous_km")):
                distance_text = f" · 이전 장소에서 약 {row.distance_from_previous_km:.2f}km"
            symbol = type_symbol(row.place_type)
            steps_html += (
                f'<div class="course-step"><b>{int(row.course_order)}.</b> '
                f'<span class="soft-icon">{symbol}</span> {row.place_name}'
                f'<br><span class="place-meta">{row.place_type} · {as_text(row.tags)}{distance_text}</span></div>'
            )

        st.markdown(
            f"""
            <div class="course-box">
                <p class="course-title">{result["name"]}</p>
                <p class="course-desc">{result["description"]}</p>
                {steps_html}
            </div>
            """,
            unsafe_allow_html=True,
        )

        st_folium(
            build_course_map(course_df, st.session_state.course_district),
            width=None,
            height=430,
        )


def render_place_form() -> None:
    default_district = "종로구" if st.session_state.selected_folder == "전체" else st.session_state.selected_folder

    st.subheader("장소 등록")
    st.markdown(
        '<p class="section-note">별점이나 평가보다 이 장소를 어떤 상황에서 어떻게 쓰는지 기록합니다. 음식점도 맛집 순위가 아니라 생활 동선 안의 식사 장소로 다룹니다.</p>',
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
        time_period = col6.multiselect("추천 시간대는 언제인가요?", TIME_PERIODS, default=["점심"])
        season = col7.multiselect("추천 계절", SEASONS, default=["사계절"])

        tags = st.multiselect(
            "혼자 가기 좋은가요, 친구와 가기 좋은가요? 간단히 먹기 좋은가요, 오래 머물기 좋은가요?",
            TAGS,
            default=["길 걷다가 들르기 좋음"],
        )
        description = st.text_input(
            "이 장소는 어떤 상황에서 이용하기 좋은가요? 한 줄 사용법을 적어주세요.",
            placeholder="예: 점심시간에 빠르게 한 끼 해결하기 좋은 곳",
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
    render_course_generator()

    st.divider()
    render_place_form()

    st.divider()
    render_principles()


if __name__ == "__main__":
    main()
