<template>
  <transition name="fade">
    <div v-if="poi" class="detail-card glass">
      <div class="dc-body">
        <div class="dc-name-row">
          <div class="dc-name">{{ poi.name }}</div>
          <button
            class="mark-btn"
            :class="{ on: marked }"
            :title="marked ? '取消标记' : '标记该点位'"
            @click="$emit('mark', poi)"
          >
            <svg viewBox="0 0 24 24">
              <path d="M6 3h12v18l-6-4-6 4V3Z" />
            </svg>
          </button>
        </div>
        <div class="dc-sub">
          <span class="tag">{{ typeLabel(poi.type) }}</span>
          <span>|</span>
          <span>{{ poi.district }}</span>
        </div>

        <p v-if="poi.description" class="dc-desc">{{ poi.description }}</p>

        <div class="dc-info">
          <div v-if="poi.open_time" class="dc-row">
            <svg viewBox="0 0 24 24">
              <circle cx="12" cy="12" r="9" />
              <path d="M12 7v5l3 2" />
            </svg>
            <span class="k">开放时间</span>
            <span class="v">{{ poi.open_time }}</span>
          </div>
          <div v-if="poi.stay_minutes" class="dc-row">
            <svg viewBox="0 0 24 24">
              <path d="M12 21a9 9 0 100-18 9 9 0 000 18Z" />
              <path d="M12 8v4l3 2" />
            </svg>
            <span class="k">停留时长</span>
            <span class="v">约 {{ poi.stay_minutes }} 分钟</span>
          </div>
          <div v-if="poi.ticket" class="dc-row">
            <svg viewBox="0 0 24 24">
              <path d="M4 8a2 2 0 012-2h12a2 2 0 012 2v2a2 2 0 000 4v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2a2 2 0 000-4V8Z" />
              <path d="M12 6v12" />
            </svg>
            <span class="k">门票</span>
            <span class="v">{{ poi.ticket }}</span>
          </div>
          <div v-if="poi.cost" class="dc-row">
            <svg viewBox="0 0 24 24">
              <path d="M12 2v20M17 6H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H7" />
            </svg>
            <span class="k">消费参考</span>
            <span class="v">{{ poi.cost }}</span>
          </div>
        </div>
      </div>

      <div class="dc-actions">
        <button class="btn btn-ghost" @click="$emit('nearby', poi)">
          <svg viewBox="0 0 24 24">
            <circle cx="12" cy="12" r="9" />
            <path d="M12 8v4l3 2" />
          </svg>
          查看周边
        </button>
        <button
          v-if="poi.type !== 'facility'"
          class="btn btn-primary"
          :disabled="selected"
          @click="$emit('add', poi)"
        >
          <svg viewBox="0 0 24 24">
            <path d="m5 12 5 5L20 7" v-if="selected" />
            <path d="M12 5v14M5 12h14" v-else />
          </svg>
          {{ selected ? "已添加" : "添加到路线" }}
        </button>
      </div>
    </div>
  </transition>
</template>

<script setup>
const TYPE_LABELS = {
  spot: "景点",
  food: "正餐美食",
  leisure: "休闲市集小店",
  facility: "配套服务",
}
defineProps({
  poi: Object,
  selected: Boolean,
  marked: Boolean,
})
defineEmits(["close", "add", "nearby", "mark"])
const typeLabel = (t) => TYPE_LABELS[t]
</script>

<style scoped>
.detail-card {
  position: absolute;
  right: 22px;
  top: 50%;
  width: 330px;
  transform: translateY(-50%);
  border-radius: var(--r-xl);
  z-index: 22;
  max-height: calc(100% - 180px);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
.dc-body {
  padding: 18px;
  overflow-y: auto;
}
.dc-name-row {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 10px;
}
.dc-name {
  font-size: 18px;
  font-weight: 600;
}
.mark-btn {
  width: 34px;
  height: 34px;
  border-radius: 10px;
  display: grid;
  place-items: center;
  flex: none;
  background: var(--glass-inner);
}
.mark-btn svg {
  width: 17px;
  height: 17px;
  stroke: var(--text-2);
  fill: none;
  stroke-width: 1.9;
  stroke-linejoin: round;
}
.mark-btn.on {
  background: var(--accent-soft);
}
.mark-btn.on svg {
  stroke: var(--accent);
  fill: var(--accent);
}
.dc-sub {
  font-size: 12px;
  color: var(--text-2);
  margin-top: 4px;
  display: flex;
  align-items: center;
  gap: 6px;
}
.dc-sub .tag {
  color: var(--accent);
}
.dc-desc {
  font-size: 13.5px;
  line-height: 1.65;
  color: var(--text);
  margin-top: 12px;
}
.dc-info {
  margin-top: 14px;
  display: flex;
  flex-direction: column;
  gap: 9px;
}
.dc-row {
  display: flex;
  align-items: center;
  gap: 9px;
  font-size: 13px;
}
.dc-row svg {
  width: 16px;
  height: 16px;
  stroke: var(--text-2);
  fill: none;
  stroke-width: 1.8;
  stroke-linecap: round;
  stroke-linejoin: round;
  flex: none;
}
.dc-row .k {
  color: var(--text-2);
  width: 58px;
  flex: none;
}
.dc-row .v {
  color: var(--text);
}
.dc-actions {
  display: flex;
  gap: 8px;
  padding: 12px 18px 16px;
}
.btn {
  flex: 1;
  height: 42px;
  border-radius: var(--r-m);
  font-size: 14px;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  transition: transform 0.15s var(--ease), background 0.2s;
}
.btn svg {
  width: 16px;
  height: 16px;
  stroke: currentColor;
  fill: none;
  stroke-width: 2;
  stroke-linecap: round;
  stroke-linejoin: round;
}
.btn:active {
  transform: scale(0.97);
}
.btn-primary {
  background: var(--accent);
  color: #fff;
}
.btn-primary:disabled {
  background: var(--text-3);
  cursor: default;
}
.btn-ghost {
  background: var(--glass-inner);
  color: var(--text);
}
.fade-enter-active,
.fade-leave-active {
  transition: 0.3s var(--ease);
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-46%);
}
</style>
