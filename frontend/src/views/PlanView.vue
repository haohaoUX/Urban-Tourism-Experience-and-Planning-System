<template>
  <section class="view active">
    <div class="plan-wrap">
      <h2 class="plan-title">行程规划</h2>

      <div class="plan-grid">
        <!-- 左列：待选与生成 -->
        <div class="plan-col">
          <div class="plan-card glass">
            <div class="pc-title">
              待选点位
              <span class="sp-count">{{ selectedPois.length }} 个</span>
            </div>

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

            <div class="plan-list">
              <p v-if="!selectedPois.length" class="empty">
                暂无点位，请先在地图页挑选
              </p>
              <div
                v-for="(poi, i) in selectedPois"
                :key="poi.poi_id"
                class="plan-item"
              >
                <span class="dot" :class="poi.type" />
                <span class="idx">{{ i + 1 }}</span>
                <span class="nm">{{ poi.name }}</span>
                <button
                  class="del"
                  @click="removeSelected(poi.poi_id)"
                >
                  ×
                </button>
              </div>
            </div>
          </div>

          <button class="generate-btn" @click="generate">
            <svg viewBox="0 0 24 24">
              <path d="M5 12h14M13 6l6 6-6 6" />
            </svg>
            一键生成路线
          </button>
        </div>

        <!-- 右列：已生成路线 -->
        <div class="plan-col">
          <div class="pc-title">已生成路线</div>
          <p v-if="!routes.length" class="empty">暂无已生成的路线</p>

          <div class="route-cards">
            <article
              v-for="(r, ri) in routes"
              :key="r.route_id"
              class="route-card glass"
              :class="{ open: openId === r.route_id }"
            >
              <div class="rc-head" @click="toggleOpen(r.route_id)">
                <div class="rc-order">{{ ri + 1 }}</div>
                <div class="rc-meta">
                  <input
                    :value="r.name"
                    class="rc-name"
                    @click.stop
                    @change="onRename(r, $event)"
                  />
                  <div class="rc-count">
                    {{ r.poi_count }} 个点位 ·
                    {{ r.gen_mode === "smart" ? "顺路最优" : "清单顺序" }}
                  </div>
                </div>
                <button
                  class="rc-icon"
                  @click.stop="onCopy(r.route_id)"
                >
                  <svg viewBox="0 0 24 24">
                    <rect x="8" y="8" width="13" height="13" rx="3" />
                    <path d="M16 8V6a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h2" />
                  </svg>
                </button>
                <button
                  class="rc-icon"
                  @click.stop="onDelete(r.route_id)"
                >
                  <svg viewBox="0 0 24 24">
                    <path d="M4 7h16M9 7V5a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2m-9 0 1 13h8l1-13" />
                  </svg>
                </button>
                <span class="rc-chevron">
                  <svg viewBox="0 0 24 24">
                    <path d="m6 9 6 6 6-6" />
                  </svg>
                </span>
              </div>

              <div v-if="openId === r.route_id" class="rc-body">
                <div class="rc-summary">
                  <span class="chip">预估 {{ fmt(r.total_minutes) }}</span>
                  <span class="chip">
                    {{ travelMode === "driving" ? "驾车" : "步行" }}估算
                  </span>
                </div>

                <div class="mini-map">
                  <svg viewBox="0 0 100 100" preserveAspectRatio="none">
                    <rect width="100" height="100" fill="var(--map-bg)" />
                    <path
                      d="M30 -5 C25 20 35 35 27 52 C21 66 30 82 25 105"
                      fill="none"
                      stroke="var(--map-water)"
                      stroke-width="8"
                    />
                    <polyline
                      class="mm-line"
                      :points="linePoints(r)"
                    />
                    <circle
                      v-for="it in detailMap[r.route_id]?.items || []"
                      :key="'c' + it.seq"
                      class="mm-dot"
                      :cx="xy(it.poi_id).x"
                      :cy="xy(it.poi_id).y"
                      r="3.4"
                      :fill="colorOf(it.poi_id)"
                    />
                    <text
                      v-for="(it, i) in detailMap[r.route_id]?.items || []"
                      :key="'t' + it.seq"
                      class="mm-num"
                      :x="xy(it.poi_id).x"
                      :y="xy(it.poi_id).y + 0.4"
                    >
                      {{ i + 1 }}
                    </text>
                  </svg>
                </div>

                <div class="itinerary">
                  <div
                    v-for="(it, i) in detailMap[r.route_id]?.items || []"
                    :key="it.seq"
                    class="it-item"
                  >
                    <span
                      class="seq"
                      :style="{ background: colorOf(it.poi_id) }"
                    >
                      {{ i + 1 }}
                    </span>
                    <div class="it-meta">
                      <div class="it-nm">{{ it.name }}</div>
                      <div class="it-sub">
                        停留约 {{ it.stay_minutes || "—" }} 分钟
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </article>
          </div>
        </div>
      </div>
    </div>
  </section>
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
import { removeSelected, showToast, state } from "../stores/trip"
import { MOCK_LAYOUT } from "../utils/mockLayout"

