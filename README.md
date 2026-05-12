# 🗺️ 동네 사용설명서

**지도에는 없지만, 주민은 알고 있는 장소들**

PGIS(Participatory GIS) 기반 주민 참여형 동네 생활경험 공유 플랫폼

## 시작하기

```bash
npm install
npm run dev
```

http://localhost:3000 에서 확인

## Vercel 배포

1. 이 저장소를 GitHub에 push
2. [vercel.com](https://vercel.com) → New Project → Import
3. Framework Preset: **Next.js** (자동 감지)
4. Deploy 클릭 → 완료!

> 환경변수 설정 불필요. 바로 배포됩니다.

## 주요 기능

| 기능 | 설명 |
|------|------|
| 🗺️ 지도 메인 | 전체화면 Leaflet 지도 + CartoDB 타일 |
| 📍 장소 등록 | 지도 클릭 → 유형/시간대/계절/태그/설명 입력 |
| 🔍 필터 검색 | 6개 유형 × 4개 시간대 × 5개 계절 조합 |
| ❤️ 공감하기 | 별점 대신 공감 버튼 |
| 📝 정보 보완 | "신고" 대신 추가 정보 남기기 |
| 🗂️ 추천 코스 | 장소를 연결한 테마별 코스 |

## 기술 스택

- **Framework**: Next.js 14 (App Router)
- **State**: Zustand
- **Map**: Leaflet + react-leaflet
- **Style**: Tailwind CSS
- **Deploy**: Vercel

## 프로젝트 구조

```
src/
├── app/
│   ├── layout.tsx
│   └── page.tsx
├── components/
│   ├── TopBar.tsx
│   ├── FilterBar.tsx
│   ├── MapView.tsx
│   ├── SidePanel.tsx
│   ├── PlaceDetail.tsx
│   ├── AddPlaceForm.tsx
│   ├── CoursePanel.tsx
│   └── AboutPanel.tsx
├── lib/
│   ├── types.ts
│   └── store.ts
└── styles/
    └── globals.css
```