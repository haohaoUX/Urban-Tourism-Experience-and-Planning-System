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
  top: 18px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 60;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  pointer-events: none;
}
.toast {
  border-radius: var(--r-m);
  padding: 11px 18px;
  font-size: 13.5px;
  font-weight: 500;
  max-width: 80vw;
}
.toast-enter-active,
.toast-leave-active {
  transition: 0.25s var(--ease);
}
.toast-enter-from,
.toast-leave-to {
  opacity: 0;
  transform: translateY(-12px);
}
</style>
