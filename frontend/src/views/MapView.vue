<template>
  <section class="view active">
    <MockMap
      :pois="pois"
      :visible-ids="visibleIds"
      :selected-ids="state.selectedIds"
      :marked-ids="state.markedIds"
      :favorite-ids="state.favoriteIds"
      @select="openDetail"
    />

    <SearchBar
      @search="onSearch"
      @clear="keyword = ''"
    />

    <button class="fab theme-btn glass" title="切换深浅色" @click="toggleTheme">
      <svg viewBox="0 0 24 24">
        <path d="M21 12.8A9 9 0 1 1 11.2 3 7 7 0 0 0 21 12.8Z" />
      </svg>
    </button>

    <MapSidebar
      :filter-open="filterOpen"
      :mark-active="markMode"
      :types="types"
      :districts="districts"
      :selected-pois="selectedPois"
      :total-count="state.selectedIds.length"
      @toggle-filter="filterOpen = !filterOpen"
      @toggle-mark="toggleMarkMode"
      @toggle-type="toggleIn(types, $event)"
      @toggle-district="toggleIn(districts, $event)"
      @remove="onRemove"
      @clear="onClear"
      @locate="openDetail"
    />

    <button class="fab reset-btn glass" title="复位视角" @click="onReset">
      <svg viewBox="0 0 24 24">
        <path d="M3 12a9 9 0 1 0 3-6.7L3 8" />
        <path d="M3 3v5h5" />
      </svg>
    </button>

    <DetailCard
      :poi="currentPoi"
      :selected="isSelected"
      :marked="isMarked"
      @add="onAdd"
      @nearby="onNearby"
      @mark="onMark"
    />
  </section>
</template>

<script setup>
import { computed, onMounted, ref } from "vue"
import MockMap from "../components/MockMap.vue"
import SearchBar from "../components/SearchBar.vue"
import MapSidebar from "../components/MapSidebar.vue"
import DetailCard from "../components/DetailCard.vue"
import { fetchNearby, fetchPois } from "../api/poi"
import {
  addSelected,
  clearSelected,
  removeSelected,
  showToast,
  state,
  toggleMarked,
  toggleTheme,
} from "../stores/trip"

const pois = ref([])
const types = ref([])
const districts = ref([])
const keyword = ref("")
const filterOpen = ref(false)
const markMode = ref(false)
const currentPoi = ref(null)

onMounted(async () => {
  try {
    const res = await fetchPois({ page_size: 100 })
    pois.value = res.data.items
  } catch (e) {
    showToast(e.message)
  }
})

const visibleIds = computed(() => {
  let list = pois.value
  if (markMode.value) {
    return list
      .filter((p) => state.markedIds.includes(p.poi_id))
      .map((p) => p.poi_id)
  }
  return list
    .filter((p) => {
      if (types.value.length && !types.value.includes(p.type))
        return false
      if (
        districts.value.length &&
        !districts.value.includes(p.district)
      )
        return false
      if (keyword.value && !p.name.includes(keyword.value))
        return false
      return true
    })
    .map((p) => p.poi_id)
})

const selectedPois = computed(() =>
  state.selectedIds
    .map((id) => pois.value.find((p) => p.poi_id === id))
    .filter(Boolean)
)

const isSelected = computed(() =>
  currentPoi.value
    ? state.selectedIds.includes(currentPoi.value.poi_id)
    : false
)

const isMarked = computed(() =>
  currentPoi.value
    ? state.markedIds.includes(currentPoi.value.poi_id)
    : false
)

function onMark(poi) {
  toggleMarked(poi.poi_id)
  const on = state.markedIds.includes(poi.poi_id)
  showToast(on ? `已标记「${poi.name}」` : `已取消标记「${poi.name}」`)
}

function toggleIn(list, value) {
  const i = list.value.indexOf(value)
  if (i >= 0) list.value.splice(i, 1)
  else list.value.push(value)
}

function toggleMarkMode() {
  markMode.value = !markMode.value
  showToast(markMode.value ? "标记模式：仅显示我的标记" : "已退出标记模式")
}

function onSearch(kw) {
  keyword.value = kw
}

function openDetail(poi) {
  currentPoi.value = poi
}

function onAdd(poi) {
  addSelected(poi.poi_id)
  const n = state.selectedIds.length
  if (n >= 15 && n % 5 === 0) {
    showToast(`已选择 ${n} 个点位，数量较多，可能影响单日游览体验`)
  } else {
    showToast(`已添加「${poi.name}」`)
  }
}

function onRemove(id) {
  removeSelected(id)
  if (currentPoi.value?.poi_id === id) currentPoi.value = null
}

function onClear() {
  if (!state.selectedIds.length) {
    showToast("清单已经是空的")
    return
  }
  clearSelected()
  showToast("已清空全部待选点位")
}

async function onNearby(poi) {
  try {
    const res = await fetchNearby(poi.poi_id, 1000)
    const items = res.data
    if (!items.length) {
      showToast("周边 1 公里内暂无收录点位")
      return
    }
    const names = items.slice(0, 3).map((x) => x.name).join("、")
    showToast(
      `周边 1 公里内有 ${items.length} 个点位：${names}` +
        (items.length > 3 ? " 等" : "")
    )
  } catch (e) {
    showToast(e.message)
  }
}

function onReset() {
  showToast("视角已复位至南昌全域")
}
</script>

<style scoped>
.fab {
  position: absolute;
  z-index: 25;
  width: 44px;
  height: 44px;
  border-radius: var(--r-m);
  display: grid;
  place-items: center;
}
.fab svg {
  width: 19px;
  height: 19px;
  stroke: var(--text-2);
  fill: none;
  stroke-width: 1.9;
  stroke-linecap: round;
  stroke-linejoin: round;
}
.theme-btn {
  right: 18px;
  top: 16px;
}
.reset-btn {
  right: 18px;
  bottom: 108px;
}
.fab:active {
  transform: scale(0.94);
}
</style>
