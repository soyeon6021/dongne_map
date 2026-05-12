"use client";

import { useStore } from "@/lib/store";
import { PLACE_TYPES } from "@/lib/types";

export default function CoursePanel() {
  const { courses, places, selectPlace, setPanel } = useStore();

  const handlePlaceClick = (id: string) => {
    const p = places.find((x) => x.id === id);
    if (p) selectPlace(p);
  };

  return (
    <div className="p-5 space-y-4 animate-fade-up">
      <p className="text-sm text-gray-500 leading-relaxed">
        주민들이 여러 장소를 연결해 만든 테마별 추천 코스입니다.
        장소를 클릭하면 상세 정보를 확인할 수 있어요.
      </p>

      {courses.map((c, i) => (
        <div
          key={c.id}
          className="border border-gray-200 rounded-2xl p-5 space-y-3 hover:border-primary-300 hover:shadow-sm transition"
        >
          <div className="flex items-start justify-between">
            <h3 className="font-bold text-gray-800 text-[15px]">{c.title}</h3>
            <span className="text-xs text-gray-400 shrink-0">{c.createdAt}</span>
          </div>
          <p className="text-sm text-gray-500 leading-relaxed">{c.description}</p>
          <div className="flex flex-col gap-1.5">
            {c.placeIds.map((id, idx) => {
              const p = places.find((x) => x.id === id);
              if (!p) return null;
              const info = PLACE_TYPES[p.type];
              return (
                <button
                  key={id}
                  onClick={() => handlePlaceClick(id)}
                  className="flex items-center gap-2 text-left text-sm px-3 py-2 bg-gray-50 hover:bg-primary-50 rounded-lg transition"
                >
                  <span className="text-xs text-gray-400 font-mono w-5">{idx + 1}.</span>
                  <span>{info.emoji}</span>
                  <span className="text-gray-700 font-medium">{p.name}</span>
                </button>
              );
            })}
          </div>
        </div>
      ))}

      {courses.length === 0 && (
        <div className="text-center text-gray-400 py-8">
          <p className="text-3xl mb-2">🚶</p>
          <p className="text-sm">아직 등록된 코스가 없습니다</p>
        </div>
      )}
    </div>
  );
}