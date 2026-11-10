<template>
  <div class="controls">
    <button
      class="ctl glass"
      :class="{ on: filterActive }"
      @click="$emit('toggle-filter')"
    >
      <svg viewBox="0 0 24 24" width="20" height="20">
        <path
          fill="currentColor"
          d="M4 6h16l-6 7v5l-4 2v-7z"
        />
      </svg>
      <span>筛选</span>
    </button>
    <button
      class="ctl glass"
      :class="{ on: markActive }"
      @click="$emit('toggle-mark')"
    >
      <svg viewBox="0 0 24 24" width="20" height="20">
        <path
          fill="currentColor"
          d="M12 2l2.5 5.6L20 8.4l-4 4.1 1 5.9L12 15.5 7 18.4l1-5.9-4-4.1 5.5-.8z"
        />
      </svg>
      <span>标记</span>
    </button>
  </div>
</template>

<script setup>
defineProps({
  filterActive: Boolean,
  markActive: Boolean,
})
defineEmits(["toggle-filter", "toggle-mark"])
</script>

<style scoped>
.controls {
  position: absolute;
  right: 14px;
  top: 118px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  z-index: 20;
}
.ctl {
  width: 52px;
  height: 52px;
  border-radius: var(--r-md);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 2px;
  color: var(--text-2);
  transition: 0.22s var(--ease);
}
.ctl span {
  font-size: 10px;
}
.ctl.on {
  color: #fff;
  background: var(--brand);
  border-color: transparent;
}
.ctl:active {
  transform: scale(0.92);
}
</style>
