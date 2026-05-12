import { create } from "zustand";
import { Place, Course, PlaceType, TimeSlot, Season } from "./types";
import { v4 as uuid } from "uuid";

const DEMO: Place[] = [
  {
    id: "d1", lat: 37.5665, lng: 126.9780,
    name: "시청 앞 느티나무 벤치", type: "rest",
    timeSlot: ["lunch", "evening"], season: ["summer", "fall"],
    tags: ["그늘 있음", "조용함", "잠깐 쉬기 좋음"],
    description: "오후에 그늘이 넓게 져서 점심 먹고 쉬기 좋아요. 벤치 3개, 앉아서 커피 마시기 딱입니다.",
    photos: [], likes: 12, createdAt: "2026-04-15",
    supplements: [{ id: "s1", text: "가을에 은행잎이 예뻐요. 사진 찍기도 좋습니다!", createdAt: "2026-05-01" }],
  },
  {
    id: "d2", lat: 37.5700, lng: 126.9745,
    name: "청계천 버들길", type: "walk",
    timeSlot: ["morning", "evening"], season: ["spring", "summer"],
    tags: ["산책하기 좋음", "나무 많음", "혼자 가기 좋음", "여유로움"],
    description: "아침 일찍 걸으면 사람이 적고 새소리가 들려요. 버드나무 그늘이 시원합니다.",
    photos: [], likes: 24, createdAt: "2026-03-20", supplements: [],
  },
  {
    id: "d3", lat: 37.5645, lng: 126.9810,
    name: "을지로 지하상가 입구", type: "wait",
    timeSlot: ["lunch", "evening"], season: ["all"],
    tags: ["비 피하기 좋음", "기다리기 좋음", "편안함"],
    description: "비 올 때 잠깐 피하기 딱 좋아요. 실내라 겨울에도 따뜻하고, 의자도 있습니다.",
    photos: [], likes: 8, createdAt: "2026-04-02", supplements: [],
  },
  {
    id: "d4", lat: 37.5723, lng: 126.9769,
    name: "광화문 광장 세종대왕상 앞", type: "meet",
    timeSlot: ["lunch", "evening"], season: ["all"],
    tags: ["친구와 가기 좋음", "활기 있음"],
    description: "약속 장소로 찾기 쉬워요. 누구나 아는 랜드마크! 주변에 벤치도 많습니다.",
    photos: [], likes: 31, createdAt: "2026-02-10", supplements: [],
  },
  {
    id: "d5", lat: 37.5590, lng: 126.9830,
    name: "남산 소나무길 입구", type: "season",
    timeSlot: ["morning", "evening"], season: ["fall", "winter"],
    tags: ["산책하기 좋음", "전망 좋음", "사진 찍기 좋음"],
    description: "가을 단풍이 정말 아름답고, 겨울엔 눈 쌓인 소나무가 멋집니다. 경사 완만해요.",
    photos: [], likes: 19, createdAt: "2026-01-25", supplements: [],
  },
  {
    id: "d6", lat: 37.5695, lng: 126.9825,
    name: "종각역 지하 공공화장실·정수기", type: "life",
    timeSlot: ["morning", "lunch", "evening", "night"], season: ["all"],
    tags: ["편안함"],
    description: "깨끗하게 관리되는 공공화장실이에요. 정수기도 있어서 물 채우기 좋습니다.",
    photos: [], likes: 15, createdAt: "2026-03-05", supplements: [],
  },
  {
    id: "d7", lat: 37.5658, lng: 126.9752,
    name: "덕수궁 돌담길", type: "walk",
    timeSlot: ["morning", "lunch", "evening"], season: ["spring", "fall"],
    tags: ["산책하기 좋음", "감성적임", "사진 찍기 좋음", "혼자 가기 좋음"],
    description: "봄 벚꽃, 가을 단풍 모두 아름다운 클래식 산책길. 평일 오전이 한적해요.",
    photos: [], likes: 42, createdAt: "2026-04-01", supplements: [],
  },
  {
    id: "d8", lat: 37.5712, lng: 126.9810,
    name: "인사동 쌈지길 앞 벤치", type: "rest",
    timeSlot: ["lunch", "evening"], season: ["spring", "fall"],
    tags: ["잠깐 쉬기 좋음", "활기 있음", "친구와 가기 좋음"],
    description: "인사동 구경하다 잠깐 앉기 좋아요. 사람 구경도 재밌습니다.",
    photos: [], likes: 9, createdAt: "2026-05-03", supplements: [],
  },
];

