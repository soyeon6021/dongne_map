"use client";

import { useStore } from "@/lib/store";
import { PLACE_TYPES, TIME_LABELS, SEASON_LABELS, PlaceType, TimeSlot, Season } from "@/lib/types";

function Chip({ active, label, onClick }: { active: boolean; label: string; onClick: () => void }) {
  return (
    <button
      onClick={onClick}
      className={`px-3 py-1 text-xs rounded-full border transition-all whitespace-nowrap ${
        active
          ? "bg-primary-500 text-white border-primary-500 shadow-sm"
          : "bg-white text-gray-500 border-gray-250 hover:border-primary-300 hover:text-primary-600"
      }`}
    >
      {label}
    </button>
  );
}

export default function FilterBar() {
  const { filters, toggleFilter, clearFilters, activeFilterCount } = useStore();
  const count = activeFilterCount();

  return (
    <div className="bg-white/95 backdrop-blur border-b border-gray-100 px-5 py-2 flex gap-5 items-center overflow-x-auto z-40 relative">
      {/* 유형 */}
      <div className="flex gap-1.5 items-center shrink-0">
        <span className="text-[11px] text-gray-400 font-semibold tracking-wide mr-0.5">유형</span>
        {Object.entries(PLACE_TYPES).map(([k, v]) => (
          <Chip
            key={k}
            active={filters.types.includes(k as PlaceType)}
            label={`${v.emoji} ${v.label}`}
            onClick={() => toggleFilter("types", k)}
          />
        ))}
      </div>

      <div className="w-px h-5 bg-gray-200 shrink-0" />

      {/* 시간대 */}
      <div className="flex gap-1.5 items-center shrink-0">
        <span className="text-[11px] text-gray-400 font-semibold tracking-wide mr-0.5">시간</span>
        {Object.entries(TIME_LABELS).map(([k, v]) => (
          <Chip
            key={k}
            active={filters.timeSlots.includes(k as TimeSlot)}
            label={v}
            onClick={() => toggleFilter("timeSlots", k)}
          />
        ))}
      </div>

      <div className="w-px h-5 bg-gray-200 shrink-0" />

      {/* 계절 */}
      <div className="flex gap-1.5 items-center shrink-0">
        <span className="text-[11px] text-gray-400 font-semibold tracking-wide mr-0.5">계절</span>
        {Object.entries(SEASON_LABELS).map(([k, v]) => (
          <Chip
            key={k}
            active={filters.seasons.includes(k as Season)}
            label={v}
            onClick={() => toggleFilter("seasons", k)}
          />
        ))}
      </div>

      {count > 0 && (
        <>
          <div className="w-px h-5 bg-gray-200 shrink-0" />
          <button
            onClick={clearFilters}
            className="text-xs text-red-400 hover:text-red-500 font-medium whitespace-nowrap shrink-0"
          >
            ✕ 초기화 ({count})
          </button>
        </>
      )}
    </div>
  );
}