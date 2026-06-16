from __future__ import annotations

from copy import deepcopy
from datetime import date
from math import cos, radians, sqrt
from uuid import uuid4

import folium
import streamlit as st
from streamlit_folium import st_folium


st.set_page_config(
    page_title="동네 사용설명서",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded",
)


PLACE_TYPES = {
    "rest": {"label": "쉬기 좋은 곳", "emoji": "🪑", "color": "#22c55e"},
    "walk": {"label": "걷기 좋은 길", "emoji": "🚶", "color": "#3b82f6"},
    "wait": {"label": "기다리기 좋은 곳", "emoji": "⏳", "color": "#f59e0b"},
    "meet": {"label": "만남 장소", "emoji": "🤝", "color": "#ec4899"},
    "season": {"label": "계절별 추천", "emoji": "🌸", "color": "#f97316"},
    "life": {"label": "생활 편의", "emoji": "🏪", "color": "#8b5cf6"},
}

TIME_LABELS = {
    "morning": "아침",
    "lunch": "점심",
    "evening": "저녁",
    "night": "밤",
}

SEASON_LABELS = {
    "spring": "봄",
    "summer": "여름",
    "fall": "가을",
    "winter": "겨울",
    "all": "사계절",
}

TAG_GROUPS = {
    "분위기": ["조용함", "활기 있음", "여유로움", "편안함", "감성적임"],
    "환경": ["그늘 있음", "햇빛 좋음", "바람 잘 통함", "전망 좋음", "나무 많음"],
    "이용": ["혼자 가기 좋음", "친구와 가기 좋음", "가족과 가기 좋음", "기다리기 좋음"],
    "활동": ["산책하기 좋음", "공부하기 좋음", "사진 찍기 좋음", "잠깐 쉬기 좋음"],
    "날씨": ["봄에 좋음", "여름에 좋음", "비 피하기 좋음", "겨울 햇볕 좋음"],
}

ALL_TAGS = [tag for tags in TAG_GROUPS.values() for tag in tags]

SEOUL_BOUNDS = {
    "min_lat": 37.413,
    "max_lat": 37.715,
    "min_lng": 126.734,
    "max_lng": 127.270,
}