const pois = ref([])
const routes = ref([])
const detailMap = ref({})
const genMode = ref("smart")
const travelMode = ref("driving")
const openId = ref(null)

onMounted(async () => {
  try {
    const res = await fetchPois({ page_size: 100 })
    pois.value = res.data.items
    const r = await fetchRoutes()
    routes.value = r.data
  } catch (e) {
    showToast(e.message)
  }
})

const selectedPois = computed(() =>
  state.selectedIds
    .map((id) => pois.value.find((p) => p.poi_id === id))
    .filter(Boolean)
)

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
    showToast("路线生成成功，可在下方查看")
    const r = await fetchRoutes()
    routes.value = r.data
  } catch (e) {
    showToast(e.message)
  }
}

async function toggleOpen(routeId) {
  if (openId.value === routeId) {
    openId.value = null
    return
  }
  openId.value = routeId
  if (!detailMap.value[routeId]) {
    const res = await fetchRoute(routeId)
    detailMap.value[routeId] = res.data
  }
}

async function onRename(r, e) {
  const name = e.target.value.trim()
  if (!name || name === r.name) {
    e.target.value = r.name
    return
  }
  await renameRoute(r.route_id, name)
  const list = await fetchRoutes()
  routes.value = list.data
}

async function onCopy(routeId) {
  await copyRoute(routeId)
  showToast("已复制路线副本")
  const r = await fetchRoutes()
  routes.value = r.data
}

async function onDelete(routeId) {
  await deleteRoute(routeId)
  if (openId.value === routeId) openId.value = null
  delete detailMap.value[routeId]
  showToast("路线已删除")
  const r = await fetchRoutes()
  routes.value = r.data
}

function fmt(minutes) {
  if (minutes == null) return "—"
  const h = Math.floor(minutes / 60)
  const m = minutes % 60
  return h ? `${h}小时${m ? m + "分钟" : ""}` : `${m}分钟`
}

function xy(poiId) {
  return (
    MOCK_LAYOUT[poiId] || { x: 50, y: 50 }
  )
}
function colorOf(poiId) {
  const p = pois.value.find((x) => x.poi_id === poiId)
  const map = {
    spot: "var(--c-spot)",
    food: "var(--c-food)",
    leisure: "var(--c-leisure)",
    facility: "var(--c-facility)",
  }
  return map[p?.type] || "var(--accent)"
}
function linePoints(r) {
  const items = detailMap.value[r.route_id]?.items || []
  return items.map((it) => {
    const c = xy(it.poi_id)
    return `${c.x},${c.y}`
  }).join(" ")
}
</script>

