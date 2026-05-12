"use client";

import { useStore } from "@/lib/store";
import PlaceDetail from "./PlaceDetail";
import AddPlaceForm from "./AddPlaceForm";
import CoursePanel from "./CoursePanel";
import AboutPanel from "./AboutPanel";

const TITLES: Record<string, string> = {
  detail: "📍 장소 정보",
  add: "✏️ 새 장소 등록",
  course: "🗂️ 추천 코스",
  about: "ℹ️ 프로젝트 소개",
};

export default function SidePanel() {
  const { panel, setPanel } = useStore();

  return (
    <div className="w-[420px] max-w-full h-full bg-white border-l border-gray-200 flex flex-col shadow-2xl z-30 animate-slide-in">
      <div className="flex items-center justify-between px-5 py-3.5 border-b border-gray-100 shrink-0">
        <h2 className="font-bold text-[15px] text-gray-800">{TITLES[panel] || ""}</h2>
        <button
          onClick={() => setPanel("none")}
          className="w-8 h-8 flex items-center justify-center rounded-lg text-gray-400 hover:bg-gray-100 hover:text-gray-600 transition"
        >
          ✕
        </button>
      </div>
      <div className="flex-1 overflow-y-auto panel-scroll">
        {panel === "detail" && <PlaceDetail />}
        {panel === "add" && <AddPlaceForm />}
        {panel === "course" && <CoursePanel />}
        {panel === "about" && <AboutPanel />}
      </div>
    </div>
  );
}