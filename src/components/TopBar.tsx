"use client";

import { useStore } from "@/lib/store";

export default function TopBar() {
  const { isAddingPlace, setAddingPlace, setPanel, panel } = useStore();

  return (
    <header className="bg-white/95 backdrop-blur border-b border-gray-200 px-5 py-2.5 flex items-center justify-between z-50 relative">
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 bg-gradient-to-br from-primary-400 to-primary-600 rounded-xl flex items-center justify-center text-white text-xl shadow-sm">
          🗺️
        </div>
        <div>
          <h1 className="text-[15px] font-bold text-gray-900 leading-tight tracking-tight">
            동네 사용설명서
          </h1>
          <p className="text-[11px] text-gray-400 tracking-wide">
            지도에는 없지만, 주민은 알고 있는 장소들
          </p>
        </div>
      </div>

      <nav className="flex items-center gap-1.5">
        <button
          onClick={() => setPanel(panel === "about" ? "none" : "about")}
          className={`px-3.5 py-1.5 text-[13px] rounded-lg transition ${
            panel === "about"
              ? "bg-gray-100 text-gray-800 font-semibold"
              : "text-gray-500 hover:bg-gray-50 hover:text-gray-700"
          }`}
        >
          ℹ️ 소개
        </button>
        <button
          onClick={() => setPanel(panel === "course" ? "none" : "course")}
          className={`px-3.5 py-1.5 text-[13px] rounded-lg transition ${
            panel === "course"
              ? "bg-gray-100 text-gray-800 font-semibold"
              : "text-gray-500 hover:bg-gray-50 hover:text-gray-700"
          }`}
        >
          🗂️ 추천코스
        </button>
        <button
          onClick={() => setAddingPlace(!isAddingPlace)}
          className={`px-4 py-2 text-[13px] font-bold rounded-xl transition shadow-sm ${
            isAddingPlace
              ? "bg-red-50 text-red-500 hover:bg-red-100 shadow-none"
              : "bg-primary-500 text-white hover:bg-primary-600 shadow-primary-200"
          }`}
        >
          {isAddingPlace ? "✕ 취소" : "＋ 장소 등록"}
        </button>
      </nav>
    </header>
  );
}