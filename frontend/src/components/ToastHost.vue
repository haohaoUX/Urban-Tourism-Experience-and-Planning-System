<template>
  <div class="toast-host">
    <transition-group name="toast">
      <div v-for="t in state.toasts" :key="t.id" class="toast glass">
        {{ t.message }}
      </div>
    </transition-group>
  </div>
</template>

<script setup>
import { state } from "../stores/trip"
</script>

<style scoped>
.toast-host {
  position: absolute;
  top: 70px;
  left: 0;
  right: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  z-index: 60;
  pointer-events: none;
}
.toast {
  padding: 10px 20px;
  border-radius: var(--r-pill);
  font-size: 13px;
}
.toast-enter-active,
.toast-leave-active {
  transition: 0.28s var(--ease);
}
.toast-enter-from,
.toast-leave-to {
  opacity: 0;
  transform: translateY(-12px);
}
</style>
