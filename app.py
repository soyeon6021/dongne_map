from __future__ import annotations

from datetime import date
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
    "rest": {"label": "쉬기 좋은 곳", "emoji": "🪑", "icon": "R", "color": "#16a34a"},
    "walk": {"label": "걷기 좋은 길", "emoji": "🚶", "icon": "W", "color": "#2563eb"},
    "wait": {"label": "기다리기 좋은 곳", "emoji": "⏳", "icon": "T", "color": "#d97706"},
    "meet": {"label": "만남 장소", "emoji": "🤝", "icon": "M", "color": "#db2777"},
    "season": {"label": "계절별 추천", "emoji": "🌸", "icon": "S", "color": "#ea580c"},
    "life": {"label": "생활 편의", "emoji": "🏪", "icon": "L", "color": "#7c3aed"},
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
        "created_at": "2026-04-15",
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
        "created_at": "2026-03-20",
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
        "created_at": "2026-04-02",
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
        "created_at": "2026-02-10",
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
        "created_at": "2026-01-25",
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
        "created_at": "2026-03-05",
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
        "created_at": "2026-04-01",
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
        "created_at": "2026-05-03",
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
        st.session_state.places = [place.copy() for place in DEMO_PLACES]
    if "selected_place_id" not in st.session_state:
        st.session_state.selected_place_id = None
    if "picked_location" not in st.session_state:
        st.session_state.picked_location = None


def label_options(source: dict[str, str] | dict[str, dict[str, str]]) -> dict[str, str]:
    labels = {}
    for key, value in source.items():
        if isinstance(value, dict):
            labels[f"{value['emoji']} {value['label']}"] = key
        else:
            labels[value] = key
    return labels


def matches_any(selected: list[str], values: list[str], include_all: bool = False) -> bool:
    if not selected:
        return True
    if include_all and "all" in values:
        return True
    return any(value in selected for value in values)


def filter_places(
    places: list[dict],
    selected_types: list[str],
    selected_times: list[str],
    selected_seasons: list[str],
    selected_tags: list[str],
) -> list[dict]:
    return [
        place
        for place in places
        if matches_any(selected_types, [place["type"]])
        and matches_any(selected_times, place["time_slot"])
        and matches_any(selected_seasons, place["season"], include_all=True)
        and matches_any(selected_tags, place["tags"])
    ]


def marker_html(place_type: str) -> str:
    meta = PLACE_TYPES[place_type]
    return f"""
    <div style="
        position: relative;
        width: 38px;
        height: 48px;
        transform: translate(-19px, -44px);
        filter: drop-shadow(0 12px 16px rgba(15, 23, 42, 0.28));
    ">
        <div style="
            position: absolute;
            top: 1px;
            left: 3px;
            width: 32px;
            height: 32px;
            border: 2px solid rgba(255, 255, 255, 0.9);
            border-radius: 50% 50% 50% 0;
            box-sizing: border-box;
            background: linear-gradient(145deg, {meta["color"]} 0%, #111827 140%);
            transform: rotate(-45deg);
        "></div>
        <div style="
            position: absolute;
            top: 6px;
            left: 7px;
            width: 24px;
            height: 24px;
            border-radius: 999px;
            background: rgba(255, 255, 255, 0.94);
            display: flex;
            align-items: center;
            justify-content: center;
            color: {meta["color"]};
            font-family: Inter, Pretendard, -apple-system, BlinkMacSystemFont, sans-serif;
            font-size: 12px;
            font-weight: 800;
            letter-spacing: 0;
            box-shadow: inset 0 0 0 1px rgba(15, 23, 42, 0.08);
        ">{meta["icon"]}</div>
        <div style="
            position: absolute;
            left: 11px;
            bottom: 2px;
            width: 14px;
            height: 5px;
            border-radius: 999px;
            background: rgba(15, 23, 42, 0.18);
            filter: blur(1px);
        "></div>
    </div>
    """


