"use client";

import dynamic from "next/dynamic";
import TopBar from "@/components/TopBar";
import FilterBar from "@/components/FilterBar";
import SidePanel from "@/components/SidePanel";
import { useStore } from "@/lib/store";

const MapView = dynamic(() => import("@/components/MapView"), { ssr: false });

export default function Home() {
  const panel = useStore((s) => s.panel);

  return (
    <div className="h-screen w-screen flex flex-col">
      <TopBar />
      <FilterBar />
      <div className="flex-1 relative flex overflow-hidden">
        <div className="flex-1 relative">
          <MapView />
        </div>
        {panel !== "none" && <SidePanel />}
      </div>
    </div>
  );
}