SEOUL_ADMIN_DONGS = {
    "강남구": ["신사동", "논현1동", "논현2동", "압구정동", "청담동", "삼성1동", "삼성2동", "대치1동", "대치2동", "대치4동", "역삼1동", "역삼2동", "도곡1동", "도곡2동", "개포1동", "개포2동", "개포3동", "개포4동", "세곡동", "일원본동", "일원1동", "수서동"],
    "강동구": ["강일동", "상일1동", "상일2동", "명일1동", "명일2동", "고덕1동", "고덕2동", "암사1동", "암사2동", "암사3동", "천호1동", "천호2동", "천호3동", "성내1동", "성내2동", "성내3동", "길동", "둔촌1동", "둔촌2동"],
    "강북구": ["삼양동", "미아동", "송중동", "송천동", "삼각산동", "번1동", "번2동", "번3동", "수유1동", "수유2동", "수유3동", "우이동", "인수동"],
    "강서구": ["염창동", "등촌1동", "등촌2동", "등촌3동", "화곡본동", "화곡1동", "화곡2동", "화곡3동", "화곡4동", "화곡6동", "화곡8동", "우장산동", "가양1동", "가양2동", "가양3동", "발산1동", "공항동", "방화1동", "방화2동", "방화3동"],
    "관악구": ["보라매동", "은천동", "성현동", "중앙동", "청림동", "행운동", "청룡동", "낙성대동", "인헌동", "남현동", "신림동", "신사동", "조원동", "미성동", "난곡동", "난향동", "서원동", "신원동", "서림동", "삼성동", "대학동"],
    "광진구": ["중곡1동", "중곡2동", "중곡3동", "중곡4동", "능동", "구의1동", "구의2동", "구의3동", "광장동", "자양1동", "자양2동", "자양3동", "자양4동", "화양동", "군자동"],
    "구로구": ["신도림동", "구로1동", "구로2동", "구로3동", "구로4동", "구로5동", "가리봉동", "고척1동", "고척2동", "개봉1동", "개봉2동", "개봉3동", "오류1동", "오류2동", "수궁동", "항동"],
    "금천구": ["가산동", "독산1동", "독산2동", "독산3동", "독산4동", "시흥1동", "시흥2동", "시흥3동", "시흥4동", "시흥5동"],
    "노원구": ["월계1동", "월계2동", "월계3동", "공릉1동", "공릉2동", "하계1동", "하계2동", "중계본동", "중계1동", "중계2·3동", "중계4동", "상계1동", "상계2동", "상계3·4동", "상계5동", "상계6·7동", "상계8동", "상계9동", "상계10동"],
    "도봉구": ["쌍문1동", "쌍문2동", "쌍문3동", "쌍문4동", "방학1동", "방학2동", "방학3동", "창1동", "창2동", "창3동", "창4동", "창5동", "도봉1동", "도봉2동"],
    "동대문구": ["용신동", "제기동", "전농1동", "전농2동", "답십리1동", "답십리2동", "장안1동", "장안2동", "청량리동", "회기동", "휘경1동", "휘경2동", "이문1동", "이문2동"],
    "동작구": ["노량진1동", "노량진2동", "상도1동", "상도2동", "상도3동", "상도4동", "흑석동", "사당1동", "사당2동", "사당3동", "사당4동", "사당5동", "대방동", "신대방1동", "신대방2동"],
    "마포구": ["공덕동", "아현동", "도화동", "용강동", "대흥동", "염리동", "신수동", "서강동", "서교동", "합정동", "망원1동", "망원2동", "연남동", "성산1동", "성산2동", "상암동"],
    "서대문구": ["충현동", "천연동", "북아현동", "신촌동", "연희동", "홍제1동", "홍제2동", "홍제3동", "홍은1동", "홍은2동", "남가좌1동", "남가좌2동", "북가좌1동", "북가좌2동"],
    "서초구": ["서초1동", "서초2동", "서초3동", "서초4동", "잠원동", "반포본동", "반포1동", "반포2동", "반포3동", "반포4동", "방배본동", "방배1동", "방배2동", "방배3동", "방배4동", "양재1동", "양재2동", "내곡동"],
    "성동구": ["왕십리도선동", "왕십리2동", "마장동", "사근동", "행당1동", "행당2동", "응봉동", "금호1가동", "금호2·3가동", "금호4가동", "옥수동", "성수1가1동", "성수1가2동", "성수2가1동", "성수2가3동", "송정동", "용답동"],
    "성북구": ["성북동", "삼선동", "동선동", "돈암1동", "돈암2동", "안암동", "보문동", "정릉1동", "정릉2동", "정릉3동", "정릉4동", "길음1동", "길음2동", "종암동", "월곡1동", "월곡2동", "장위1동", "장위2동", "장위3동", "석관동"],
    "송파구": ["풍납1동", "풍납2동", "거여1동", "거여2동", "마천1동", "마천2동", "방이1동", "방이2동", "오륜동", "오금동", "송파1동", "송파2동", "석촌동", "삼전동", "가락본동", "가락1동", "가락2동", "문정1동", "문정2동", "장지동", "위례동", "잠실본동", "잠실2동", "잠실3동", "잠실4동", "잠실6동", "잠실7동"],
    "양천구": ["목1동", "목2동", "목3동", "목4동", "목5동", "신월1동", "신월2동", "신월3동", "신월4동", "신월5동", "신월6동", "신월7동", "신정1동", "신정2동", "신정3동", "신정4동", "신정6동", "신정7동"],
    "영등포구": ["영등포본동", "영등포동", "여의동", "당산1동", "당산2동", "도림동", "문래동", "양평1동", "양평2동", "신길1동", "신길3동", "신길4동", "신길5동", "신길6동", "신길7동", "대림1동", "대림2동", "대림3동"],
    "용산구": ["후암동", "용산2가동", "남영동", "청파동", "원효로1동", "원효로2동", "효창동", "용문동", "한강로동", "이촌1동", "이촌2동", "이태원1동", "이태원2동", "한남동", "서빙고동", "보광동"],
    "은평구": ["녹번동", "불광1동", "불광2동", "갈현1동", "갈현2동", "구산동", "대조동", "응암1동", "응암2동", "응암3동", "역촌동", "신사1동", "신사2동", "증산동", "수색동", "진관동"],
    "종로구": ["청운효자동", "사직동", "삼청동", "부암동", "평창동", "무악동", "교남동", "가회동", "종로1·2·3·4가동", "종로5·6가동", "이화동", "혜화동", "창신1동", "창신2동", "창신3동", "숭인1동", "숭인2동"],
    "중구": ["소공동", "회현동", "명동", "필동", "장충동", "광희동", "을지로동", "신당동", "다산동", "약수동", "청구동", "신당5동", "동화동", "황학동", "중림동"],
    "중랑구": ["면목본동", "면목2동", "면목3·8동", "면목4동", "면목5동", "면목7동", "상봉1동", "상봉2동", "중화1동", "중화2동", "묵1동", "묵2동", "망우본동", "망우3동", "신내1동", "신내2동"],
}

