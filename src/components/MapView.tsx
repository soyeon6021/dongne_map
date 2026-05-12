"use client";

import { MapContainer, TileLayer, Marker, useMapEvents } from "react-leaflet";
import L from "leaflet";
import { useStore } from "@/lib/store";
import { PLACE_TYPES, PlaceType } from "@/lib/types";

function icon(type: PlaceType) {
  const t = PLACE_TYPES[type];
  return L.divIcon({
    className: "",
    html: `<div class="custom-marker" style="background:${t.color}">${t.emoji}</div>`,
    iconSize: [38, 38],
    iconAnchor: [19, 19],
  });
}

const pinIcon = L.divIcon({
  className: "",
  html: `<div class="custom-marker new-pin" style="background:#ef4444">📍</div>`,
  iconSize: [38, 38],
  iconAnchor: [19, 19],
});

function ClickHandler() {
  const { isAddingPlace, setNewPlaceCoords, setPanel } = useStore();
  useMapEvents({
    click(e) {
      if (isAddingPlace) {
        setNewPlaceCoords({ lat: e.latlng.lat, lng: e.latlng.lng });
        setPanel("add");
      }
    },
  });
  return null;
}

export default function MapView() {
  const { filteredPlaces, selectPlace, isAddingPlace, newPlaceCoords } = useStore();
  const places = filteredPlaces();

  return (
    <MapContainer center={[37.567, 126.979]} zoom={15} className="w-full h-full" zoomControl={false}>
      <TileLayer
        attribution='&copy; <a href="https://carto.com/">CARTO</a>'
        url="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png"
      />
      <ClickHandler />

      {places.map((p) => (
        <Marker
          key={p.id}
          position={[p.lat, p.lng]}
          icon={icon(p.type)}
          eventHandlers={{ click: () => selectPlace(p) }}
        />
      ))}

      {newPlaceCoords && (
        <Marker position={[newPlaceCoords.lat, newPlaceCoords.lng]} icon={pinIcon} />
      )}

      {isAddingPlace && (
        <div className="absolute top-4 left-1/2 -translate-x-1/2 z-[1000] bg-yellow-50/95 backdrop-blur border border-yellow-300 text-yellow-800 px-5 py-2.5 rounded-xl text-sm font-semibold shadow-lg pointer-events-none">
          📍 지도에서 등록할 위치를 클릭하세요
        </div>
      )}
    </MapContainer>
  );
}