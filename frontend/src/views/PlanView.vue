<template>
  <div class="view plan-view">
    <header class="page-head">
      <h2>路线规划</h2>
    </header>

    <div class="scroll">
      <!-- 待选清单 -->
      <section class="glass block">
        <div class="block-head">
          <h3>待选清单（{{ selectedPois.length }}）</h3>
          <button
            v-if="selectedPois.length"
            class="text-btn"
            @click="clearAll"
          >
            清空
          </button>
        </div>

        <p v-if="!selectedPois.length" class="empty">
          还没有点位，去地图页挑选想前往的地方
        </p>
        <ul v-else class="pick-list">
          <li v-for="(poi, i) in selectedPois" :key="poi.poi_id">
            <span class="seq">{{ i + 1 }}</span>
            <span class="pick-name">{{ poi.name }}</span>
            <span class="pick-type" :class="poi.type">
              {{ typeLabels[poi.type] }}
            </span>
            <button class="x" @click="removeSelected(poi.poi_id)">
              ×
            </button>
          </li>
        </ul>

        <template v-if="selectedPois.length">
          <div class="option">
            <p class="opt-label">生成方式</p>
            <div class="seg">
              <button
                :class="{ on: genMode === 'smart' }"
                @click="genMode = 'smart'"
              >
                顺路最优
              </button>
              <button
                :class="{ on: genMode === 'manual' }"
                @click="genMode = 'manual'"
              >
                清单顺序
              </button>
            </div>
          </div>
          <div class="option">
            <p class="opt-label">出行方式</p>
            <div class="seg">
              <button
                :class="{ on: travelMode === 'driving' }"
                @click="travelMode = 'driving'"
              >
                驾车
              </button>
              <button
                :class="{ on: travelMode === 'walking' }"
                @click="travelMode = 'walking'"
              >
                步行
              </button>
            </div>
          </div>
          <button class="generate" @click="generate">
            生成路线
          </button>
        </template>
      </section>

      <!-- 已生成路线 -->
      <section class="glass block">
        <div class="block-head">
          <h3>我的路线（{{ routes.length }}）</h3>
        </div>
        <p v-if="!routes.length" class="empty">暂无已生成的路线</p>

        <article
          v-for="r in routes"
          :key="r.route_id"
          class="route-card"
        >
          <button class="card-head" @click="toggleExpand(r.route_id)">
            <span class="card-title">
              <input
                v-if="editingId === r.route_id"
                v-model="editingName"
                class="name-input"
                @click.stop
                @keyup.enter="saveName(r)"
              />
              {{ r.name }}
            </span>
            <span class="card-meta">
              {{ r.poi_count }} 点 · {{ r.total_minutes }} 分钟
            </span>
          </button>

          <div v-if="expandedId === r.route_id" class="card-body">
            <ul class="route-items">
              <li
                v-for="it in detailMap[r.route_id]?.items || []"
                :key="it.seq"
              >
                <span class="r-seq">{{ it.seq }}</span>
                {{ it.name }}
                <span class="stay">{{ it.stay_minutes }} 分钟</span>
              </li>
            </ul>
            <div class="card-actions">
              <button @click="startEdit(r)">重命名</button>
              <button @click="onCopy(r.route_id)">复制</button>
              <button class="danger" @click="onDelete(r.route_id)">
                删除
              </button>
            </div>
          </div>
        </article>
      </section>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from "vue"
import { fetchPois } from "../api/poi"
import {
  copyRoute,
  createRoute,
  deleteRoute,
  fetchRoute,
  fetchRoutes,
  renameRoute,
} from "../api/route"
import {
  clearSelected,
  removeSelected,
  showToast,
  state,
} from "../stores/trip"

const typeLabels = {
  spot: "景点",
  food: "美食",
  leisure: "休闲",
  facility: "配套",
}

const allPois = ref([])
const routes = ref([])
const detailMap = ref({})
const genMode = ref("smart")
const travelMode = ref("driving")
const expandedId = ref(null)
const editingId = ref(null)
const editingName = ref("")

onMounted(async () => {
  try {
    const res = await fetchPois({ page_size: 100 })
    allPois.value = res.data.items
    await loadRoutes()
  } catch (e) {
    showToast(e.message)
  }
})

const selectedPois = computed(() =>
  state.selectedIds
    .map((id) => allPois.value.find((p) => p.poi_id === id))
    .filter(Boolean)
)

async function loadRoutes() {
  const res = await fetchRoutes()
  routes.value = res.data
}

function clearAll() {
  clearSelected()
  showToast("已清空待选清单")
}