<style scoped>
.plan-wrap {
  position: absolute;
  inset: 0;
  padding: 74px 24px 108px;
  overflow-y: auto;
}
.plan-title {
  font-size: 26px;
  font-weight: 700;
  letter-spacing: -0.3px;
}
.plan-grid {
  display: grid;
  grid-template-columns: 340px 1fr;
  gap: 18px;
  margin-top: 18px;
  align-items: start;
}
.plan-col {
  display: flex;
  flex-direction: column;
  gap: 14px;
  min-width: 0;
}
.plan-card {
  border-radius: var(--r-l);
  padding: 16px;
}
.pc-title {
  font-size: 15px;
  font-weight: 600;
  margin-bottom: 12px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.sp-count {
  font-size: 12px;
  color: var(--text-2);
  background: var(--glass-inner);
  padding: 3px 9px;
  border-radius: 11px;
}
.seg {
  display: flex;
  background: var(--glass-inner);
  border-radius: 12px;
  padding: 3px;
  gap: 3px;
  margin-bottom: 12px;
}
.seg button {
  flex: 1;
  height: 32px;
  border-radius: 9px;
  font-size: 12.5px;
  font-weight: 500;
  color: var(--text-2);
  transition: all 0.2s var(--ease);
}
.seg button.on {
  background: var(--glass-bg-strong);
  color: var(--text);
  box-shadow: var(--shadow-s);
}
.plan-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  max-height: 300px;
  overflow-y: auto;
}
.empty {
  color: var(--text-3);
  font-size: 13px;
  padding: 18px 4px;
}
.plan-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  background: var(--glass-inner);
  border-radius: var(--r-m);
  padding: 8px 10px;
}
.plan-item .dot {
  width: 9px;
  height: 9px;
  border-radius: 50%;
}
.dot.spot { background: var(--c-spot); }
.dot.food { background: var(--c-food); }
.dot.leisure { background: var(--c-leisure); }
.dot.facility { background: var(--c-facility); }
.idx {
  color: var(--text-3);
  font-size: 11px;
}
.nm { flex: 1; }
.del {
  width: 22px;
  height: 22px;
  border-radius: 7px;
  font-size: 14px;
}
.del:hover {
  background: rgba(255, 59, 48, 0.12);
  color: var(--danger);
}
.generate-btn {
  height: 46px;
  border-radius: var(--r-m);
  background: var(--accent);
  color: #fff;
  font-size: 15px;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  box-shadow: 0 8px 20px rgba(10, 132, 255, 0.3);
}
.generate-btn svg {
  width: 18px;
  height: 18px;
  stroke: #fff;
  fill: none;
  stroke-width: 2;
  stroke-linecap: round;
}
.generate-btn:active { transform: scale(0.98); }

.route-cards {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.route-card {
  border-radius: var(--r-l);
  overflow: hidden;
}
.rc-head {
  padding: 15px 16px;
  display: flex;
  align-items: center;
  gap: 11px;
  cursor: pointer;
  min-height: 56px;
}
.rc-order {
  width: 30px;
  height: 30px;
  border-radius: var(--r-s);
  background: var(--accent-soft);
  color: var(--accent);
  font-size: 13px;
  font-weight: 700;
  display: grid;
  place-items: center;
  flex: none;
}
.rc-meta { flex: 1; min-width: 0; }
.rc-name {
  background: none;
  border: none;
  outline: none;
  font-size: 14.5px;
  font-weight: 600;
  color: var(--text);
  width: 150px;
  border-radius: 6px;
  padding: 1px 4px;
}
.rc-name:focus { background: var(--glass-inner); }
.rc-count {
  font-size: 12px;
  color: var(--text-2);
  margin-top: 2px;
}
.rc-icon {
  width: 30px;
  height: 30px;
  border-radius: 9px;
  display: grid;
  place-items: center;
}
.rc-icon svg {
  width: 15px;
  height: 15px;
  stroke: var(--text-2);
  fill: none;
  stroke-width: 1.9;
  stroke-linecap: round;
  stroke-linejoin: round;
}
.rc-icon:hover { background: var(--glass-inner); }
.rc-chevron svg {
  width: 18px;
  height: 18px;
  stroke: var(--text-2);
  fill: none;
  stroke-width: 2;
  transition: transform 0.25s var(--ease);
}
.route-card.open .rc-chevron svg { transform: rotate(180deg); }
.rc-body { padding: 0 16px 16px; }
.rc-summary {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
}
.rc-summary .chip {
  font-size: 12px;
  color: var(--text-2);
  background: var(--glass-inner);
  padding: 5px 11px;
  border-radius: 11px;
}
.mini-map {
  height: 180px;
  border-radius: var(--r-m);
  overflow: hidden;
  position: relative;
  background: var(--map-bg);
  margin-bottom: 12px;
}
.mini-map svg { width: 100%; height: 100%; }
.mm-line {
  fill: none;
  stroke: var(--accent);
  stroke-width: 2.5;
  stroke-dasharray: 5 4;
  stroke-linecap: round;
}
.mm-dot { stroke: #fff; stroke-width: 2; }
.mm-num {
  font-size: 9px;
  font-weight: 700;
  fill: #fff;
  text-anchor: middle;
}
.itinerary { display: flex; flex-direction: column; }
.it-item {
  display: flex;
  gap: 11px;
  padding: 10px 2px;
}
.it-item + .it-item { border-top: 1px solid var(--line); }
.it-item .seq {
  width: 22px;
  height: 22px;
  border-radius: 50%;
  font-size: 11.5px;
  font-weight: 700;
  display: grid;
  place-items: center;
  color: #fff;
  flex: none;
}
.it-nm { font-size: 13.5px; font-weight: 500; }
.it-sub { font-size: 11.5px; color: var(--text-2); margin-top: 2px; }
</style>
