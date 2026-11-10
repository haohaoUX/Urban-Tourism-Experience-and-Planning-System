<template>
  <aside class="sidebar">
    <div class="sb-buttons">
      <button
        class="sb-btn"
        :class="{ on: filterOpen }"
        @click="$emit('toggle-filter')"
      >
        <svg viewBox="0 0 24 24">
          <path d="M3 5h18M6 12h12M10 19h4" />
        </svg>
        筛选
      </button>
      <button
        class="sb-btn"
        :class="{ on: markActive }"
        @click="$emit('toggle-mark')"
      >
        <svg viewBox="0 0 24 24">
          <path d="M12 21s-7-5.5-7-11a7 7 0 0 1 14 0c0 5.5-7 11-7 11Z" />
          <circle cx="12" cy="10" r="2.5" />
        </svg>
        标记
      </button>
    </div>

    <FilterPanel
      :open="filterOpen"
      :types="types"
      :districts="districts"
      @toggle-type="$emit('toggle-type', $event)"
      @toggle-district="$emit('toggle-district', $event)"
    />

    <SelectedPanel
      :pois="selectedPois"
      :total-count="totalCount"
      @remove="$emit('remove', $event)"
      @clear="$emit('clear')"
      @locate="$emit('locate', $event)"
    />
  </aside>
</template>

<script setup>
import FilterPanel from "./FilterPanel.vue"
import SelectedPanel from "./SelectedPanel.vue"

defineProps({
  filterOpen: Boolean,
  markActive: Boolean,
  types: Array,
  districts: Array,
  selectedPois: Array,
  totalCount: Number,
})
defineEmits([
  "toggle-filter",
  "toggle-mark",
  "toggle-type",
  "toggle-district",
  "remove",
  "clear",
  "locate",
])
</script>

<style scoped>
.sidebar {
  position: absolute;
  left: 16px;
  top: 72px;
  bottom: 96px;
  width: 236px;
  z-index: 20;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.sb-buttons {
  display: flex;
  gap: 8px;
}
.sb-btn {
  flex: 1;
  height: 46px;
  border-radius: var(--r-m);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 2px;
  font-size: 12px;
  font-weight: 500;
  color: var(--text-2);
  background: var(--glass-bg);
  backdrop-filter: var(--blur);
  -webkit-backdrop-filter: var(--blur);
  border: 1px solid var(--glass-border);
  box-shadow: var(--shadow-s);
  transition: all 0.2s var(--ease);
}
.sb-btn svg {
  width: 18px;
  height: 18px;
  stroke: currentColor;
  fill: none;
  stroke-width: 1.8;
  stroke-linecap: round;
  stroke-linejoin: round;
}
.sb-btn:active {
  transform: scale(0.96);
}
.sb-btn.on {
  background: var(--accent);
  color: #fff;
  border-color: transparent;
  box-shadow: 0 6px 16px rgba(10, 132, 255, 0.35);
}
</style>
