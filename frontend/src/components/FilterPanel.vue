<template>
  <transition name="slide">
    <div v-if="open" class="filter-panel glass">
      <div class="head">
        <span>筛选</span>
        <button class="link" @click="$emit('reset')">重置</button>
      </div>

      <p class="label">类型</p>
      <div class="chips">
        <button
          v-for="t in TYPES"
          :key="t.value"
          class="chip"
          :class="{ on: types.includes(t.value) }"
          :style="on ? chipColor(t.value) : null"
          @click="$emit('toggle-type', t.value)"
        >
          {{ t.label }}
        </button>
      </div>

      <p class="label">行政区</p>
      <div class="chips">
        <button
          v-for="d in DISTRICTS"
          :key="d"
          class="chip"
          :class="{ on: districts.includes(d) }"
          @click="$emit('toggle-district', d)"
        >
          {{ d }}
        </button>
      </div>

      <button class="done" @click="$emit('close')">完成</button>
    </div>
  </transition>
</template>

<script setup>
const TYPES = [
  { value: "spot", label: "景点" },
  { value: "food", label: "美食" },
  { value: "leisure", label: "休闲" },
  { value: "facility", label: "配套" },
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
defineEmits([
  "toggle-type",
  "toggle-district",
  "reset",
  "close",
])

const chipColor = (value) => {
  const map = {
    spot: "var(--c-spot)",
    food: "var(--c-food)",
    leisure: "var(--c-leisure)",
    facility: "var(--c-facility)",
  }
  return { "--chip": map[value] }
}
</script>

<style scoped>
.filter-panel {
  position: absolute;
  left: 14px;
  right: 14px;
  bottom: 96px;
  border-radius: var(--r-lg);
  padding: 18px;
  z-index: 30;
}
.head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 700;
  font-size: 16px;
}
.link {
  font-size: 13px;
  color: var(--brand);
}
.label {
  margin: 16px 0 8px;
  font-size: 13px;
  color: var(--text-2);
}
.chips {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
.chip {
  padding: 7px 14px;
  border-radius: var(--r-pill);
  font-size: 13px;
  background: rgba(128, 140, 155, 0.14);
  border: 1px solid transparent;
  transition: 0.2s var(--ease-soft);
}
.chip.on {
  color: #fff;
  background: var(--chip, var(--brand));
  border-color: transparent;
}
.done {
  margin-top: 18px;
  width: 100%;
  padding: 12px;
  border-radius: var(--r-md);
  background: var(--brand);
  color: #fff;
  font-weight: 600;
}
.slide-enter-active,
.slide-leave-active {
  transition: 0.28s var(--ease);
}
.slide-enter-from,
.slide-leave-to {
  opacity: 0;
  transform: translateY(20px);
}
</style>
