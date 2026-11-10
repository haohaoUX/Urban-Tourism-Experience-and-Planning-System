<template>
  <transition name="pop">
    <div v-if="open" class="filter-panel glass">
      <p class="group-title">行政区</p>
      <div class="group">
        <button
          v-for="d in DISTRICTS"
          :key="d"
          class="chk"
          :class="{ on: districts.includes(d) }"
          @click="$emit('toggle-district', d)"
        >
          <span class="box">
            <svg viewBox="0 0 24 24">
              <path d="m5 12 5 5L20 7" />
            </svg>
          </span>
          {{ d }}
        </button>
      </div>

      <p class="group-title">点位类型</p>
      <div class="group">
        <button
          v-for="t in TYPES"
          :key="t.value"
          class="chk"
          :class="{ on: types.includes(t.value) }"
          @click="$emit('toggle-type', t.value)"
        >
          <span class="box">
            <svg viewBox="0 0 24 24">
              <path d="m5 12 5 5L20 7" />
            </svg>
          </span>
          {{ t.label }}
        </button>
      </div>
    </div>
  </transition>
</template>

<script setup>
const TYPES = [
  { value: "spot", label: "景点" },
  { value: "food", label: "正餐美食" },
  { value: "leisure", label: "休闲市集小店" },
  { value: "facility", label: "配套服务" },
]
const DISTRICTS = [
  "东湖区",
  "西湖区",
  "红谷滩区",
  "青云谱区",
  "青山湖区",
  "新建区",
]
defineProps({
  open: Boolean,
  types: Array,
  districts: Array,
})
defineEmits(["toggle-type", "toggle-district"])
</script>

<style scoped>
.filter-panel {
  border-radius: var(--r-l);
  padding: 14px;
}
.group-title {
  font-size: 11px;
  font-weight: 600;
  color: var(--text-3);
  margin: 4px 2px 8px;
  letter-spacing: 0.5px;
}
.group {
  display: flex;
  flex-wrap: wrap;
  gap: 7px;
  margin-bottom: 12px;
}
.group:last-child {
  margin-bottom: 2px;
}
.chk {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12.5px;
  color: var(--text-2);
  padding: 6px 10px 6px 7px;
  border-radius: 18px;
  background: var(--glass-inner);
  border: 1px solid transparent;
  transition: all 0.18s var(--ease);
  min-height: 32px;
}
.box {
  width: 17px;
  height: 17px;
  border-radius: 50%;
  border: 1.5px solid var(--text-3);
  display: grid;
  place-items: center;
  transition: all 0.18s var(--ease);
}
.box svg {
  width: 10px;
  height: 10px;
  stroke: #fff;
  stroke-width: 2.4;
  fill: none;
  stroke-linecap: round;
  stroke-linejoin: round;
  opacity: 0;
}
.chk.on {
  color: var(--accent);
  border-color: var(--accent);
}
.chk.on .box {
  background: var(--accent);
  border-color: var(--accent);
}
.chk.on .box svg {
  opacity: 1;
}
.pop-enter-active,
.pop-leave-active {
  transition: 0.24s var(--spring);
}
.pop-enter-from,
.pop-leave-to {
  opacity: 0;
  transform: scale(0.94);
}
</style>
