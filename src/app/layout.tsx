import "@/styles/globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "동네 사용설명서 — 주민이 만드는 생활지도",
  description: "PGIS 기반 주민 참여형 동네 생활경험 공유 플랫폼. 쉬기 좋은 곳, 걷기 좋은 길, 기다리기 좋은 장소를 함께 기록합니다.",
  openGraph: {
    title: "동네 사용설명서",
    description: "지도에는 없지만, 주민은 알고 있는 장소들",
    type: "website",
  },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ko">
      <head>
        <link
          rel="stylesheet"
          href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
          crossOrigin=""
        />
      </head>
      <body>{children}</body>
    </html>
  );
}