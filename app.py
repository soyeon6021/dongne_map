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
FOLDER_OPTIONS = ["전체 폴더", "종로구 폴더", "중구 폴더"]
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
    "전체 폴더": {"center": [37.5708, 126.9911], "zoom": 14},
    "종로구 폴더": {"center": [37.5759, 126.9860], "zoom": 14},
    "중구 폴더": {"center": [37.5629, 126.9950], "zoom": 14},
}

TYPE_STYLES = {
    "쉬기 좋은 곳": {"color": "green", "icon": "tree"},
    "걷기 좋은 길": {"color": "blue", "icon": "road"},
    "기다리기 좋은 곳": {"color": "orange", "icon": "clock"},
    "만남 장소": {"color": "purple", "icon": "star"},
    "계절별 추천 장소": {"color": "pink", "icon": "heart"},
    "생활 편의 장소": {"color": "cadetblue", "icon": "info"},
    "역사·문화 산책길": {"color": "darkred", "icon": "landmark"},
    "비 오는 날 피하기 좋은 곳": {"color": "darkblue", "icon": "cloud-rain"},
    "밤에도 걷기 괜찮은 길": {"color": "darkpurple", "icon": "moon"},
}


def base_place_folders() -> dict[str, list[dict]]:
    """구별 장소 폴더. 나중에 CSV/DB로 옮길 때도 district 단위로 분리하기 쉽습니다."""
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
        "selected_folder": "종로구 폴더",
        "filter_types": [],
        "filter_time": "전체",
        "filter_season": "전체",
        "filter_tags": [],
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


def reset_filters() -> None:
    st.session_state.filter_types = []
    st.session_state.filter_time = "전체"
    st.session_state.filter_season = "전체"
    st.session_state.filter_tags = []


def apply_preset(types: list[str] | None = None, time: str = "전체", season: str = "전체", tags: list[str] | None = None) -> None:
    st.session_state.filter_types = types or []
    st.session_state.filter_time = time
    st.session_state.filter_season = season
    st.session_state.filter_tags = tags or []


def folder_to_district(folder_name: str) -> str | None:
    if folder_name == "종로구 폴더":
        return "종로구"
    if folder_name == "중구 폴더":
        return "중구"
    return None


def all_places() -> list[dict]:
    return [
        place
        for places in st.session_state.place_folders.values()
        for place in places
    ]


def folder_dataframe(folder_name: str) -> pd.DataFrame:
    district = folder_to_district(folder_name)
    places = st.session_state.place_folders[district] if district else all_places()
    return pd.DataFrame(places)


def as_text(value: list[str] | str) -> str:
    if isinstance(value, list):
        return ", ".join(value)
    return str(value)


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


