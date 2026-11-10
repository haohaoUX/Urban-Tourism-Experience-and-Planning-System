<template>
  <div class="view map-view">
    <!-- 顶部 -->
    <header class="top">
      <div class="title-row">
        <h1>洪城漫游</h1>
        <button class="theme-btn" @click="toggleTheme">
          <svg viewBox="0 0 24 24" width="18" height="18">
            <path
              fill="currentColor"
              d="M12 18a6 6 0 100-12 6 6 0 000 12zM11 1h2v3h-2zm0 19h2v3h-2zM3.5 4.9l1.4-1.4 2.1 2.1-1.4 1.4zm13.5 13.5l2.1 2.1 1.4-1.4-2.1-2.1zM1 11h3v2H1zm19 0h3v2h-3zM3.5 19.1l2.1-2.1 1.4 1.4-2.1 2.1zM17 7l2.1-2.1 1.4 1.4-2.1 2.1z"
            />
          </svg>
        </button>
      </div>
      <SearchBox @search="onSearch" @clear="onSearch('')" />
    </header>

    <MockMap
      :pois="visiblePois"
      :selected-ids="state.selectedIds"
      :marked-ids="state.markedIds"
      :favorite-ids="state.favoriteIds"
      @select="openDetail"
    />

    <MapControls
      :filter-active="filterActive"
      :mark-active="markMode"
      @toggle-filter="toggleFilterPanel"
      @toggle-mark="toggleMarkMode"
    />

    <FilterPanel
      :open="filterOpen"
      :types="types"
      :districts="districts"
      @toggle-type="toggleType"
      @toggle-district="toggleDistrict"
      @reset="resetFilter"
      @close="filterOpen = false"
    />

    <POIDetail
      :poi="currentPoi"
      :selected="isSelected"
      :marked="isMarked"
      :favored="isFavored"
      @close="currentPoi = null"
      @toggle-add="onToggleAdd"
      @toggle-mark="onToggleMark"
      @toggle-favorite="onToggleFavorite"
    />
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from "vue"
import MockMap from "../components/MockMap.vue"
import MapControls from "../components/MapControls.vue"
import FilterPanel from "../components/FilterPanel.vue"
import POIDetail from "../components/POIDetail.vue"
import SearchBox from "../components/SearchBox.vue"
import { fetchPois } from "../api/poi"
import {
  addSelected,
  removeSelected,
  showToast,
  state,
  toggleFavorite,
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

const filterActive = computed(
  () =>
    types.value.length > 0 ||
    districts.value.length > 0 ||
    keyword.value !== ""
)

const visiblePois = computed(() => {
  if (markMode.value) {
    return pois.value.filter((p) =>
      state.markedIds.includes(p.poi_id)
    )
  }
  return pois.value.filter((p) => {
    if (types.value.length && !types.value.includes(p.type))
      return false
    if (
      districts.value.length &&
      !districts.value.includes(p.district)
    )
      return false
    if (
      keyword.value &&
      !p.name.includes(keyword.value)
    )
      return false
    return true
  })
})

function toggleInList(list, value) {
  const i = list.value.indexOf(value)
  if (i >= 0) list.value.splice(i, 1)
  else list.value.push(value)
}
const toggleType = (t) => toggleInList(types, t)
const toggleDistrict = (d) => toggleInList(districts, d)
function resetFilter() {
  types.value = []
  districts.value = []
  keyword.value = ""
}

function toggleFilterPanel() {
  filterOpen.value = !filterOpen.value
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
const isFavored = computed(() =>
  currentPoi.value
    ? state.favoriteIds.includes(currentPoi.value.poi_id)
    : false
)

function onToggleAdd(poi) {
  if (state.selectedIds.includes(poi.poi_id)) {
    removeSelected(poi.poi_id)
    showToast("已从待选清单移除")
    return
  }
  addSelected(poi.poi_id)
  const n = state.selectedIds.length
  if (n >= 15 && n % 5 === 0) {
    showToast(`已选 ${n} 个点位，行程较满，注意合理安排时间`)
  } else {
    showToast("已加入待选清单")
  }
}
function onToggleMark(poi) {
  toggleMarked(poi.poi_id)
  showToast(
    state.markedIds.includes(poi.poi_id) ? "已标记" : "已取消标记"
  )
}
function onToggleFavorite(poi) {
  toggleFavorite(poi.poi_id)
  showToast(
    state.favoriteIds.includes(poi.poi_id) ? "已收藏" : "已取消收藏"
  )
}
</script>

<style scoped>
.top {
  position: absolute;
  top: 14px;
  left: 14px;
  right: 14px;
  z-index: 25;
}
.title-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}
h1 {
  font-size: 24px;
  letter-spacing: 1px;
}
.theme-btn {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-2);
}
</style>
