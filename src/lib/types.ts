export type PlaceType = "rest" | "walk" | "wait" | "meet" | "season" | "life";
export type TimeSlot = "morning" | "lunch" | "evening" | "night";
export type Season = "spring" | "summer" | "fall" | "winter" | "all";

export interface Supplement {
  id: string;
  text: string;
  createdAt: string;
}

export interface Place {
  id: string;
  lat: number;
  lng: number;
  name: string;
  type: PlaceType;
  timeSlot: TimeSlot[];
  season: Season[];
  tags: string[];
  description: string;
  photos: string[];
  likes: number;
  createdAt: string;
  supplements: Supplement[];
}

export interface Course {
  id: string;
  title: string;
  description: string;
  placeIds: string[];
  createdAt: string;
}

export const PLACE_TYPES: Record<PlaceType, { label: string; emoji: string; color: string }> = {
  rest:   { label: "쉬기 좋은 곳",    emoji: "🪑", color: "#22c55e" },
  walk:   { label: "걷기 좋은 길",    emoji: "🚶", color: "#3b82f6" },
  wait:   { label: "기다리기 좋은 곳", emoji: "⏳", color: "#f59e0b" },
  meet:   { label: "만남 장소",       emoji: "🤝", color: "#ec4899" },
  season: { label: "계절별 추천",     emoji: "🌸", color: "#f97316" },
  life:   { label: "생활 편의",       emoji: "🏪", color: "#8b5cf6" },
};

export const TIME_LABELS: Record<TimeSlot, string> = {
  morning: "아침", lunch: "점심", evening: "저녁", night: "밤",
};

export const SEASON_LABELS: Record<Season, string> = {
  spring: "봄", summer: "여름", fall: "가을", winter: "겨울", all: "사계절",
};

export const TAG_GROUPS: { label: string; tags: string[] }[] = [
  { label: "분위기", tags: ["조용함", "활기 있음", "여유로움", "편안함", "감성적임"] },
  { label: "환경",  tags: ["그늘 있음", "햇빛 좋음", "바람 잘 통함", "전망 좋음", "나무 많음"] },
  { label: "이용",  tags: ["혼자 가기 좋음", "친구와 가기 좋음", "가족과 가기 좋음", "기다리기 좋음"] },
  { label: "활동",  tags: ["산책하기 좋음", "공부하기 좋음", "사진 찍기 좋음", "잠깐 쉬기 좋음"] },
  { label: "날씨",  tags: ["봄에 좋음", "여름에 좋음", "비 피하기 좋음", "겨울 햇볕 좋음"] },
];

export const ALL_TAGS = TAG_GROUPS.flatMap((g) => g.tags);