SEOUL_DONG_CENTERS = {
    ("종로구", "청운효자동"): (37.5842, 126.9708),
    ("종로구", "사직동"): (37.5758, 126.9689),
    ("종로구", "삼청동"): (37.5850, 126.9818),
    ("종로구", "가회동"): (37.5828, 126.9867),
    ("종로구", "종로1·2·3·4가동"): (37.5703, 126.9830),
    ("종로구", "종로5·6가동"): (37.5707, 127.0030),
    ("종로구", "혜화동"): (37.5861, 127.0005),
    ("중구", "소공동"): (37.5638, 126.9796),
    ("중구", "회현동"): (37.5574, 126.9791),
    ("중구", "명동"): (37.5636, 126.9869),
    ("중구", "필동"): (37.5604, 126.9958),
    ("중구", "을지로동"): (37.5664, 126.9914),
    ("중구", "광희동"): (37.5644, 127.0051),
    ("중구", "신당동"): (37.5654, 127.0168),
    ("용산구", "한강로동"): (37.5299, 126.9706),
    ("용산구", "이태원1동"): (37.5345, 126.9946),
    ("용산구", "한남동"): (37.5345, 127.0036),
    ("성동구", "성수1가1동"): (37.5421, 127.0431),
    ("성동구", "성수2가1동"): (37.5397, 127.0555),
    ("성동구", "왕십리도선동"): (37.5676, 127.0255),
    ("광진구", "화양동"): (37.5452, 127.0717),
    ("광진구", "자양1동"): (37.5347, 127.0828),
    ("광진구", "광장동"): (37.5469, 127.1034),
    ("동대문구", "청량리동"): (37.5877, 127.0473),
    ("동대문구", "회기동"): (37.5908, 127.0553),
    ("중랑구", "면목본동"): (37.5893, 127.0875),
    ("중랑구", "상봉1동"): (37.5979, 127.0930),
    ("성북구", "성북동"): (37.5926, 126.9989),
    ("성북구", "안암동"): (37.5860, 127.0217),
    ("성북구", "정릉1동"): (37.6034, 127.0135),
    ("강북구", "수유3동"): (37.6380, 127.0255),
    ("강북구", "미아동"): (37.6270, 127.0261),
    ("도봉구", "창1동"): (37.6477, 127.0449),
    ("도봉구", "도봉2동"): (37.6692, 127.0470),
    ("노원구", "상계6·7동"): (37.6542, 127.0606),
    ("노원구", "공릉1동"): (37.6248, 127.0738),
    ("은평구", "녹번동"): (37.6028, 126.9292),
    ("은평구", "진관동"): (37.6375, 126.9198),
    ("서대문구", "신촌동"): (37.5654, 126.9390),
    ("서대문구", "연희동"): (37.5736, 126.9352),
    ("마포구", "서교동"): (37.5552, 126.9237),
    ("마포구", "연남동"): (37.5623, 126.9217),
    ("마포구", "상암동"): (37.5784, 126.8927),
    ("양천구", "목1동"): (37.5307, 126.8755),
    ("양천구", "신정1동"): (37.5186, 126.8545),
    ("강서구", "가양1동"): (37.5696, 126.8449),
    ("강서구", "공항동"): (37.5585, 126.8107),
    ("강서구", "화곡1동"): (37.5441, 126.8416),
    ("구로구", "신도림동"): (37.5088, 126.8807),
    ("구로구", "구로3동"): (37.4854, 126.8955),
    ("금천구", "가산동"): (37.4768, 126.8838),
    ("금천구", "시흥1동"): (37.4568, 126.8954),
    ("영등포구", "여의동"): (37.5236, 126.9246),
    ("영등포구", "문래동"): (37.5165, 126.8899),
    ("동작구", "노량진1동"): (37.5125, 126.9419),
    ("동작구", "흑석동"): (37.5053, 126.9626),
    ("관악구", "낙성대동"): (37.4761, 126.9580),
    ("관악구", "신림동"): (37.4874, 126.9298),
    ("서초구", "서초2동"): (37.4921, 127.0246),
    ("서초구", "반포4동"): (37.4995, 127.0005),
    ("서초구", "양재1동"): (37.4837, 127.0365),
    ("강남구", "신사동"): (37.5224, 127.0287),
    ("강남구", "압구정동"): (37.5271, 127.0307),
    ("강남구", "청담동"): (37.5251, 127.0493),
    ("강남구", "삼성1동"): (37.5146, 127.0625),
    ("강남구", "대치1동"): (37.4931, 127.0560),
    ("강남구", "역삼1동"): (37.5007, 127.0365),
    ("송파구", "잠실6동"): (37.5145, 127.1003),
    ("송파구", "석촌동"): (37.5036, 127.1036),
    ("송파구", "가락본동"): (37.4957, 127.1200),
    ("송파구", "문정2동"): (37.4860, 127.1225),
    ("강동구", "천호2동"): (37.5435, 127.1259),
    ("강동구", "길동"): (37.5391, 127.1466),
    ("강동구", "상일1동"): (37.5512, 127.1693),
}


