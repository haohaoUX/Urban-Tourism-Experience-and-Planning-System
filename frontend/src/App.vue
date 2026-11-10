<template>
  <div class="app-shell">
    <router-view v-slot="{ Component }">
      <transition name="fade" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>
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

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.22s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
