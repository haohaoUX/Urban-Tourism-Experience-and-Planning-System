<template>
  <div class="app">
    <router-view />
    <BottomNav />
    <ToastHost />
  </div>
</template>

<script setup>
import { watch } from "vue"
import BottomNav from "./components/BottomNav.vue"
import ToastHost from "./components/ToastHost.vue"
import { state } from "./stores/trip"

// 同步浅色 / 深色主题
watch(
  () => state.theme,
  (theme) => {
    document.documentElement.dataset.theme = theme
  },
  { immediate: true }
)
</script>
