<template>
  <div class="search-bar glass">
    <svg viewBox="0 0 24 24">
      <circle cx="11" cy="11" r="7" />
      <path d="m20 20-3.2-3.2" />
    </svg>
    <input
      v-model="text"
      type="text"
      placeholder="搜索南昌点位，如：滕王阁"
      @input="onInput"
      @keyup.enter="$emit('search', text.trim())"
    />
  </div>
</template>

<script setup>
import { ref } from "vue"

const text = ref("")
const emit = defineEmits(["search", "clear"])

let timer
function onInput() {
  clearTimeout(timer)
  timer = setTimeout(() => {
    if (text.value) emit("search", text.value.trim())
    else emit("clear")
  }, 250)
}
</script>

<style scoped>
.search-bar {
  position: absolute;
  top: 16px;
  left: 50%;
  transform: translateX(-50%);
  width: min(420px, calc(100% - 200px));
  height: 42px;
  border-radius: 21px;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 0 16px;
  z-index: 30;
}
.search-bar svg {
  width: 17px;
  height: 17px;
  stroke: var(--text-2);
  fill: none;
  stroke-width: 2;
  stroke-linecap: round;
  flex: none;
}
input {
  flex: 1;
  min-width: 0;
  border: none;
  background: none;
  outline: none;
  font-size: 14px;
  color: var(--text);
}
input::placeholder {
  color: var(--text-3);
}
.search-bar:focus-within {
  border-color: var(--accent);
  box-shadow: 0 0 0 4px var(--accent-soft), var(--shadow-m);
}
</style>
