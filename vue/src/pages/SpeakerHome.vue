<template>
  <div class="speaker-home">
    <header class="sh-header">
      <h2 class="header-title">
        <template v-if="activeTab === 0">我的讲座课程</template>
        <template v-else-if="activeTab === 1">数据总览</template>
        <template v-else>个人中心</template>
      </h2>
      <button v-if="activeTab === 0" class="create-btn" @click="onCreate">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="12" y1="5" x2="12" y2="19"></line>
          <line x1="5" y1="12" x2="19" y2="12"></line>
        </svg>
        创建演讲
      </button>
    </header>

    <section v-if="activeTab === 0" class="lecture-list">
      <div v-if="lectures.length === 0" class="empty-state">
        <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#9e9e9e" stroke-width="1.5">
          <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
        </svg>
        <p>暂无演讲，点击上方按钮创建</p>
      </div>
      <div v-else>
        <div class="sort-controls">
          <span>排序方式：</span>
          <select v-model="sortOption" class="sort-select">
            <option value="default">默认（状态+时间）</option>
            <option value="dateAsc">时间（从近到远）</option>
            <option value="dateDesc">时间（从远到近）</option>
          </select>
        </div>
        <ul class="lecture-grid">
        <li
          v-for="lecture in sortedLectures"
          :key="lecture.lid"
          class="lecture-card"
          :class="getStatusClass(lecture.status) || ''"
          @click="handleLectureClick(lecture)"
          :style="lecture.status === '进行中' ? 'cursor:pointer;' : ''"
        >
          <div class="status-indicator" :class="getStatusClass(lecture.status) || ''"></div>
          <div class="card-content">
            <h3 class="lecture-title">{{ lecture.name }}</h3>
            <div class="lecture-info">
              <div class="info-row">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <circle cx="12" cy="12" r="10"></circle>
                  <polyline points="12 6 12 12 16 14"></polyline>
                </svg>
                <span>{{ lecture.start_time.slice(0, 10) + ' ' + lecture.start_time.slice(11, 16) }}</span>
              </div>
              <div class="info-row">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
                  <circle cx="12" cy="10" r="3"></circle>
                </svg>
                <span>演讲者：{{ lecture.speaker }}</span>
              </div>
              <div class="info-row">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <rect x="4" y="4" width="16" height="16" rx="2"/>
                  <path d="M8 8h8v8H8z"/>
                </svg>
                <span>文件数：{{ lecture.fids.length }}</span>
              </div>
            </div>
          </div>
          <div class="lecture-meta">
            <span :class="['status', getStatusClass(lecture.status) || '']">
            {{ lecture.status }}
            </span>
          </div>
        </li>
        </ul>
      </div>
    </section>
    <section v-if="activeTab === 1" class="overview-section">
      <div class="overview-chart">
        <div class="chart-title">最近5场讲座正确率变化</div>
        <div class="chart-container" style="position:relative;">
          <!-- 横坐标右侧为最近时间，鼠标悬停显示讲座名 -->
          <svg :width="280" :height="120" viewBox="0 0 280 120" @mouseleave="hideTooltip">
            <polyline
              :points="chartData.map((rate, i) => `${(chartData.length-1-i)*56},${120 - rate}` ).join(' ')"
              fill="none"
              stroke="#4caf50"
              stroke-width="3"
            />
            <circle
              v-for="(rate, i) in chartData"
              :key="i"
              :cx="(chartData.length-1-i)*56"
              :cy="120 - rate"
              r="5"
              fill="#4caf50"
              @mouseenter="showTooltip(i, $event)"
            />
            <text
              v-for="(label, i) in chartLabels"
              :key="label"
              :x="(chartLabels.length-1-i)*56"
              y="115"
              font-size="12"
              text-anchor="middle"
              fill="#555"
            >{{ label }}</text>
          </svg>
          <div v-if="tooltip.visible" class="chart-tooltip" :style="{left: tooltip.x+'px', top: tooltip.y+'px'}">
            {{ tooltip.title }}
          </div>
        </div>
        <div class="chart-legend">
          <span v-for="(rate, i) in chartData" :key="i" class="legend-item">
            <span class="legend-dot" :style="{ background: '#4caf50' }"></span>
            {{ chartLabels[i] }}：{{ rate }}%
          </span>
        </div>
      </div>
    </section>

    <!-- 个人中心占位 -->
    <section v-if="activeTab === 2"  class="center-section">
      <div class="center-placeholder">个人中心功能开发中...</div>
      <button class="logout-btn" @click="logout">退出登录</button>
    </section>

    <BottomNav :active="activeTab" @changeTab="onTabChange" />
  </div>
