<template>
  <transition name="up">
    <div v-if="poi" class="detail-mask" @click.self="$emit('close')">
      <div class="sheet glass">
        <div class="grip" />
        <div class="head">
          <div>
            <h3>{{ poi.name }}</h3>
            <div class="meta">
              <span class="tag" :class="poi.type">
                {{ typeLabel }}
              </span>
              <span>{{ poi.district }}</span>
            </div>
          </div>
          <button class="close" @click="$emit('close')">×</button>
        </div>

        <p v-if="poi.description" class="desc">
          {{ poi.description }}
        </p>

        <ul class="info">
          <li v-if="poi.address">
            <span class="k">地址</span>{{ poi.address }}
          </li>
          <li v-if="poi.open_time">
            <span class="k">开放</span>{{ poi.open_time }}
          </li>
          <li v-if="poi.ticket">
            <span class="k">门票</span>{{ poi.ticket }}
          </li>
          <li v-if="poi.cost">
            <span class="k">消费</span>{{ poi.cost }}
          </li>
          <li v-if="poi.stay_minutes">
            <span class="k">建议停留</span>{{ poi.stay_minutes }} 分钟
          </li>
        </ul>

        <div class="actions">
          <button
            class="icon-btn"
            :class="{ on: favored }"
            @click="$emit('toggle-favorite', poi)"
          >
            <svg viewBox="0 0 24 24" width="18" height="18">
              <path
                fill="currentColor"
                d="M12 20s-7-4.4-9.2-8.2C1.3 9.2 2.7 6 6 6c2 0 3.2 1.2 4 2.3C10.8 7.2 12 6 14 6c3.3 0 4.7 3.2 3.2 5.8C19 15.6 12 20 12 20z"
              />
            </svg>
            收藏
          </button>
          <button
            class="icon-btn"
            :class="{ on: marked }"
            @click="$emit('toggle-mark', poi)"
          >
            <svg viewBox="0 0 24 24" width="18" height="18">
              <path
                fill="currentColor"
                d="M12 2l2.5 5.6L20 8.4l-4 4.1 1 5.9L12 15.5 7 18.4l1-5.9-4-4.1 5.5-.8z"
              />
            </svg>
            标记
          </button>
          <button
            v-if="poi.type !== 'facility'"
            class="primary"
            :class="{ added: selected }"
            @click="$emit('toggle-add', poi)"
          >
            {{ selected ? "已加入 · 点击移除" : "加入待选" }}
          </button>
          <p v-else class="facility-note">配套服务点位，仅作参考，不能加入路线</p>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
const TYPE_LABELS = {
  spot: "景点",
  food: "美食",
  leisure: "休闲",
  facility: "配套",
}

defineProps({
  poi: Object,
  selected: Boolean,
  marked: Boolean,
  favored: Boolean,
})
defineEmits([
  "close",
  "toggle-add",
  "toggle-mark",
  "toggle-favorite",
])
</script>

<style scoped>
.detail-mask {
  position: absolute;
  inset: 0;
  background: rgba(20, 28, 40, 0.32);
  z-index: 40;
  display: flex;
  align-items: flex-end;
}
.sheet {
  width: 100%;
  border-radius: var(--r-lg) var(--r-lg) 0 0;
  padding: 10px 20px 26px;
}
.grip {
  width: 40px;
  height: 4px;
  border-radius: 2px;
  background: rgba(128, 140, 155, 0.35);
  margin: 4px auto 14px;
}
.head {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}
h3 {
  font-size: 20px;
}
.meta {
  display: flex;
  gap: 8px;
  align-items: center;
  margin-top: 6px;
  font-size: 12px;
  color: var(--text-2);
}
.tag {
  padding: 2px 10px;
  border-radius: var(--r-pill);
  color: #fff;
}
.tag.spot {
  background: var(--c-spot);
}
.tag.food {
  background: var(--c-food);
}
.tag.leisure {
  background: var(--c-leisure);
}
.tag.facility {
  background: var(--c-facility);
}
.close {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: rgba(128, 140, 155, 0.2);
  font-size: 18px;
}
.desc {
  margin-top: 14px;
  font-size: 14px;
  line-height: 1.7;
  color: var(--text-2);
}
.info {
  list-style: none;
  margin-top: 14px;
  display: grid;
  gap: 8px;
}
.info li {
  font-size: 13px;
  display: flex;
  gap: 10px;
}
.k {
  color: var(--text-3);
  width: 56px;
  flex-shrink: 0;
}
.actions {
  display: flex;
  gap: 10px;
  margin-top: 20px;
  align-items: center;
}
.icon-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 3px;
  font-size: 11px;
  color: var(--text-2);
  padding: 8px 10px;
  border-radius: var(--r-sm);
  background: rgba(128, 140, 155, 0.12);
}
.icon-btn.on {
  color: var(--brand);
  background: rgba(58, 123, 213, 0.14);
}
.primary {
  flex: 1;
  padding: 13px;
  border-radius: var(--r-md);
  background: var(--brand);
  color: #fff;
  font-weight: 600;
  transition: 0.2s var(--ease);
}
.primary.added {
  background: rgba(128, 140, 155, 0.28);
  color: var(--text);
}
.facility-note {
  flex: 1;
  font-size: 12px;
  color: var(--text-3);
  text-align: center;
}
.up-enter-active,
.up-leave-active {
  transition: 0.3s var(--ease);
}
.up-enter-from .sheet,
.up-leave-to .sheet {
  transform: translateY(100%);
}
.up-enter-from,
.up-leave-to {
  opacity: 0;
}
</style>
