<template>
  <div class="mock-map">
    <!-- 底图 -->
    <svg
      class="base"
      viewBox="0 0 100 100"
      preserveAspectRatio="none"
      aria-hidden="true"
    >
      <rect width="100" height="100" class="land" />

      <!-- 行政区底色块 -->
      <polygon class="district" points="0,0 36,0 30,45 0,55" />
      <polygon
        class="district alt"
        points="36,0 100,0 100,30 70,32 45,40 30,45"
      />
      <polygon class="district" points="0,55 30,45 40,70 0,80" />
      <polygon
        class="district alt"
        points="40,70 45,40 100,30 100,100 0,100 0,80"
      />

      <!-- 赣江 -->
      <path
        class="river"
        d="M33 100 C35 82 30 64 35 46 C39 30 37 16 41 0"
      />
      <!-- 青山湖 -->
      <ellipse class="lake" cx="79" cy="34" rx="7" ry="9" />

      <!-- 道路 -->
      <path class="road" d="M8 60 L92 42" />
      <path class="road" d="M14 20 L88 78" />
      <path class="road" d="M50 0 L58 100" />

      <!-- 地名 -->
      <text x="14" y="30" class="place">红谷滩</text>
      <text x="52" y="26" class="place">东湖</text>
      <text x="48" y="58" class="place">西湖</text>
      <text x="70" y="74" class="place">青山湖</text>
      <text x="30" y="90" class="place">青云谱</text>
      <text x="8" y="88" class="place">新建</text>
    </svg>

    <!-- 点位标记 -->
    <button
      v-for="poi in pois"
      :key="poi.poi_id"
      class="marker"
      :class="[
        poi.type,
        {
          selected: selectedIds.includes(poi.poi_id),
          marked: markedIds.includes(poi.poi_id),
          favored: favoriteIds.includes(poi.poi_id),
        },
      ]"
      :style="{ left: pos(poi).x + '%', top: pos(poi).y + '%' }"
      @click="$emit('select', poi)"
    >
      <span class="dot" />
      <span class="marker-name">{{ poi.name }}</span>
    </button>
  </div>
</template>

<script setup>
import { project } from "../utils/projection"

defineProps({
  pois: { type: Array, default: () => [] },
  selectedIds: { type: Array, default: () => [] },
  markedIds: { type: Array, default: () => [] },
  favoriteIds: { type: Array, default: () => [] },
})
defineEmits(["select"])

const pos = (poi) =>
  project(Number(poi.longitude), Number(poi.latitude))
</script>

<style scoped>
.mock-map {
  position: absolute;
  inset: 0;
  overflow: hidden;
}
.base {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
}
.land {
  fill: rgba(120, 150, 180, 0.12);
}
.district {
  fill: rgba(255, 255, 255, 0.18);
}
.district.alt {
  fill: rgba(255, 255, 255, 0.3);
}
.river {
  fill: none;
  stroke: rgba(90, 169, 240, 0.4);
  stroke-width: 7;
  stroke-linecap: round;
}
.lake {
  fill: rgba(90, 169, 240, 0.32);
}
.road {
  fill: none;
  stroke: rgba(120, 130, 145, 0.22);
  stroke-width: 0.6;
}
.place {
  font-size: 4.2px;
  fill: var(--text-3);
  letter-spacing: 1px;
}

.marker {
  position: absolute;
  transform: translate(-50%, -50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 6px;
  z-index: 2;
}
.dot {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  border: 2.5px solid #fff;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.22);
  transition: transform 0.25s var(--ease);
}
.marker.spot .dot {
  background: var(--c-spot);
}
.marker.food .dot {
  background: var(--c-food);
}
.marker.leisure .dot {
  background: var(--c-leisure);
}
.marker.facility .dot {
  background: var(--c-facility);
}
.marker:hover .dot,
.marker.selected .dot {
  transform: scale(1.28);
}
.marker.selected .dot {
  box-shadow:
    0 0 0 5px rgba(58, 123, 213, 0.18),
    0 3px 10px rgba(0, 0, 0, 0.22);
}
.marker.marked .dot {
  outline: 2px dashed var(--brand);
  outline-offset: 2px;
}
.marker-name {
  margin-top: 3px;
  font-size: 11px;
  font-weight: 600;
  color: var(--text);
  background: var(--glass-bg);
  padding: 1px 7px;
  border-radius: var(--r-pill);
  white-space: nowrap;
  opacity: 0;
  transform: translateY(-3px);
  transition: 0.2s var(--ease-soft);
  backdrop-filter: blur(8px);
}
.marker:hover .marker-name,
.marker.selected .marker-name {
  opacity: 1;
  transform: translateY(0);
}
</style>
