<template>
  <div class="selected-panel glass">
    <div class="sp-head">
      <span class="sp-title">待选点位</span>
      <span class="sp-count">已选择：{{ totalCount }} 个</span>
    </div>

    <div class="sp-tools">
      <button
        v-for="f in FILTERS"
        :key="f.value"
        class="mini-chip"
        :class="{ on: listFilter === f.value }"
        @click="listFilter = f.value"
      >
        {{ f.label }}
      </button>
    </div>

    <div class="sp-list">
      <p v-if="!totalCount" class="sp-empty">
        还没有选择点位<br />点击地图上的点位添加
      </p>
      <p v-else-if="!filtered.length" class="sp-empty">
        该类型下暂无点位
      </p>
      <div
        v-for="(poi, i) in filtered"
        :key="poi.poi_id"
        class="sp-item"
        @click="$emit('locate', poi)"
      >
        <span class="dot" :class="poi.type" />
        <div class="meta">
          <div class="nm">{{ poi.name }}</div>
          <div class="ty">{{ typeLabel(poi.type) }} · {{ poi.district }}</div>
        </div>
        <button class="del" @click.stop="$emit('remove', poi.poi_id)">
          <svg viewBox="0 0 24 24">
            <path d="M18 6 6 18M6 6l18 18" />
          </svg>
        </button>
      </div>
    </div>

    <div class="sp-foot">
      <button class="text-btn" @click="$emit('clear')">一键清空</button>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from "vue"

const FILTERS = [
  { value: "all", label: "全部" },
  { value: "spot", label: "景点" },
  { value: "food", label: "美食" },
  { value: "leisure", label: "休闲" },
]
const listFilter = ref("all")

const props = defineProps({
  pois: { type: Array, default: () => [] },
  totalCount: Number,
})
defineEmits(["remove", "clear", "locate"])

const filtered = computed(() =>
  listFilter.value === "all"
    ? props.pois
    : props.pois.filter((p) => p.type === listFilter.value)
)

const TYPE_LABELS = {
  spot: "景点",
  food: "正餐美食",
  leisure: "休闲",
  facility: "配套",
}
const typeLabel = (t) => TYPE_LABELS[t]
</script>

<style scoped>
.selected-panel {
  flex: 1;
  min-height: 0;
  border-radius: var(--r-l);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
.sp-head {
  padding: 13px 14px 10px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex: none;
}
.sp-title {
  font-size: 14px;
  font-weight: 600;
}
.sp-count {
  font-size: 12px;
  color: var(--text-2);
  background: var(--glass-inner);
  padding: 3px 9px;
  border-radius: 11px;
}
.sp-tools {
  display: flex;
  gap: 6px;
  padding: 0 12px 10px;
  flex: none;
}
.mini-chip {
  font-size: 11.5px;
  color: var(--text-2);
  padding: 4px 10px;
  border-radius: 12px;
  background: var(--glass-inner);
  transition: all 0.15s var(--ease);
}
.mini-chip.on {
  background: var(--accent-soft);
  color: var(--accent);
}
.sp-list {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  padding: 0 10px 10px;
  display: flex;
  flex-direction: column;
  gap: 7px;
}
.sp-empty {
  text-align: center;
  color: var(--text-3);
  font-size: 12.5px;
  padding: 34px 10px;
  line-height: 1.8;
}
.sp-item {
  border-radius: var(--r-m);
  background: var(--glass-inner);
  padding: 9px 10px;
  display: flex;
  align-items: center;
  gap: 9px;
  transition: transform 0.18s var(--ease), box-shadow 0.18s var(--ease);
  cursor: pointer;
}
.sp-item:hover {
  transform: translateY(-1px);
  box-shadow: var(--shadow-s);
}
.dot {
  width: 9px;
  height: 9px;
  border-radius: 50%;
  flex: none;
}
.dot.spot {
  background: var(--c-spot);
}
.dot.food {
  background: var(--c-food);
}
.dot.leisure {
  background: var(--c-leisure);
}
.dot.facility {
  background: var(--c-facility);
}
.meta {
  flex: 1;
  min-width: 0;
}
.nm {
  font-size: 13px;
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.ty {
  font-size: 11px;
  color: var(--text-2);
  margin-top: 1px;
}
.del {
  width: 22px;
  height: 22px;
  border-radius: 7px;
  display: grid;
  place-items: center;
  flex: none;
}
.del svg {
  width: 13px;
  height: 13px;
  stroke: var(--text-2);
  fill: none;
  stroke-width: 2;
  stroke-linecap: round;
}
.del:hover {
  background: rgba(255, 59, 48, 0.12);
}
.del:hover svg {
  stroke: var(--danger);
}
.sp-foot {
  padding: 10px 12px 12px;
  flex: none;
}
.text-btn {
  font-size: 12px;
  color: var(--danger);
  width: 100%;
  padding: 7px;
  border-radius: 10px;
  background: var(--glass-inner);
  transition: all 0.15s;
}
.text-btn:active {
  transform: scale(0.97);
}
</style>