DEMO_PLACES = [
    {
        "id": "d1",
        "lat": 37.5665,
        "lng": 126.9780,
        "name": "시청 앞 느티나무 벤치",
        "type": "rest",
        "time_slot": ["lunch", "evening"],
        "season": ["summer", "fall"],
        "tags": ["그늘 있음", "조용함", "잠깐 쉬기 좋음"],
        "description": "오후에 그늘이 넓게 져서 점심 먹고 쉬기 좋아요. 벤치 3개, 앉아서 커피 마시기 딱입니다.",
        "likes": 12,
        "liked_by": [],
        "created_at": "2026-04-15",
        "feeds": [],
        "supplements": ["가을에 은행잎이 예뻐요. 사진 찍기도 좋습니다!"],
    },
    {
        "id": "d2",
        "lat": 37.5700,
        "lng": 126.9745,
        "name": "청계천 버들길",
        "type": "walk",
        "time_slot": ["morning", "evening"],
        "season": ["spring", "summer"],
        "tags": ["산책하기 좋음", "나무 많음", "혼자 가기 좋음", "여유로움"],
        "description": "아침 일찍 걸으면 사람이 적고 새소리가 들려요. 버드나무 그늘이 시원합니다.",
        "likes": 24,
        "liked_by": [],
        "created_at": "2026-03-20",
        "feeds": [],
        "supplements": [],
    },
    {
        "id": "d3",
        "lat": 37.5645,
        "lng": 126.9810,
        "name": "을지로 지하상가 입구",
        "type": "wait",
        "time_slot": ["lunch", "evening"],
        "season": ["all"],
        "tags": ["비 피하기 좋음", "기다리기 좋음", "편안함"],
        "description": "비 올 때 잠깐 피하기 딱 좋아요. 실내라 겨울에도 따뜻하고, 의자도 있습니다.",
        "likes": 8,
        "liked_by": [],
        "created_at": "2026-04-02",
        "feeds": [],
        "supplements": [],
    },
    {
        "id": "d4",
        "lat": 37.5723,
        "lng": 126.9769,
        "name": "광화문 광장 세종대왕상 앞",
        "type": "meet",
        "time_slot": ["lunch", "evening"],
        "season": ["all"],
        "tags": ["친구와 가기 좋음", "활기 있음"],
        "description": "약속 장소로 찾기 쉬워요. 누구나 아는 랜드마크! 주변에 벤치도 많습니다.",
        "likes": 31,
        "liked_by": [],
        "created_at": "2026-02-10",
        "feeds": [],
        "supplements": [],
    },
    {
        "id": "d5",
        "lat": 37.5590,
        "lng": 126.9830,
        "name": "남산 소나무길 입구",
        "type": "season",
        "time_slot": ["morning", "evening"],
        "season": ["fall", "winter"],
        "tags": ["산책하기 좋음", "전망 좋음", "사진 찍기 좋음"],
        "description": "가을 단풍이 정말 아름답고, 겨울엔 눈 쌓인 소나무가 멋집니다. 경사 완만해요.",
        "likes": 19,
        "liked_by": [],
        "created_at": "2026-01-25",
        "feeds": [],
        "supplements": [],
    },
    {
        "id": "d6",
        "lat": 37.5695,
        "lng": 126.9825,
        "name": "종각역 지하 공공화장실·정수기",
        "type": "life",
        "time_slot": ["morning", "lunch", "evening", "night"],
        "season": ["all"],
        "tags": ["편안함"],
        "description": "깨끗하게 관리되는 공공화장실이에요. 정수기도 있어서 물 채우기 좋습니다.",
        "likes": 15,
        "liked_by": [],
        "created_at": "2026-03-05",
        "feeds": [],
        "supplements": [],
    },
    {
        "id": "d7",
        "lat": 37.5658,
        "lng": 126.9752,
        "name": "덕수궁 돌담길",
        "type": "walk",
        "time_slot": ["morning", "lunch", "evening"],
        "season": ["spring", "fall"],
        "tags": ["산책하기 좋음", "감성적임", "사진 찍기 좋음", "혼자 가기 좋음"],
        "description": "봄 벚꽃, 가을 단풍 모두 아름다운 클래식 산책길. 평일 오전이 한적해요.",
        "likes": 42,
        "liked_by": [],
        "created_at": "2026-04-01",
        "feeds": [],
        "supplements": [],
    },
    {
        "id": "d8",
        "lat": 37.5712,
        "lng": 126.9810,
        "name": "인사동 쌈지길 앞 벤치",
        "type": "rest",
        "time_slot": ["lunch", "evening"],
        "season": ["spring", "fall"],
        "tags": ["잠깐 쉬기 좋음", "활기 있음", "친구와 가기 좋음"],
        "description": "인사동 구경하다 잠깐 앉기 좋아요. 사람 구경도 재밌습니다.",
        "likes": 9,
        "liked_by": [],
        "created_at": "2026-05-03",
        "feeds": [],
        "supplements": [],
    },
]