def picked_marker_html() -> str:
    return """
    <div style="
        position: relative;
        width: 42px;
        height: 52px;
        transform: translate(-21px, -48px);
        filter: drop-shadow(0 14px 18px rgba(15, 23, 42, 0.30));
    ">
        <div style="
            position: absolute;
            top: 1px;
            left: 3px;
            width: 36px;
            height: 36px;
            border: 2px solid rgba(255, 255, 255, 0.92);
            border-radius: 50% 50% 50% 0;
            box-sizing: border-box;
            background: linear-gradient(145deg, #ef4444 0%, #7f1d1d 135%);
            transform: rotate(-45deg);
        "></div>
        <div style="
            position: absolute;
            top: 8px;
            left: 8px;
            width: 26px;
            height: 26px;
            border-radius: 999px;
            border: 2px solid rgba(255, 255, 255, 0.95);
            box-sizing: border-box;
            background: rgba(255, 255, 255, 0.2);
        "></div>
        <div style="
            position: absolute;
            top: 17px;
            left: 17px;
            width: 8px;
            height: 8px;
            border-radius: 999px;
            background: #ffffff;
        "></div>
        <div style="
            position: absolute;
            left: 13px;
            bottom: 2px;
            width: 16px;
            height: 6px;
            border-radius: 999px;
            background: rgba(15, 23, 42, 0.18);
            filter: blur(1px);
        "></div>
    </div>
    """


def make_map(places: list[dict], picked_location: dict | None) -> folium.Map:
    dongne_map = folium.Map(
        location=[37.567, 126.979],
        zoom_start=15,
        tiles="CartoDB positron",
        control_scale=True,
    )

    for place in places:
        meta = PLACE_TYPES[place["type"]]
        popup = folium.Popup(
            f"""
            <strong>{place["name"]}</strong><br>
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
            icon=folium.DivIcon(html=picked_marker_html()),
        ).add_to(dongne_map)

    return dongne_map


def render_place_card(place: dict) -> None:
    meta = PLACE_TYPES[place["type"]]
    time_text = ", ".join(TIME_LABELS[item] for item in place["time_slot"])
    season_text = ", ".join(SEASON_LABELS[item] for item in place["season"])

    with st.container(border=True):
        st.subheader(f"{meta['emoji']} {place['name']}")
        st.caption(f"{meta['label']} · {time_text} · {season_text}")
        st.write(place["description"])
        if place["tags"]:
            st.write(" ".join(f"`#{tag}`" for tag in place["tags"]))

        left, right = st.columns([1, 2])
        with left:
            if st.button(f"❤️ 공감 {place['likes']}", key=f"like-{place['id']}"):
                place["likes"] += 1
                st.rerun()
        with right:
            st.caption(f"등록일 {place['created_at']}")

        if place["supplements"]:
            st.markdown("**주민이 덧붙인 정보**")
            for supplement in place["supplements"]:
                st.info(supplement)


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
        st.success(f"선택된 위치: {picked['lat']:.5f}, {picked['lng']:.5f}")
    else:
        st.warning("먼저 지도에서 등록할 위치를 클릭해 주세요.")

    type_labels = label_options(PLACE_TYPES)
    time_labels = label_options(TIME_LABELS)
    season_labels = label_options(SEASON_LABELS)

    with st.form("add-place-form", clear_on_submit=True):
        name = st.text_input("장소 이름", placeholder="예: 동네 느티나무 벤치")
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
                "type": type_labels[place_type_label],
                "time_slot": [time_labels[label] for label in time_label_values],
                "season": [season_labels[label] for label in season_label_values],
                "tags": selected_tags,
                "description": description.strip(),
                "likes": 0,
                "created_at": date.today().isoformat(),
                "supplements": [],
            }
        )
        st.session_state.picked_location = None
        st.success("장소가 등록되었습니다.")
        st.rerun()


def main() -> None:
    init_state()

    st.title("🗺️ 동네 사용설명서")
    st.caption("지도에는 없지만, 주민은 알고 있는 장소들")

    with st.sidebar:
        st.header("필터")
        type_labels = label_options(PLACE_TYPES)
        time_labels = label_options(TIME_LABELS)
        season_labels = label_options(SEASON_LABELS)

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
        selected_types,
        selected_times,
        selected_seasons,
        selected_tags,
    )

    map_col, info_col = st.columns([1.55, 1], gap="large")

    with map_col:
        st.markdown(f"**표시 중인 장소 {len(filtered_places)}곳**")
        map_state = st_folium(
            make_map(filtered_places, st.session_state.picked_location),
            height=680,
            use_container_width=True,
            returned_objects=["last_clicked"],
        )
        if map_state.get("last_clicked"):
            clicked = map_state["last_clicked"]
            st.session_state.picked_location = {
                "lat": clicked["lat"],
                "lng": clicked["lng"],
            }

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
                "기다리기 좋은 장소, 생활 편의 정보를 모아 보는 작은 지도입니다."
            )
            st.write("Railway에서는 이 파일을 `streamlit run app.py`로 실행하면 됩니다.")


if __name__ == "__main__":
    main()