def popup_html(row: pd.Series) -> str:
    return f"""
    <div style="width:260px">
        <h4 style="margin:0 0 6px 0;">{row.place_name}</h4>
        <b>장소 폴더</b>: {row.district}<br>
        <b>유형</b>: {row.place_type}<br>
        <b>추천 시간대</b>: {as_text(row.time_period)}<br>
        <b>추천 계절</b>: {as_text(row.season)}<br>
        <b>태그</b>: {as_text(row.tags)}<br>
        <b>공감</b>: {row.likes}<br>
        <p style="margin:8px 0 0 0;">{row.description}</p>
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
        m.fit_bounds(filtered_df[["latitude", "longitude"]].values.tolist(), padding=(28, 28))

    return m


def render_sidebar() -> None:
    st.sidebar.header("장소 폴더")
    st.sidebar.radio("구별로 먼저 선택", FOLDER_OPTIONS, key="selected_folder")
    st.sidebar.caption("장소가 섞여 보이지 않도록 선택한 폴더 안의 장소만 지도에 표시합니다.")

    st.sidebar.divider()
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


def render_folder_overview() -> None:
    cols = st.columns(2)
    for index, district in enumerate(DISTRICTS):
        places = st.session_state.place_folders[district]
        type_counter = Counter(place["place_type"] for place in places)
        tag_counter = Counter(tag for place in places for tag in place["tags"])
        with cols[index]:
            with st.container(border=True):
                st.subheader(f"{district} 폴더")
                st.metric("등록된 장소", f"{len(places)}곳")
                st.caption(f"대표 유형: {type_counter.most_common(1)[0][0]}")
                st.caption(f"대표 태그: {tag_counter.most_common(1)[0][0]}")


def render_summary(filtered_df: pd.DataFrame) -> None:
    tag_counter = Counter(tag for tags in filtered_df["tags"] for tag in tags) if not filtered_df.empty else Counter()
    type_counter = Counter(filtered_df["place_type"]) if not filtered_df.empty else Counter()
    avg_likes = filtered_df["likes"].mean() if not filtered_df.empty else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("현재 폴더 표시 장소", f"{len(filtered_df)}곳")
    col2.metric("가장 많은 유형", type_counter.most_common(1)[0][0] if type_counter else "-")
    col3.metric("가장 많은 태그", tag_counter.most_common(1)[0][0] if tag_counter else "-")
    col4.metric("평균 공감 수", f"{avg_likes:.1f}")

    if not filtered_df.empty:
        counts = filtered_df["district"].value_counts().reindex(DISTRICTS, fill_value=0)
        st.caption(f"종로구 {counts['종로구']}곳 · 중구 {counts['중구']}곳")


def render_place_cards(filtered_df: pd.DataFrame) -> None:
    if filtered_df.empty:
        st.info("현재 폴더와 필터에 맞는 장소가 없습니다.")
        return

    for _, row in filtered_df.sort_values(["district", "place_type", "likes"], ascending=[True, True, False]).iterrows():
        with st.container(border=True):
            st.markdown(f"**[{row.district}] {row.place_name}**")
            st.caption(f"{row.place_type} · {as_text(row.time_period)} · {as_text(row.season)} · 공감 {row.likes}")
            st.write(row.description)
            st.write(" ".join(f"`#{tag}`" for tag in row.tags))


def render_courses(folder_name: str) -> None:
    district = folder_to_district(folder_name)
    visible_courses = [course for course in COURSES if district is None or course["district"] == district]
    lookup = {place["id"]: place["place_name"] for place in all_places()}

    cols = st.columns(2)
    for index, course in enumerate(visible_courses):
        with cols[index % 2]:
            with st.container(border=True):
                names = [lookup[place_id] for place_id in course["place_ids"] if place_id in lookup]
                st.subheader(course["name"])
                st.caption(f"{course['district']} 폴더")
                st.write(course["description"])
                st.caption(" -> ".join(names))


def render_place_form() -> None:
    current_district = folder_to_district(st.session_state.selected_folder) or "종로구"

    st.subheader("장소 등록")
    st.caption(
        "등록한 장소는 선택한 구의 장소 폴더에 임시 저장됩니다. "
        "일반 리뷰보다 이 장소를 어떤 상황에서 어떻게 사용하는지 적어주세요."
    )

    with st.form("place_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        district = col1.selectbox("저장할 장소 폴더", DISTRICTS, index=DISTRICTS.index(current_district))
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

        submitted = st.form_submit_button("해당 구 폴더에 임시 등록")

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
    render_sidebar()

    st.title("동네 사용설명서")
    st.subheader("지도에는 없지만, 주민은 알고 있는 장소들")
    st.write("종로구와 중구의 생활경험 장소를 구별 폴더에 나누어 기록하는 PGIS 기반 도심 생활지도입니다.")

    render_folder_overview()

    folder_name = st.session_state.selected_folder
    folder_df = folder_dataframe(folder_name)
    filtered_df = filter_places(folder_df)

    st.divider()
    st.header(folder_name)
    st.caption("선택한 장소 폴더 안에서만 지도와 목록이 갱신됩니다.")
    render_summary(filtered_df)

    map_col, list_col = st.columns([1.35, 1], gap="large")
    with map_col:
        st.subheader("폴더 지도")
        st_folium(build_map(filtered_df, folder_name), width=None, height=560)

    with list_col:
        st.subheader("폴더 안 장소")
        render_place_cards(filtered_df)

    with st.expander("표로 보기", expanded=False):
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