</template>

<script setup lang="ts">
const logout = () => {
  localStorage.removeItem('uid');
  localStorage.removeItem('type');
  router.replace('/login');
}
// 折线图tooltip
import { ref as vueRef, onMounted } from 'vue';
import axios from '@/utils/api.js';

interface Lecture {
  lid: number;
  name: string;
  speaker: string;
  start_time: string;
  fids: number[];
  status?: string;
}
const tooltip = vueRef({ visible: false, title: '', x: 0, y: 0 });
function showTooltip(i: number, evt: MouseEvent) {
  tooltip.value.visible = true;
  tooltip.value.title = recentLectures.value[recentLectures.value.length-1-i].name;
  tooltip.value.x = evt.offsetX + 20;
  tooltip.value.y = evt.offsetY - 10;
}
function hideTooltip() {
  tooltip.value.visible = false;
}

// 讲座卡片点击跳转
function handleLectureClick(lecture: any) {
if (lecture.status === '进行中') {
  router.push({ path: '/speaker-main-lct', query: { lid: lecture.lid } });
} else if (lecture.status === '即将开始') {
  router.push({ path: '/speaker-upcoming-detail', query: { lid: lecture.lid } });
} else if (lecture.status === '已结束') {
  router.push({ path: '/speaker-ended-detail', query: { lid: lecture.lid } });
}
}
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import BottomNav from '@/components/BottomNav.vue';

const activeMenu = ref<number | null>(null);
const sortOption = ref('default');
const router = useRouter();
const activeTab = ref(0); // 0: 讲座列表, 1: 数据总览, 2: 个人中心

const lectures = ref<Lecture[]>([])
// Removed the incorrect declaration

