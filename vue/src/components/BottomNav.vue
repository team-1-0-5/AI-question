<template>
  <nav class="bottom-nav">
    <div
      v-for="(item, idx) in navs"
      :key="item.label"
      :class="['nav-item', {active: idx === active}]"
      @click="$emit('changeTab', idx)"
    >
      <div class="nav-icon">
        <svg v-if="idx === 0" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none">
          <path d="M4 19.5V9.5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
          <path d="M4 9.5L12 4L20 9.5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
          <path d="M12 4V20" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M20 9.5V19.5C20 20.0523 19.5523 20.5 19 20.5H5C4.44772 20.5 4 20.0523 4 19.5V9.5" stroke="currentColor" stroke-width="2"/>
        </svg>

        <svg v-else-if="idx === 1" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none">
          <path d="M3 3V18C3 19.6569 4.34315 21 6 21H21" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
          <path d="M7 14L10.5 10.5L14 14L21 7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          <circle cx="18" cy="8" r="1" fill="currentColor"/>
        </svg>

        <svg v-else xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none">
          <circle cx="12" cy="8" r="4" stroke="currentColor" stroke-width="2"/>
          <path d="M5.33788 18C6.06687 15.347 8.29836 14 12.0002 14C15.7021 14 17.9336 15.347 18.6626 18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
        </svg>
      </div>
      <span class="nav-label">{{ item.label }}</span>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { defineProps, defineEmits } from 'vue';
const props = defineProps<{ active: number }>();
defineEmits(['changeTab']);
const navs = [
  { label: '讲座课程' },
  { label: '统计数据' },
  { label: '个人中心' },
];
</script>

<style scoped>
.bottom-nav {
  display: flex;
  justify-content: space-around;
  height: 72px;
  background: white;
  border-top: 1px solid rgba(0, 0, 0, 0.05);
  box-shadow: 0 -4px 12px rgba(0, 0, 0, 0.03);
  padding: 0.5rem 0;
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 100;
}

.nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 4px;
  color: #9e9e9e;
  cursor: pointer;
  transition: all 0.2s ease;
  flex: 1;
  padding: 0.5rem;
}

.nav-item.active {
  color: #4caf50;
}

.nav-icon {
  width: 26px;
  height: 26px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.2s ease;
}

.nav-item.active .nav-icon {
  transform: translateY(-3px);
}

.nav-label {
  font-size: 0.8rem;
  font-weight: 500;
  letter-spacing: 0.3px;
}
</style>
