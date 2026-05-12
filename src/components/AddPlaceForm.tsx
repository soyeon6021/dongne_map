"use client";

import { useState } from "react";
import { useStore } from "@/lib/store";
import {
  PLACE_TYPES, TIME_LABELS, SEASON_LABELS, TAG_GROUPS,
  PlaceType, TimeSlot, Season,
} from "@/lib/types";

function toggle<T extends string>(arr: T[], v: T): T[] {
  return arr.includes(v) ? arr.filter((x) => x !== v) : [...arr, v];
}

export default function AddPlaceForm() {
  const { newPlaceCoords, addPlace } = useStore();
  const [name, setName] = useState("");
  const [type, setType] = useState<PlaceType>("rest");
  const [timeSlot, setTimeSlot] = useState<TimeSlot[]>([]);
  const [season, setSeason] = useState<Season[]>([]);
  const [tags, setTags] = useState<string[]>([]);
  const [desc, setDesc] = useState("");

  if (!newPlaceCoords)
    return (
      <div className="flex flex-col items-center justify-center h-64 text-gray-400 animate-fade-up">
        <div className="text-5xl mb-4">📍</div>
        <p className="text-sm font-medium">지도에서 등록할 위치를 클릭하세요</p>
        <p className="text-xs mt-1 text-gray-300">클릭하면 빨간 핀이 표시됩니다</p>
      </div>
    );

  const ok = name.trim() && desc.trim() && timeSlot.length > 0 && season.length > 0;

  return (
    <div className="p-5 space-y-5 animate-fade-up">
      {/* 좌표 */}
      <div className="bg-green-50 border border-green-200 rounded-xl p-3.5 text-sm text-green-700 font-medium">
        📍 위치 선택됨: {newPlaceCoords.lat.toFixed(5)}, {newPlaceCoords.lng.toFixed(5)}
      </div>

      {/* 이름 */}
      <div>
        <label className="block text-sm font-bold text-gray-700 mb-1.5">장소 이름 *</label>
        <input
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="예: 동네 느티나무 벤치"
          className="w-full border border-gray-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-primary-400 focus:ring-2 focus:ring-primary-100 transition"
        />
      </div>

      {/* 유형 */}
      <div>
        <label className="block text-sm font-bold text-gray-700 mb-2">장소 유형 *</label>
        <div className="grid grid-cols-2 gap-2">
          {Object.entries(PLACE_TYPES).map(([k, v]) => (
            <button
              key={k}
              onClick={() => setType(k as PlaceType)}
              className={`flex items-center gap-2 px-3.5 py-2.5 rounded-xl border text-sm transition ${
                type === k
                  ? "border-primary-500 bg-primary-50 font-bold text-primary-700"
                  : "border-gray-200 text-gray-600 hover:border-gray-300"
              }`}
            >
              <span className="text-lg">{v.emoji}</span>
              {v.label}
            </button>
          ))}
        </div>
      </div>

      {/* 시간대 */}
      <div>
        <label className="block text-sm font-bold text-gray-700 mb-2">이용 시간대 *</label>
        <div className="flex gap-2 flex-wrap">
          {Object.entries(TIME_LABELS).map(([k, v]) => (
            <button
              key={k}
              onClick={() => setTimeSlot(toggle(timeSlot, k as TimeSlot))}
              className={`px-4 py-1.5 rounded-full text-xs font-medium border transition ${
                timeSlot.includes(k as TimeSlot)
                  ? "bg-blue-500 text-white border-blue-500"
                  : "border-gray-300 text-gray-500 hover:border-blue-300"
              }`}
            >
              {v}
            </button>
          ))}
        </div>
      </div>

      {/* 계절 */}
      <div>
        <label className="block text-sm font-bold text-gray-700 mb-2">추천 계절 *</label>
        <div className="flex gap-2 flex-wrap">
          {Object.entries(SEASON_LABELS).map(([k, v]) => (
            <button
              key={k}
              onClick={() => setSeason(toggle(season, k as Season))}
              className={`px-4 py-1.5 rounded-full text-xs font-medium border transition ${
                season.includes(k as Season)
                  ? "bg-orange-500 text-white border-orange-500"
                  : "border-gray-300 text-gray-500 hover:border-orange-300"
              }`}
            >
              {v}
            </button>
          ))}
        </div>
      </div>

      {/* 태그 */}
      <div>
        <label className="block text-sm font-bold text-gray-700 mb-2">태그 (선택)</label>
        {TAG_GROUPS.map((g) => (
          <div key={g.label} className="mb-2">
            <span className="text-[11px] text-gray-400 font-semibold">{g.label}</span>
            <div className="flex gap-1.5 flex-wrap mt-1">
              {g.tags.map((t) => (
                <button
                  key={t}
                  onClick={() => setTags(toggle(tags, t))}
                  className={`px-2.5 py-1 rounded-full text-[11px] border transition ${
                    tags.includes(t)
                      ? "bg-gray-800 text-white border-gray-800"
                      : "border-gray-200 text-gray-500 hover:border-gray-400"
                  }`}
                >
                  #{t}
                </button>
              ))}
            </div>
          </div>
        ))}
      </div>

      {/* 설명 */}
      <div>
        <label className="block text-sm font-bold text-gray-700 mb-1.5">한 줄 설명 *</label>
        <textarea
          value={desc}
          onChange={(e) => setDesc(e.target.value)}
          placeholder="이 장소를 어떻게 사용하는지 간단히 적어주세요..."
          className="w-full border border-gray-200 rounded-xl p-3.5 text-sm resize-none h-28 focus:outline-none focus:border-primary-400 focus:ring-2 focus:ring-primary-100 transition"
        />
      </div>

      {/* 제출 */}
      <button
        onClick={() => {
          if (!ok) return;
          addPlace({
            lat: newPlaceCoords.lat,
            lng: newPlaceCoords.lng,
            name: name.trim(),
            type,
            timeSlot,
            season,
            tags,
            description: desc.trim(),
            photos: [],
          });
        }}
        disabled={!ok}
        className={`w-full py-3 rounded-xl text-sm font-bold transition ${
          ok
            ? "bg-primary-500 text-white hover:bg-primary-600 active:scale-[0.98] shadow-lg shadow-primary-200"
            : "bg-gray-100 text-gray-400 cursor-not-allowed"
        }`}
      >
        등록하기
      </button>
    </div>
  );
}