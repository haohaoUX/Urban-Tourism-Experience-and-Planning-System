<template>
  <div class="map-stage">
    <svg
      class="map-svg"
      viewBox="0 0 1200 800"
      preserveAspectRatio="xMidYMid slice"
      aria-hidden="true"
    >
      <rect width="1200" height="800" fill="var(--map-bg)" />
      <!-- 街区方块 -->
      <g>
        <rect class="block" x="430" y="60" width="120" height="90" rx="8" />
        <rect class="block" x="580" y="90" width="150" height="70" rx="8" />
        <rect class="block" x="470" y="240" width="130" height="100" rx="8" />
        <rect class="block" x="640" y="260" width="110" height="120" rx="8" />
        <rect class="block" x="450" y="520" width="140" height="80" rx="8" />
        <rect class="block" x="620" y="560" width="120" height="90" rx="8" />
        <rect class="block" x="930" y="180" width="130" height="100" rx="8" />
        <rect class="block" x="950" y="620" width="140" height="80" rx="8" />
        <rect class="block" x="80" y="120" width="120" height="100" rx="8" />
        <rect class="block" x="60" y="480" width="130" height="90" rx="8" />
      </g>
      <!-- 绿地 -->
      <path class="green" d="M470 250 Q520 220 570 260 Q560 320 490 320 Q455 295 470 250 Z" />
      <path class="green" d="M60 470 Q120 440 200 480 Q190 560 90 560 Q45 520 60 470 Z" />
      <path class="green" d="M740 600 Q830 570 900 620 Q880 700 770 700 Q720 660 740 600 Z" />
      <!-- 水域 -->
      <ellipse class="water" cx="792" cy="304" rx="108" ry="72" />
      <ellipse class="water" cx="1015" cy="525" rx="58" ry="88" />
      <!-- 赣江（双层） -->
      <path class="river" d="M360 -40 C300 150 420 280 330 420 C260 540 360 680 300 840" stroke-width="92" />
      <path class="river2" d="M360 -40 C300 150 420 280 330 420 C260 540 360 680 300 840" stroke-width="34" />
      <!-- 主路 -->
      <path class="road" d="M-20 200 L1220 240" stroke-width="9" />
      <path class="road" d="M-20 460 L1220 430" stroke-width="11" />
      <path class="road" d="M-20 660 L1220 700" stroke-width="8" />
      <path class="road" d="M200 -20 L240 820" stroke-width="9" />
      <path class="road" d="M560 -20 L520 820" stroke-width="10" />
      <path class="road" d="M880 -20 L920 820" stroke-width="9" />
      <!-- 次路 -->
      <path class="road2" d="M100 800 L700 60" stroke-width="5" />
      <path class="road2" d="M600 820 L1100 100" stroke-width="5" />
      <path class="road2" d="M-20 340 L1220 350" stroke-width="5" />
      <path class="road2" d="M700 -20 L680 820" stroke-width="5" />
      <!-- 边界 -->
      <path class="boundary" d="M520 -20 L500 820" />
      <path class="boundary" d="M-20 560 L1220 580" />
    </svg>

    <div class="markers-layer">
      <button
        v-for="poi in pois"
        :key="poi.poi_id"
        class="marker"
        :class="[
          poi.type,
          {
            hidden: !visibleIds.includes(poi.poi_id),
            selected: selectedIds.includes(poi.poi_id),
            marked: markedIds.includes(poi.poi_id),
            favored: favoriteIds.includes(poi.poi_id),
          },
        ]"
        :style="{ left: layout(poi).x + '%', top: layout(poi).y + '%' }"
        @click="$emit('select', poi)"
        @mouseenter="hoverId = poi.poi_id"
        @mouseleave="hoverId = null"
      >
        <span class="pin">
          <svg viewBox="0 0 24 24" class="pin-ico">
            <path :d="ICON_PATH[poi.type]" />
          </svg>
        </span>
        <span v-if="hoverId === poi.poi_id" class="tip">{{ poi.name }}</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue"
import { MOCK_LAYOUT } from "../utils/mockLayout"
import { project } from "../utils/projection"

defineProps({
  pois: { type: Array, default: () => [] },
  visibleIds: { type: Array, default: () => [] },
  selectedIds: { type: Array, default: () => [] },
  markedIds: { type: Array, default: () => [] },
  favoriteIds: { type: Array, default: () => [] },
})
defineEmits(["select"])

