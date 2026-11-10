<template>
  <nav class="bottom-nav glass">
    <div class="nav-pill" :class="{ slide: isPlan }" />
    <router-link to="/" class="nav-item" :class="{ active: !isPlan }">
      <svg viewBox="0 0 24 24">
        <path d="M9 4 3 6v14l6-2 6 2 6-2V4l-6 2-6-2Z" />
        <path d="M9 4v14M15 6v14" />
      </svg>
      地图
    </router-link>
    <router-link to="/plan" class="nav-item" :class="{ active: isPlan }">
      <svg viewBox="0 0 24 24">
        <path d="M12 21s-7-5.5-7-11a7 7 0 0 1 14 0c0 5.5-7 11-7 11Z" />
        <circle cx="12" cy="10" r="2.5" />
      </svg>
      规划
    </router-link>
  </nav>
</template>

<script setup>
import { computed } from "vue"
import { useRoute } from "vue-router"

const route = useRoute()
const isPlan = computed(() => route.path === "/plan")
</script>

<style scoped>
.bottom-nav {
  position: absolute;
  left: 50%;
  bottom: 16px;
  transform: translateX(-50%);
  z-index: 40;
  border-radius: 28px;
  padding: 7px;
  display: flex;
}
.nav-pill {
  position: absolute;
  top: 7px;
  bottom: 7px;
  left: 7px;
  width: calc(50% - 7px);
  border-radius: 22px;
  background: var(--accent-soft);
  transition: transform 0.35s var(--spring);
}
.nav-pill.slide {
  transform: translateX(100%);
}
.nav-item {
  position: relative;
  width: 120px;
  height: 44px;
  border-radius: 22px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 7px;
  font-size: 14px;
  font-weight: 500;
  color: var(--text-2);
  text-decoration: none;
  z-index: 1;
  transition: color 0.25s var(--ease);
}
.nav-item svg {
  width: 18px;
  height: 18px;
  stroke: currentColor;
  fill: none;
  stroke-width: 1.9;
  stroke-linecap: round;
  stroke-linejoin: round;
}
.nav-item.active {
  color: var(--accent);
}
</style>
