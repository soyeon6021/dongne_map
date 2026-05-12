"use client";

export default function AboutPanel() {
  return (
    <div className="p-5 space-y-6 animate-fade-up">
      {/* 히어로 */}
      <div className="bg-gradient-to-br from-primary-50 via-green-50 to-emerald-50 rounded-2xl p-6">
        <h3 className="text-lg font-bold text-gray-800 mb-1.5">🗺️ 동네 사용설명서</h3>
        <p className="text-sm font-semibold text-primary-700 mb-3">
          지도에는 없지만, 주민은 알고 있는 장소들
        </p>
        <p className="text-[13px] text-gray-600 leading-relaxed">
          주민이 직접 쉬기 좋은 곳, 걷기 좋은 길, 기다리기 좋은 장소, 계절별 추천 장소,
          생활 편의 공간을 지도에 기록하며 함께 만들어가는
          <strong> PGIS 기반 생활경험 공유 플랫폼</strong>입니다.
        </p>
      </div>

      {/* PGIS */}
      <section className="space-y-2">
        <h4 className="font-bold text-gray-800 text-[14px]">📌 PGIS란?</h4>
        <p className="text-[13px] text-gray-600 leading-relaxed">
          <strong>PGIS(Participatory GIS)</strong>는 지역 주민과 이용자가 직접 공간정보
          생산 과정에 참여하는 방식입니다. 전문 기관의 데이터가 아니라 주민의 실제 경험이
          데이터가 되어, 동네를 함께 해석하고 이해하는 구조를 만듭니다.
        </p>
      </section>

      {/* 기획 목표 */}
      <section className="space-y-2">
        <h4 className="font-bold text-gray-800 text-[14px]">🎯 기획 목표</h4>
        <ul className="text-[13px] text-gray-600 space-y-1.5 leading-relaxed">
          <li className="flex gap-2"><span className="shrink-0">①</span> 주민의 생활밀착형 장소 정보를 수집하고 공유</li>
          <li className="flex gap-2"><span className="shrink-0">②</span> 시간대·계절·목적별 동네 사용 방식을 시각화</li>
          <li className="flex gap-2"><span className="shrink-0">③</span> 공식 지도에 없는 쉬기 좋은 곳, 걷기 좋은 길 등 생활자원 발굴</li>
          <li className="flex gap-2"><span className="shrink-0">④</span> 주민 참여 데이터로 생활환경 이해를 위한 기초 자료 구축</li>
          <li className="flex gap-2"><span className="shrink-0">⑤</span> 중립적이고 긍정적인 생활정보 공유 플랫폼 지향</li>
        </ul>
      </section>

      {/* 이용자 */}
      <section className="space-y-2">
        <h4 className="font-bold text-gray-800 text-[14px]">👥 이런 분들이 이용해요</h4>
        <div className="grid grid-cols-2 gap-2">
          {[
            { t: "동네 주민", d: "산책길·쉬는 곳·편의 공간 공유", e: "🏠" },
            { t: "방문자", d: "상황별 유용한 장소 탐색", e: "🧳" },
            { t: "청년·학생", d: "공부·산책·만남 장소 확인", e: "📚" },
            { t: "노인", d: "벤치·완만한 길·편의시설 확인", e: "🧓" },
            { t: "지역단체", d: "생활공간 파악·프로그램 기획", e: "🏢" },
            { t: "지자체", d: "생활자원 분포·이용 수요 참고", e: "🏛️" },
          ].map((x) => (
            <div key={x.t} className="bg-gray-50 rounded-xl p-3">
              <div className="text-lg mb-1">{x.e}</div>
              <div className="text-[13px] font-bold text-gray-700">{x.t}</div>
              <div className="text-[11px] text-gray-500 mt-0.5">{x.d}</div>
            </div>
          ))}
        </div>
      </section>

      {/* 운영 원칙 */}
      <section className="space-y-2">
        <h4 className="font-bold text-gray-800 text-[14px]">📏 중립적 운영 원칙</h4>
        <div className="bg-amber-50 border border-amber-200 rounded-xl p-4 space-y-2 text-[13px] text-gray-700">
          <p>🚫 특정 개인·상점에 대한 비방 금지</p>
          <p>🔒 개인정보 보호 (얼굴, 차량번호, 상세 주소)</p>
          <p>✅ 불만 제보보다 장소 활용법·생활 팁 중심</p>
          <p>🔄 "신고하기" 대신 "정보 보완하기" 사용</p>
          <p>📋 부적절한 게시물은 관리자 검토 후 비공개 처리</p>
        </div>
      </section>

      {/* 하단 안내 */}
      <div className="text-center text-xs text-gray-400 pt-2 pb-4">
        PGIS 기반 주민 참여형 웹 지도 플랫폼 · 동네 사용설명서
      </div>
    </div>
  );
}