const hoverId = ref(null)

const ICON_PATH = {
  spot: "M12 3.5 14.4 9l6 .7-4.5 4.1 1.2 5.9L12 16.9l-5.1 2.8 1.2-5.9L3.6 9.7l6-.7L12 3.5Z",
  food: "M7 3v7M5 3v7a2 2 0 004 0V3M7 10v11M17 3c-2 1.5-2.5 4-2.5 7s.5 5 2.5 5v6",
  leisure: "M6 8h12l-1 12H7L6 8ZM9 8V6a3 3 0 016 0v2",
  facility: "M12 8h.01M11 12h1v4h1M12 3a9 9 0 100 18 9 9 0 000-18Z",
}

function layout(poi) {
  if (MOCK_LAYOUT[poi.poi_id]) return MOCK_LAYOUT[poi.poi_id]
  const p = project(Number(poi.longitude), Number(poi.latitude))
  return { x: p.x, y: p.y }
}
</script>

<style scoped>
.map-stage {
  position: absolute;
  inset: 0;
  background: var(--map-bg);
}
.map-svg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
}
.map-svg .road {
  fill: none;
  stroke: var(--map-road);
  stroke-linecap: round;
}
.map-svg .road2 {
  fill: none;
  stroke: var(--map-road-2);
  stroke-linecap: round;
}
.map-svg .block {
  fill: var(--map-block);
}
.map-svg .green {
  fill: var(--map-green);
}
.map-svg .water {
  fill: var(--map-water);
}
.map-svg .river {
  fill: none;
  stroke: var(--map-water);
  stroke-linecap: round;
}
.map-svg .river2 {
  fill: none;
  stroke: var(--map-water-2);
  stroke-linecap: round;
}
.map-svg .boundary {
  fill: none;
  stroke: var(--map-boundary);
  stroke-dasharray: 6 8;
}
.markers-layer {
  position: absolute;
  inset: 0;
}

.marker {
  position: absolute;
  width: 30px;
  height: 30px;
  transform: translate(-50%, -50%);
  display: grid;
  place-items: center;
  transition: opacity 0.25s var(--ease);
}
.pin {
  width: 26px;
  height: 26px;
  border-radius: 50%;
  border: 2.5px solid #fff;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.25);
  display: grid;
  place-items: center;
  transition: transform 0.2s var(--spring);
  background: var(--pin-color, var(--c-spot));
}
.marker.spot .pin {
  background: var(--c-spot);
}
.marker.food .pin {
  background: var(--c-food);
}
.marker.leisure .pin {
  background: var(--c-leisure);
}
.marker.facility {
  width: 22px;
  height: 22px;
}
.marker.facility .pin {
  width: 18px;
  height: 18px;
  border-width: 2px;
  background: var(--c-facility);
}
.pin-ico {
  width: 13px;
  height: 13px;
  stroke: #fff;
  fill: none;
  stroke-width: 2;
  stroke-linecap: round;
  stroke-linejoin: round;
}
.marker.facility .pin-ico {
  width: 10px;
  height: 10px;
}
.marker:hover .pin,
.marker.selected .pin {
  transform: scale(1.18);
}
.marker.marked::after {
  content: "";
  position: absolute;
  inset: -5px;
  border-radius: 50%;
  border: 2px solid var(--accent);
  animation: pulse 1.6s ease-in-out infinite;
}
@keyframes pulse {
  0%,
  100% {
    opacity: 0.9;
    transform: scale(1);
  }
  50% {
    opacity: 0.3;
    transform: scale(1.12);
  }
}
.marker.hidden {
  opacity: 0;
  pointer-events: none;
  transform: translate(-50%, -50%) scale(0.5);
}
.tip {
  position: absolute;
  bottom: calc(100% + 6px);
  left: 50%;
  transform: translateX(-50%);
  white-space: nowrap;
  background: var(--glass-bg-strong);
  backdrop-filter: var(--blur);
  -webkit-backdrop-filter: var(--blur);
  font-size: 12px;
  font-weight: 500;
  padding: 5px 10px;
  border-radius: 8px;
  box-shadow: var(--shadow-s);
  border: 1px solid var(--glass-border);
}
</style>