// 页面加载时自动获取该用户所有演讲信息
onMounted(async () => {
  const uid = localStorage.getItem('uid');
  try {
    const form = new FormData();
    if (uid) form.append('uid', uid);
    const res = await axios.post('/all_lecture', form, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
    // 返回参数为data列表
    const statusMap = {
      ongoing: '进行中',
      upcoming: '即将开始',
      ended: '已结束'
    };
    let rawLectures = [];
    if (res && Array.isArray(res.data)) {
      rawLectures = res.data;
    } else if (res && Array.isArray(res)) {
      rawLectures = res;
    }
    lectures.value = rawLectures.map((l: any) => ({
      ...l,
      status: l.state === 'ongoing' ? '进行中' : l.state === 'upcoming' ? '即将开始' : '已结束'
    }));
    if (!Array.isArray(rawLectures)) {
      lectures.value = [];
    }
  } catch (e) {
    lectures.value = [];
  }
});

// 计算排序后的讲座列表
const sortedLectures = computed(() => {
  const lecturesCopy = [...lectures.value];
  if (sortOption.value === 'dateAsc') {
    return lecturesCopy.sort((a, b) =>
      new Date(a.start_time).getTime() - new Date(b.start_time).getTime()
    );
  }
  if (sortOption.value === 'dateDesc') {
    return lecturesCopy.sort((a, b) =>
      new Date(b.start_time).getTime() - new Date(a.start_time).getTime()
    );
  }
  const statusOrder = {
    '进行中': 1,
    '即将开始': 2,
    '已结束': 3
  } as const;
  type StatusKey = keyof typeof statusOrder;
  return lecturesCopy.sort((a, b) => {
    if (statusOrder[a.status as StatusKey] !== statusOrder[b.status as StatusKey]) {
      return statusOrder[a.status as StatusKey] - statusOrder[b.status as StatusKey];
    }
    return new Date(a.start_time).getTime() - new Date(b.start_time).getTime();
  });
})

// 数据总览相关
const recentLectures = computed(() => {
  // 仅展示最近5个演讲（按时间倒序）
  return lectures.value
    .slice()
    .sort((a, b) => new Date(b.start_time).getTime() - new Date(a.start_time).getTime())
    .slice(0, 5);
})

const totalAnswers = computed(() => 0)
const avgCorrectRate = computed(() => 0)
const chartLabels = computed(() => recentLectures.value.map(l => formatDate(l.start_time)))
const chartData = computed(() => recentLectures.value.map(() => 0))

function onCreate() {
  router.push({ path: '/create-lecture' });
}

function formatDate(dateString: string) {
  // 只展示本地年月日时分，不处理时区
  const date = new Date(dateString.replace(/-/g, '/'));
  const y = date.getFullYear();
  const m = date.getMonth() + 1;
  const d = date.getDate();
  const h = date.getHours();
  const min = date.getMinutes().toString().padStart(2, '0');
  return `${y}年${m}月${d}日 ${h}:${min}`;
}

function onTabChange(idx: number) {
  activeTab.value = idx;
}

function getStatusClass(status: string | undefined): string {
  if (status === '进行中') return 'active';
  if (status === '已结束') return 'ended';
  if (status === '即将开始') return 'upcoming';
  return '';
}

function toggleMenu(id: number) {
  activeMenu.value = activeMenu.value === id ? null : id;
}

function editLecture(lecture: any) {
  alert(`编辑讲座: ${lecture.name}`);
  activeMenu.value = null;
}

function shareLecture(lecture: any) {
  alert(`分享讲座: ${lecture.name}`);
  activeMenu.value = null;
}

function deleteLecture(lecture: any) {
  if(confirm(`确定删除讲座 "${lecture.name}" 吗？`)) {
    lectures.value = lectures.value.filter(l => l.lid !== lecture.lid);
  }
  activeMenu.value = null;
}
</script>

<style scoped>
/* 折线图tooltip样式 */
.chart-tooltip {
  position: absolute;
  background: #fff;
  color: #1565c0;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  padding: 6px 14px;
  font-size: 0.98rem;
  box-shadow: 0 2px 8px rgba(33,150,243,0.08);
  pointer-events: none;
  z-index: 99;
}

.speaker-home {
  height: 100vh;
  display: flex;
  flex-direction: column;
  padding-bottom: env(safe-area-inset-bottom);
  background: #f8f9fb;
}

.overview-section {
  flex: 1;
  padding: 2rem 1.5rem 80px 1.5rem;
  background: #fff;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.overview-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 1.5rem;
}
.overview-title {
  font-size: 1.2rem;
  font-weight: 600;
  color: #2e7d32;
}
.overview-stats {
  display: flex;
  gap: 2.5rem;
  margin-bottom: 2rem;
}
.stat-item {
  background: #f8f9fb;
  border-radius: 12px;
  padding: 1rem 2rem;
  text-align: center;
  box-shadow: 0 2px 8px rgba(76,175,80,0.07);
}
.stat-label {
  font-size: 0.95rem;
  color: #555;
  margin-bottom: 0.5rem;
}
.stat-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #4caf50;
}
.overview-chart {
  width: 100%;
  max-width: 320px;
  margin: 0 auto;
  background: #f8f9fb;
  border-radius: 16px;
  padding: 1.2rem 1rem 1.5rem 1rem;
  box-shadow: 0 2px 8px rgba(76,175,80,0.07);
}
.chart-title {
  font-size: 1rem;
  color: #333;
  margin-bottom: 0.8rem;
  text-align: center;
}
.chart-container {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 0.8rem;
}
.chart-legend {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: center;
  font-size: 0.92rem;
  color: #555;
}
.legend-item {
  display: flex;
  align-items: center;
  gap: 4px;
}
.legend-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  display: inline-block;
}
.center-section {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #fff;
  font-size: 1.1rem;
  color: #aaa;
}
.center-placeholder {
  text-align: center;
  color: #aaa;
}

.logout-btn {
  margin-top: 2rem;
  background: linear-gradient(135deg, #f44336 0%, #e57373 100%);
  color: #fff;
  border: none;
  border-radius: 10px;
  padding: 0.9rem 2.5rem;
  font-size: 1.08rem;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(244,67,54,0.13);
  transition: all 0.2s;
}
.logout-btn:hover {
  background: #d32f2f;
}

.sh-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 1.8rem;
  background: white;
  box-shadow: 0 2px 15px rgba(0, 0, 0, 0.05);
  position: sticky;
  top: 0;
  z-index: 10;
  width: 100%;
}

