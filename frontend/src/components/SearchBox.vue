<template>
  <div class="search glass">
    <svg viewBox="0 0 24 24" width="17" height="17" class="icon">
      <path
        fill="currentColor"
        d="M10 4a6 6 0 103.7 10.7l4.3 4.3 1.4-1.4-4.3-4.3A6 6 0 0010 4zm0 2a4 4 0 110 8 4 4 0 010-8z"
      />
    </svg>
    <input
      v-model="text"
      type="text"
      placeholder="搜索景点、美食、街区"
      @input="onInput"
      @keyup.enter="$emit('search', text.trim())"
    />
    <button v-if="text" class="clear" @click="clearText">×</button>
  </div>
</template>

<script setup>
import { ref } from "vue"

const text = ref("")
const emit = defineEmits(["search", "clear"])

let timer
function onInput() {
  clearTimeout(timer)
  timer = setTimeout(() => emit("search", text.value.trim()), 250)
}
function clearText() {
  text.value = ""
  emit("clear")
}
</script>

<style scoped>
.search {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 14px;
  border-radius: var(--r-pill);
}
.icon {
  color: var(--text-3);
  flex-shrink: 0;
}
input {
  flex: 1;
  min-width: 0;
  border: none;
  background: transparent;
  outline: none;
  font-size: 14px;
  color: var(--text);
}
input::placeholder {
  color: var(--text-3);
}
.clear {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: rgba(128, 140, 155, 0.25);
  color: #fff;
  font-size: 14px;
  line-height: 1;
}
</style>