const DEMO_COURSES: Course[] = [
  {
    id: "c1", title: "🌙 혼자 걷기 좋은 저녁 산책",
    description: "청계천 버들길에서 시작해 덕수궁 돌담길까지, 조용하게 걷기 좋은 코스",
    placeIds: ["d2", "d7"], createdAt: "2026-04-20",
  },
  {
    id: "c2", title: "☀️ 점심시간 힐링 코스",
    description: "시청 벤치에서 쉬고 광화문까지 걸으며 기분전환",
    placeIds: ["d1", "d4"], createdAt: "2026-04-25",
  },
  {
    id: "c3", title: "🍂 가을 감성 산책",
    description: "덕수궁 돌담길 → 남산 소나무길로 이어지는 단풍 코스",
    placeIds: ["d7", "d5"], createdAt: "2026-05-05",
  },
];

interface Filters {
  types: PlaceType[];
  timeSlots: TimeSlot[];
  seasons: Season[];
  tags: string[];
}

type PanelView = "none" | "detail" | "add" | "course" | "about";

interface AppState {
  places: Place[];
  courses: Course[];
  filters: Filters;
  selectedPlace: Place | null;
  isAddingPlace: boolean;
  newPlaceCoords: { lat: number; lng: number } | null;
  panel: PanelView;

  toggleFilter: (key: keyof Filters, value: string) => void;
  clearFilters: () => void;
  selectPlace: (p: Place | null) => void;
  addPlace: (p: Omit<Place, "id" | "likes" | "createdAt" | "supplements">) => void;
  likePlace: (id: string) => void;
  addSupplement: (placeId: string, text: string) => void;
  setAddingPlace: (v: boolean) => void;
  setNewPlaceCoords: (c: { lat: number; lng: number } | null) => void;
  setPanel: (v: PanelView) => void;
  filteredPlaces: () => Place[];
  activeFilterCount: () => number;
}

export const useStore = create<AppState>((set, get) => ({
  places: DEMO,
  courses: DEMO_COURSES,
  filters: { types: [], timeSlots: [], seasons: [], tags: [] },
  selectedPlace: null,
  isAddingPlace: false,
  newPlaceCoords: null,
  panel: "none",

  toggleFilter: (key, value) =>
    set((s) => {
      const arr = s.filters[key] as string[];
      const next = arr.includes(value) ? arr.filter((v) => v !== value) : [...arr, value];
      return { filters: { ...s.filters, [key]: next } };
    }),

  clearFilters: () =>
    set({ filters: { types: [], timeSlots: [], seasons: [], tags: [] } }),

  selectPlace: (p) => set({ selectedPlace: p, panel: p ? "detail" : "none" }),

  addPlace: (p) =>
    set((s) => ({
      places: [
        ...s.places,
        { ...p, id: uuid(), likes: 0, createdAt: new Date().toISOString().slice(0, 10), supplements: [] },
      ],
      panel: "none",
      isAddingPlace: false,
      newPlaceCoords: null,
    })),

  likePlace: (id) =>
    set((s) => ({
      places: s.places.map((p) => (p.id === id ? { ...p, likes: p.likes + 1 } : p)),
      selectedPlace: s.selectedPlace?.id === id ? { ...s.selectedPlace, likes: s.selectedPlace.likes + 1 } : s.selectedPlace,
    })),

  addSupplement: (placeId, text) =>
    set((s) => {
      const sup = { id: uuid(), text, createdAt: new Date().toISOString().slice(0, 10) };
      const places = s.places.map((p) =>
        p.id === placeId ? { ...p, supplements: [...p.supplements, sup] } : p
      );
      const sel = s.selectedPlace?.id === placeId
        ? { ...s.selectedPlace, supplements: [...s.selectedPlace.supplements, sup] }
        : s.selectedPlace;
      return { places, selectedPlace: sel };
    }),

  setAddingPlace: (v) =>
    set({ isAddingPlace: v, panel: v ? "add" : "none", newPlaceCoords: null }),

  setNewPlaceCoords: (c) => set({ newPlaceCoords: c }),

  setPanel: (v) =>
    set({ panel: v, selectedPlace: v === "detail" ? get().selectedPlace : null }),

  filteredPlaces: () => {
    const { places, filters } = get();
    return places.filter((p) => {
      if (filters.types.length && !filters.types.includes(p.type)) return false;
      if (filters.timeSlots.length && !p.timeSlot.some((t) => filters.timeSlots.includes(t))) return false;
      if (filters.seasons.length && !p.season.some((s) => filters.seasons.includes(s) || s === "all")) return false;
      if (filters.tags.length && !filters.tags.some((t) => p.tags.includes(t))) return false;
      return true;
    });
  },

  activeFilterCount: () => {
    const f = get().filters;
    return f.types.length + f.timeSlots.length + f.seasons.length + f.tags.length;
  },
}));