async function generate() {
  if (!state.selectedIds.length) {
    showToast("请先在地图页添加点位")
    return
  }
  try {
    await createRoute({
      gen_mode: genMode.value,
      travel_mode: travelMode.value,
      poi_ids: state.selectedIds,
    })
    showToast("路线生成成功")
    await loadRoutes()
  } catch (e) {
    showToast(e.message)
  }
}

async function toggleExpand(routeId) {
  if (expandedId.value === routeId) {
    expandedId.value = null
    return
  }
  expandedId.value = routeId
  if (!detailMap.value[routeId]) {
    const res = await fetchRoute(routeId)
    detailMap.value[routeId] = res.data
  }
}

function startEdit(r) {
  editingId.value = r.route_id
  editingName.value = r.name
}
async function saveName(r) {
  const name = editingName.value.trim()
  if (!name) {
    showToast("名称不能为空")
    return
  }
  await renameRoute(r.route_id, name)
  editingId.value = null
  await loadRoutes()
}

async function onCopy(routeId) {
  await copyRoute(routeId)
  showToast("复制成功")
  await loadRoutes()
}
async function onDelete(routeId) {
  await deleteRoute(routeId)
  if (expandedId.value === routeId) expandedId.value = null
  delete detailMap.value[routeId]
  showToast("路线已删除")
  await loadRoutes()
}
</script>

<style scoped>
.page-head {
  padding: 18px 18px 8px;
}
h2 {
  font-size: 24px;
}
.scroll {
  position: absolute;
  top: 70px;
  left: 14px;
  right: 14px;
  bottom: 92px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 14px;
}
.block {
  border-radius: var(--r-lg);
  padding: 16px;
}
.block-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
h3 {
  font-size: 15px;
}
.text-btn {
  font-size: 13px;
  color: var(--brand);
}
.empty {
  margin-top: 12px;
  font-size: 13px;
  color: var(--text-3);
}
.pick-list {
  list-style: none;
  margin-top: 12px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.pick-list li {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 13px;
}
.seq {
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: rgba(58, 123, 213, 0.15);
  color: var(--brand);
  font-size: 11px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.pick-name {
  flex: 1;
}
.pick-type {
  font-size: 11px;
  color: var(--text-3);
}
.pick-type.spot {
  color: var(--c-spot);
}
.pick-type.food {
  color: var(--c-food);
}
.pick-type.leisure {
  color: var(--c-leisure);
}
.x {
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: rgba(128, 140, 155, 0.18);
  font-size: 14px;
}
.option {
  margin-top: 16px;
}
.opt-label {
  font-size: 12px;
  color: var(--text-2);
  margin-bottom: 8px;
}
.seg {
  display: flex;
  background: rgba(128, 140, 155, 0.14);
  border-radius: var(--r-sm);
  padding: 3px;
}
.seg button {
  flex: 1;
  padding: 8px;
  border-radius: var(--r-sm);
  font-size: 13px;
  color: var(--text-2);
}
.seg button.on {
  background: var(--glass-bg-strong);
  color: var(--brand);
  font-weight: 600;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}
.generate {
  margin-top: 16px;
  width: 100%;
  padding: 13px;
  border-radius: var(--r-md);
  background: var(--brand);
  color: #fff;
  font-weight: 600;
}

.route-card {
  margin-top: 10px;
  border-radius: var(--r-md);
  background: rgba(128, 140, 155, 0.1);
  overflow: hidden;
}
.card-head {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 13px 14px;
  text-align: left;
}
.card-title {
  font-size: 14px;
  font-weight: 600;
}
.card-meta {
  font-size: 12px;
  color: var(--text-3);
}
.name-input {
  border: 1px solid var(--brand);
  border-radius: var(--r-sm);
  padding: 4px 8px;
  font-size: 13px;
  background: var(--glass-bg-strong);
  color: var(--text);
}
.card-body {
  padding: 0 14px 14px;
}
.route-items {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 8px;
  font-size: 13px;
}
.r-seq {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: rgba(58, 123, 213, 0.15);
  color: var(--brand);
  font-size: 10px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  margin-right: 6px;
}
.stay {
  margin-left: auto;
  color: var(--text-3);
  font-size: 12px;
}
.route-items li {
  display: flex;
  align-items: center;
}
.card-actions {
  display: flex;
  gap: 8px;
  margin-top: 14px;
}
.card-actions button {
  flex: 1;
  padding: 8px;
  border-radius: var(--r-sm);
  font-size: 12px;
  background: rgba(128, 140, 155, 0.16);
}
.card-actions .danger {
  color: #d9534f;
}
</style>