.header-title {
  font-size: 1.35rem;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0;
}

.create-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  background: linear-gradient(135deg, #4caf50 0%, #2e7d32 100%);
  color: white;
  border: none;
  border-radius: 12px;
  padding: 0.75rem 1.4rem;
  font-size: 0.95rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1);
  box-shadow: 0 4px 10px rgba(76, 175, 80, 0.2);
}

.create-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 15px rgba(76, 175, 80, 0.3);
}

.create-btn:active {
  transform: translateY(0);
}

.lecture-list {
  flex: 1;
  overflow-y: auto;
  margin: 0;
  padding: 0;
  padding-top: 1.2rem;
  padding-bottom: 72px; /* 额外留出导航栏空间 */
}

.sort-controls {
  display: flex;
  align-items: center;
  padding: 0 1.5rem 1rem 1.5rem;
  font-size: 0.95rem;
  color: #555;
}

.sort-select {
  margin-left: 10px;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  border: 1px solid #e0e0e0;
  background: white;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.sort-select:focus {
  outline: none;
  border-color: #4caf50;
  box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2);
}

.lecture-grid {
  display: grid;
  gap: 1.5rem;
  margin: 0;
  padding: 0 1.5rem;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
}

.lecture-card {
  background: white;
  border-radius: 16px;
  padding: 1.5rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  border: 1px solid #f0f0f0;
  display: flex;
  flex-direction: column;
  min-height: 200px;
}

.lecture-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
  border-color: #e0e0e0;
}

.lecture-card.active {
  border-left: 4px solid #4caf50;
}

.lecture-card.ended {
  border-left: 4px solid #9e9e9e;
}

.lecture-card.upcoming {
  border-left: 4px solid #2196f3;
}

.status-indicator {
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 100%;
}

.status-indicator.active {
  background: #4caf50;
}

.status-indicator.ended {
  background: #9e9e9e;
}

.status-indicator.upcoming {
  background: #2196f3;
}

.lecture-title {
  font-size: 1.15rem;
  color: #1a1a1a;
  margin: 0 0 1rem 0;
  line-height: 1.4;
  font-weight: 600;
}

.lecture-info {
  margin: 0.5rem 0;
  flex: 1;
}

.info-row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 0.75rem;
  font-size: 0.9rem;
  color: #555;
}

.info-row svg {
  flex-shrink: 0;
}

.lecture-meta {
  display: flex;
  justify-content: flex-end;
  margin-top: 0.5rem;
}

.status {
  padding: 0.35rem 0.9rem;
  border-radius: 20px;
  font-weight: 500;
  font-size: 0.85rem;
  display: inline-block;
}

.status.active {
  background: rgba(76, 175, 80, 0.12);
  color: #2e7d32;
}

.status.ended {
  background: #f5f5f5;
  color: #757575;
}

.status.upcoming {
  background: rgba(33, 150, 243, 0.12);
  color: #1565c0;
}

.empty-state {
  text-align: center;
  padding: 4rem 0;
  color: #9e9e9e;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.empty-state p {
  margin: 0;
  font-size: 1rem;
}

.card-hover-content {
  position: absolute;
  top: 12px;
  right: 12px;
  opacity: 0;
  transform: translateY(-5px);
  transition: all 0.25s ease;
  z-index: 2;
}

.lecture-card:hover .card-hover-content {
  opacity: 1;
  transform: translateY(0);
}

.action-btn {
  background: rgba(255, 255, 255, 0.8);
  border: none;
  border-radius: 50%;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  z-index: 3;
}

.action-btn:hover {
  background: white;
  transform: scale(1.1);
}

.action-menu {
  position: absolute;
  top: 40px;
  right: 0;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  min-width: 120px;
  overflow: hidden;
  z-index: 10;
}

.action-menu button {
  display: block;
  width: 100%;
  padding: 0.75rem 1rem;
  text-align: left;
  background: none;
  border: none;
  font-size: 0.9rem;
  color: #333;
  cursor: pointer;
  transition: all 0.2s;
}

.action-menu button:hover {
  background: #f5f5f5;
}

.action-menu button.delete {
  color: #f44336;
}

.action-menu button.delete:hover {
  background: rgba(244, 67, 54, 0.08);
}
</style>
