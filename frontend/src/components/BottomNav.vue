<template>
  <nav class="bottom-nav glass">
    <router-link
      v-for="item in items"
      :key="item.to"
      :to="item.to"
      class="nav-item"
      :class="{ active: route.path === item.to }"
    >
      <span class="ico">
        <svg viewBox="0 0 24 24" width="22" height="22">
          <path fill="currentColor" :d="item.icon" />
        </svg>
        <i v-if="item.badge" class="badge">{{ badgeCount }}</i>
      </span>
      <span>{{ item.label }}</span>
    </router-link>
  </nav>
</template>

<script setup>
import { useRoute } from "vue-router"
import { state } from "../stores/trip"

const route = useRoute()
const items = [
  {
    to: "/",
    label: "地图",
    icon:
      "M12 2C8 2 5 5 5 9c0 5 7 13 7 13s7-8 7-13c0-4-3-7-7-7zm0 9.5A2.5 2.5 0 1112 6.5a2.5 2.5 0 010 5z",
    badge: false,
  },
  {
    to: "/plan",
    label: "规划",
    icon:
      "M19 3h-4.2A3 3 0 0012 1a3 3 0 00-2.8 2H5a2 2 0 00-2 2v15a2 2 0 002 2h14a2 2 0 002-2V5a2 2 0 00-2-2zm-7 0a1 1 0 11-1 1 1 1 0 011-1zm-2 13l-3-3 1.4-1.4L12 14l5.6-5.6L19 9.8z",
    badge: true,
  },
]
const badgeCount = state.selectedIds.length
</script>

<style scoped>
.bottom-nav {
  position: absolute;
  left: 14px;
  right: 14px;
  bottom: 16px;
  height: 62px;
  border-radius: var(--r-lg);
  display: flex;
  z-index: 50;
}
.nav-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 3px;
  font-size: 11px;
  color: var(--text-3);
  text-decoration: none;
  transition: 0.2s var(--ease);
}
.nav-item.active {
  color: var(--brand);
}
.ico {
  position: relative;
  display: flex;
}
.badge {
  position: absolute;
  top: -5px;
  right: -9px;
  min-width: 16px;
  height: 16px;
  padding: 0 4px;
  border-radius: var(--r-pill);
  background: var(--c-food);
  color: #fff;
  font-size: 10px;
  font-style: normal;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