DEMO_COURSES = [
    {
        "title": "🌙 혼자 걷기 좋은 저녁 산책",
        "description": "청계천 버들길에서 시작해 덕수궁 돌담길까지, 조용하게 걷기 좋은 코스",
        "place_ids": ["d2", "d7"],
    },
    {
        "title": "☀️ 점심시간 힐링 코스",
        "description": "시청 벤치에서 쉬고 광화문까지 걸으며 기분전환",
        "place_ids": ["d1", "d4"],
    },
    {
        "title": "🍂 가을 감성 산책",
        "description": "덕수궁 돌담길 → 남산 소나무길로 이어지는 단풍 코스",
        "place_ids": ["d7", "d5"],
    },
]


def init_state() -> None:
    if "places" not in st.session_state:
        st.session_state.places = deepcopy(DEMO_PLACES)
    for place in st.session_state.places:
        place.setdefault("liked_by", [])
        place.setdefault("feeds", place.pop("comments", []))
        district, admin_dong = infer_admin_area(place["lat"], place["lng"])
        place.setdefault("district", district)
        place.setdefault("admin_dong", admin_dong)
    if "selected_place_id" not in st.session_state:
        st.session_state.selected_place_id = None
    if "picked_location" not in st.session_state:
        st.session_state.picked_location = None
    if "account_name" not in st.session_state:
        st.session_state.account_name = "동네 주민"


def current_account() -> str:
    account_name = st.session_state.account_name.strip()
    return account_name or "동네 주민"


def feed_columns(photo_count: int) -> int:
    if photo_count == 1:
        return 1
    if photo_count <= 4:
        return 2
    return 3


def label_options(source: dict[str, str] | dict[str, dict[str, str]]) -> dict[str, str]:
    labels = {}
    for key, value in source.items():
        if isinstance(value, dict):
            labels[f"{value['emoji']} {value['label']}"] = key
        else:
            labels[value] = key
    return labels


def is_in_seoul(lat: float, lng: float) -> bool:
    return (
        SEOUL_BOUNDS["min_lat"] <= lat <= SEOUL_BOUNDS["max_lat"]
        and SEOUL_BOUNDS["min_lng"] <= lng <= SEOUL_BOUNDS["max_lng"]
    )


