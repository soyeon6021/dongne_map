"use client";

import { useState } from "react";
import { useStore } from "@/lib/store";
import { PLACE_TYPES, TIME_LABELS, SEASON_LABELS } from "@/lib/types";

export default function PlaceDetail() {
  const { selectedPlace, likePlace, addSupplement } = useStore();
  const [text, setText] = useState("");

  if (!selectedPlace) return null;
  const p = selectedPlace;
  const info = PLACE_TYPES[p.type];

  return (
    <div className="p-5 space-y-5 animate-fade-up">
      {/* 헤더 */}
      <div>
        <div className="flex items-center gap-2 mb-2">
          <span
            className="px-2.5 py-1 rounded-full text-xs font-bold text-white"
            style={{ background: info.color }}
          >
            {info.emoji} {info.label}
          </span>
          <span className="text-xs text-gray-400">{p.createdAt}</span>
        </div>
        <h3 className="text-xl font-bold text-gray-900 leading-snug">{p.name}</h3>
      </div>

      {/* 설명 */}
      <p className="text-[14px] text-gray-600 leading-relaxed bg-gray-50 rounded-xl p-4">
        {p.description}
      </p>

      {/* 시간대/계절 */}
      <div className="space-y-2.5">
        <div className="flex gap-2 flex-wrap items-center">
          <span className="text-xs text-gray-400 font-medium w-12">시간대</span>
          {p.timeSlot.map((t) => (
            <span key={t} className="px-2.5 py-0.5 bg-blue-50 text-blue-600 text-xs rounded-full font-medium">
              {TIME_LABELS[t]}
            </span>
          ))}
        </div>
        <div className="flex gap-2 flex-wrap items-center">
          <span className="text-xs text-gray-400 font-medium w-12">계절</span>
          {p.season.map((s) => (
            <span key={s} className="px-2.5 py-0.5 bg-orange-50 text-orange-600 text-xs rounded-full font-medium">
              {SEASON_LABELS[s]}
            </span>
          ))}
        </div>
      </div>

      {/* 태그 */}
      <div className="flex gap-1.5 flex-wrap">
        {p.tags.map((t) => (
          <span key={t} className="px-2.5 py-1 bg-gray-100 text-gray-600 text-xs rounded-full">
            #{t}
          </span>
        ))}
      </div>

      {/* 공감 */}
      <button
        onClick={() => likePlace(p.id)}
        className="flex items-center gap-2.5 px-5 py-2.5 bg-pink-50 hover:bg-pink-100 text-pink-600 rounded-xl transition text-sm font-semibold active:scale-95"
      >
        ❤️ 공감하기
        <span className="bg-pink-200/50 px-2 py-0.5 rounded-full text-xs">{p.likes}</span>
      </button>

      {/* 보완 정보 */}
      {p.supplements.length > 0 && (
        <div className="space-y-2">
          <h4 className="text-sm font-bold text-gray-700">💬 보완 정보 ({p.supplements.length})</h4>
          {p.supplements.map((s) => (
            <div key={s.id} className="bg-blue-50/50 border border-blue-100 rounded-xl p-3.5">
              <p className="text-sm text-gray-700 leading-relaxed">{s.text}</p>
              <p className="text-[11px] text-gray-400 mt-1.5">{s.createdAt}</p>
            </div>
          ))}
        </div>
      )}

      {/* 정보 보완 입력 */}
      <div className="border-t border-gray-100 pt-4">
        <h4 className="text-sm font-bold text-gray-700 mb-2">📝 정보 보완하기</h4>
        <p className="text-xs text-gray-400 mb-2">이 장소에 대해 아는 추가 정보를 남겨주세요</p>
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="예: 겨울에는 바람이 세서 오후보다 오전이 나아요..."
          className="w-full border border-gray-200 rounded-xl p-3.5 text-sm resize-none h-24 focus:outline-none focus:border-primary-400 focus:ring-2 focus:ring-primary-100 transition"
        />
        <button
          onClick={() => {
            if (text.trim()) {
              addSupplement(p.id, text.trim());
              setText("");
            }
          }}
          disabled={!text.trim()}
          className={`mt-2 px-5 py-2.5 text-sm font-bold rounded-xl transition ${
            text.trim()
              ? "bg-primary-500 text-white hover:bg-primary-600 active:scale-95"
              : "bg-gray-100 text-gray-400 cursor-not-allowed"
          }`}
        >
          등록
        </button>
      </div>
    </div>
  );
}