def coordinate_distance(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    lat_scale = 111.0
    lng_scale = 111.0 * cos(radians((lat1 + lat2) / 2))
    return sqrt(((lat1 - lat2) * lat_scale) ** 2 + ((lng1 - lng2) * lng_scale) ** 2)


def infer_admin_area(lat: float, lng: float) -> tuple[str, str]:
    if not is_in_seoul(lat, lng):
        return "서울 외 지역", "서울 외 지역"

    nearest_area = min(
        SEOUL_DONG_CENTERS.items(),
        key=lambda item: coordinate_distance(lat, lng, item[1][0], item[1][1]),
    )[0]
    return nearest_area


def seoul_district_options() -> list[str]:
    return ["전체"] + sorted(SEOUL_ADMIN_DONGS) + ["서울 외 지역"]


def seoul_dong_options(district: str) -> list[str]:
    if district == "전체":
        return ["전체"]
    if district == "서울 외 지역":
        return ["전체", "서울 외 지역"]
    return ["전체"] + SEOUL_ADMIN_DONGS[district]


def matches_any(selected: list[str], values: list[str], include_all: bool = False) -> bool:
    if not selected:
        return True
    if include_all and "all" in values:
        return True
    return any(value in selected for value in values)


def filter_places(
    places: list[dict],
    selected_district: str,
    selected_admin_dong: str,
    selected_types: list[str],
    selected_times: list[str],
    selected_seasons: list[str],
    selected_tags: list[str],
) -> list[dict]:
    return [
        place
        for place in places
        if (selected_district == "전체" or place["district"] == selected_district)
        and (selected_admin_dong == "전체" or place["admin_dong"] == selected_admin_dong)
        and matches_any(selected_types, [place["type"]])
        and matches_any(selected_times, place["time_slot"])
        and matches_any(selected_seasons, place["season"], include_all=True)
        and matches_any(selected_tags, place["tags"])
    ]


def marker_html(place_type: str) -> str:
    meta = PLACE_TYPES[place_type]
    return f"""
    <div style="
        width: 36px;
        height: 36px;
        border-radius: 999px;
        background: {meta["color"]};
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        border: 3px solid white;
        box-shadow: 0 6px 16px rgba(15, 23, 42, 0.25);
        font-size: 18px;
    ">{meta["emoji"]}</div>
    """


def make_map(places: list[dict], picked_location: dict | None) -> folium.Map:
    if places:
        center = [
            sum(place["lat"] for place in places) / len(places),
            sum(place["lng"] for place in places) / len(places),
        ]
        zoom_start = 14 if len(places) > 1 else 16
    elif picked_location:
        center = [picked_location["lat"], picked_location["lng"]]
        zoom_start = 16
    else:
        center = [37.567, 126.979]
        zoom_start = 12

    dongne_map = folium.Map(
        location=center,
        zoom_start=zoom_start,
        tiles="CartoDB positron",
        control_scale=True,
    )

    for place in places:
        meta = PLACE_TYPES[place["type"]]
        popup = folium.Popup(
            f"""
            <strong>{place["name"]}</strong><br>
            {place["district"]} {place["admin_dong"]}<br>
            {meta["emoji"]} {meta["label"]}<br>
            ❤️ {place["likes"]}<br>
            {place["description"]}
            """,
            max_width=280,
        )
        folium.Marker(
            location=[place["lat"], place["lng"]],
            tooltip=place["name"],
            popup=popup,
            icon=folium.DivIcon(html=marker_html(place["type"])),
        ).add_to(dongne_map)

    if picked_location:
        folium.Marker(
            location=[picked_location["lat"], picked_location["lng"]],
            tooltip="새 장소 위치",
            icon=folium.Icon(color="red", icon="map-pin", prefix="fa"),
        ).add_to(dongne_map)

    return dongne_map


def render_place_card(place: dict) -> None:
    meta = PLACE_TYPES[place["type"]]
    time_text = ", ".join(TIME_LABELS[item] for item in place["time_slot"])
    season_text = ", ".join(SEASON_LABELS[item] for item in place["season"])
    account_name = current_account()
    already_liked = account_name in place["liked_by"]

    with st.container(border=True):
        st.subheader(f"{meta['emoji']} {place['name']}")
        st.caption(f"{place['district']} {place['admin_dong']} · {meta['label']} · {time_text} · {season_text}")
        st.write(place["description"])
        if place["tags"]:
            st.write(" ".join(f"`#{tag}`" for tag in place["tags"]))

        left, right = st.columns([1, 2])
        with left:
            like_label = f"❤️ 공감 {place['likes']}"
            if already_liked:
                like_label = f"❤️ 공감 완료 {place['likes']}"
            if st.button(like_label, key=f"like-{place['id']}", disabled=already_liked):
                place["likes"] += 1
                place["liked_by"].append(account_name)
                st.rerun()
        with right:
            st.caption(f"등록일 {place['created_at']}")

        if place["supplements"]:
            st.markdown("**주민이 덧붙인 정보**")
            for supplement in place["supplements"]:
                st.info(supplement)

        st.divider()
        st.markdown(f"**사진 피드 {len(place['feeds'])}개**")
        if place["feeds"]:
            for feed in reversed(place["feeds"]):
                with st.container(border=True):
                    st.caption(f"{feed['author']} · {feed['created_at']}")
                    photos = feed.get("photos", [])
                    if photos:
                        columns = st.columns(feed_columns(len(photos)))
                        for index, photo in enumerate(photos):
                            with columns[index % len(columns)]:
                                st.image(photo["data"], caption=photo["name"], use_container_width=True)
                    st.write(feed.get("review", feed.get("content", "")))
        else:
            st.caption("아직 사진 피드가 없습니다.")

        with st.form(f"feed-form-{place['id']}", clear_on_submit=True):
            photos = st.file_uploader(
                "사진 업로드",
                type=["jpg", "jpeg", "png", "webp"],
                accept_multiple_files=True,
                key=f"feed-photos-{place['id']}",
            )
            review = st.text_area(
                "한줄평",
                placeholder="이 장소에서 찍은 사진과 함께 남길 한줄평을 적어주세요.",
                height=100,
                max_chars=500,
                key=f"feed-review-{place['id']}",
            )
            st.caption(f"{len(review)} / 500자 · 사진은 피드당 최대 10장")
            submitted = st.form_submit_button("피드 등록")

        if submitted:
            if not photos:
                st.error("사진을 1장 이상 업로드해 주세요.")
                return
            if len(photos) > 10:
                st.error("사진은 한 피드당 최대 10장까지 업로드할 수 있습니다.")
                return
            if not review.strip():
                st.error("한줄평을 입력해 주세요.")
                return
            if len(review.strip()) > 500:
                st.error("한줄평은 500자 이하로 작성해 주세요.")
                return
            place["feeds"].append(
                {
                    "id": str(uuid4()),
                    "author": account_name,
                    "review": review.strip(),
                    "photos": [
                        {
                            "name": photo.name,
                            "type": photo.type,
                            "data": photo.getvalue(),
                        }
                        for photo in photos
                    ],
                    "created_at": date.today().isoformat(),
                }
            )
            st.success("사진 피드가 등록되었습니다.")
            st.rerun()


def render_courses(places: list[dict]) -> None:
    place_by_id = {place["id"]: place for place in st.session_state.places}
    st.subheader("추천 코스")
    for course in DEMO_COURSES:
        course_places = [place_by_id[place_id] for place_id in course["place_ids"] if place_id in place_by_id]
        if not course_places:
            continue
        if places and not any(place in places for place in course_places):
            continue
        with st.container(border=True):
            st.markdown(f"**{course['title']}**")
            st.caption(course["description"])
            st.write(" → ".join(place["name"] for place in course_places))


def render_add_place_form() -> None:
    st.subheader("장소 등록")
    st.caption("지도에서 위치를 클릭하면 좌표가 자동으로 들어옵니다.")

    picked = st.session_state.picked_location
    if picked:
        suggested_district, suggested_dong = infer_admin_area(picked["lat"], picked["lng"])
        st.success(f"선택된 위치: {picked['lat']:.5f}, {picked['lng']:.5f}")
        st.caption(f"자동 분류: {suggested_district} {suggested_dong}")
    else:
        suggested_district, suggested_dong = "종로구", "종로1·2·3·4가동"
        st.warning("먼저 지도에서 등록할 위치를 클릭해 주세요.")

    type_labels = label_options(PLACE_TYPES)
    time_labels = label_options(TIME_LABELS)
    season_labels = label_options(SEASON_LABELS)

    with st.form("add-place-form", clear_on_submit=True):
        name = st.text_input("장소 이름", placeholder="예: 동네 느티나무 벤치")
        district_values = sorted(SEOUL_ADMIN_DONGS) + ["서울 외 지역"]
        district_index = district_values.index(suggested_district) if suggested_district in district_values else 0
        district = st.selectbox("자치구", district_values, index=district_index)
        dong_values = SEOUL_ADMIN_DONGS.get(district, ["서울 외 지역"])
        dong_index = dong_values.index(suggested_dong) if suggested_dong in dong_values else 0
        admin_dong = st.selectbox("행정동", dong_values, index=dong_index)
        place_type_label = st.selectbox("장소 유형", list(type_labels.keys()))
        time_label_values = st.multiselect("이용 시간대", list(time_labels.keys()))
        season_label_values = st.multiselect("추천 계절", list(season_labels.keys()))
        selected_tags = st.multiselect("태그", ALL_TAGS)
        description = st.text_area(
            "한 줄 설명",
            placeholder="이 장소를 어떻게 사용하는지 간단히 적어주세요.",
            height=120,
        )
        submitted = st.form_submit_button("등록하기", type="primary")

    if submitted:
        if not picked or not name.strip() or not description.strip() or not time_label_values or not season_label_values:
            st.error("위치, 이름, 시간대, 계절, 설명을 모두 입력해 주세요.")
            return

        st.session_state.places.append(
            {
                "id": str(uuid4()),
                "lat": picked["lat"],
                "lng": picked["lng"],
                "name": name.strip(),
                "district": district,
                "admin_dong": admin_dong,
                "type": type_labels[place_type_label],
                "time_slot": [time_labels[label] for label in time_label_values],
                "season": [season_labels[label] for label in season_label_values],
                "tags": selected_tags,
                "description": description.strip(),
                "likes": 0,
                "liked_by": [],
                "created_at": date.today().isoformat(),
                "feeds": [],
                "supplements": [],
            }
        )
        st.session_state.picked_location = None
        st.success("장소가 등록되었습니다.")
        st.rerun()


def main() -> None:
    init_state()

    st.title("🗺️ 동네 사용설명서")
    st.caption("서울의 장소를 행정동 단위로 나눠 보고, 주민이 아는 작은 정보를 더합니다.")

    with st.sidebar:
        st.header("내 계정")
        st.text_input("계정 이름", key="account_name")
        st.caption(f"{current_account()} 계정으로 공감과 사진 피드를 남깁니다.")

        st.divider()
        st.header("필터")
        type_labels = label_options(PLACE_TYPES)
        time_labels = label_options(TIME_LABELS)
        season_labels = label_options(SEASON_LABELS)

        selected_district = st.selectbox("자치구", seoul_district_options())
        selected_admin_dong = st.selectbox("행정동", seoul_dong_options(selected_district))
        selected_type_labels = st.multiselect("장소 유형", list(type_labels.keys()))
        selected_time_labels = st.multiselect("시간대", list(time_labels.keys()))
        selected_season_labels = st.multiselect("계절", list(season_labels.keys()))
        selected_tags = st.multiselect("태그", ALL_TAGS)

        st.divider()
        render_add_place_form()

    selected_types = [type_labels[label] for label in selected_type_labels]
    selected_times = [time_labels[label] for label in selected_time_labels]
    selected_seasons = [season_labels[label] for label in selected_season_labels]

    filtered_places = filter_places(
        st.session_state.places,
        selected_district,
        selected_admin_dong,
        selected_types,
        selected_times,
        selected_seasons,
        selected_tags,
    )

    map_col, info_col = st.columns([1.55, 1], gap="large")

    with map_col:
        area_label = selected_district if selected_admin_dong == "전체" else f"{selected_district} {selected_admin_dong}"
        st.markdown(f"**{area_label} 표시 중인 장소 {len(filtered_places)}곳**")
        map_state = st_folium(
            make_map(filtered_places, st.session_state.picked_location),
            height=680,
            use_container_width=True,
            returned_objects=["last_clicked"],
        )
        if map_state.get("last_clicked"):
            clicked = map_state["last_clicked"]
            picked_location = {
                "lat": clicked["lat"],
                "lng": clicked["lng"],
            }
            if picked_location != st.session_state.picked_location:
                st.session_state.picked_location = picked_location
                st.rerun()

    with info_col:
        tab_places, tab_courses, tab_about = st.tabs(["장소", "코스", "소개"])
        with tab_places:
            if not filtered_places:
                st.info("조건에 맞는 장소가 없습니다.")
            for place in sorted(filtered_places, key=lambda item: item["likes"], reverse=True):
                render_place_card(place)

        with tab_courses:
            render_courses(filtered_places)

        with tab_about:
            st.subheader("PGIS 기반 주민 참여형 지도")
            st.write(
                "동네 사용설명서는 주민들이 직접 발견한 쉬는 곳, 걷기 좋은 길, "
                "기다리기 좋은 장소, 생활 편의 정보를 서울 행정동 단위로 모아 보는 작은 지도입니다."
            )
            st.write("Railway에서는 이 파일을 `streamlit run app.py`로 실행하면 됩니다.")


if __name__ == "__main__":
    main()
