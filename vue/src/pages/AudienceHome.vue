<!-- AudienceHome.vue -->
<template>
  <div class="audience-home">
    <header class="ah-header">
      <h2 class="header-title">公开演讲</h2>
      <div class="search-box" v-if="activeTab === 'home'">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="11" cy="11" r="8"></circle>
          <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
        </svg>
        <input type="text" placeholder="搜索演讲主题或地点" v-model="searchQuery">
      </div>
    </header>

    <section v-if="activeTab === 'home'">
      <div class="lecture-list">
      <div class="lecture-list-header">
        <span></span>
        <button class="sort-btn" @click="toggleSort">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="6 9 12 15 18 9"></polyline>
          </svg>
          <span :class="{'active-sort': sortOption==='timeAsc'}" v-if="sortOption==='timeAsc'">时间从近到远</span>
          <span :class="{'active-sort': sortOption==='timeDesc'}" v-else>时间从远到近</span>
        </button>
      </div>

      <ul class="lecture-grid">
        <li v-for="lecture in filteredLectures"
            :key="lecture.lid"
            class="lecture-card"
            @click="navigateToDetail(lecture.lid)">
          <div class="status-indicator active"></div>
          <div class="card-content">
            <h3 class="lecture-title">{{ lecture.name }}</h3>
            <div class="lecture-info">
              <div class="info-row">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <circle cx="12" cy="12" r="10"></circle>
                  <polyline points="12 6 12 12 16 14"></polyline>
                </svg>
                <span>{{ formatDate(lecture.start_time) }}</span>
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
          <button class="join-btn" @click.stop="joinLecture(lecture)">
            立即加入
          </button>
        </li>
      </ul>
      </div>
    </section>

    <section v-else-if="activeTab === 'history'" class="history-list">
      <div class="heatmap-section">
        <h3 class="heatmap-title">每日答题正确率热力图</h3>
        <div class="heatmap-container">
          <div class="heatmap-row">
            <div v-for="(item, idx) in heatmapData" :key="idx" class="heatmap-cell" :title="item.date + (item.rate !== null ? (' 正确率: ' + item.rate + '%') : ' 无答题')"
              :style="{background: item.rate === null ? '#f5f5f5' : getHeatColor(item.rate)}">
              <span v-if="item.rate !== null">{{ item.rate }}%</span>
            </div>
          </div>
          <div class="heatmap-labels">
            <span v-for="(item, idx) in heatmapData" :key="'label'+idx" class="heatmap-label">{{ item.date.slice(5) }}</span>
          </div>
        </div>
      </div>
      <div v-if="historyLectures.length === 0" class="empty-tip">暂无历史演讲</div>
      <ul v-else>
        <li v-for="lecture in historyLectures" :key="lecture.lid" class="history-card">
          <div class="history-title">{{ lecture.name }}</div>
          <div class="history-meta">
            <span>时间：{{ formatDate(lecture.start_time) }}</span>
            <span>演讲者：{{ lecture.speaker }}</span>
            <span>文件数：{{ lecture.fids.length }}</span>
          </div>
          <div class="history-status">{{ lecture.status }}</div>
        </li>
      </ul>
    </section>

    <section v-else-if="activeTab === 'profile'" class="profile-content">
      <div class="profile-avatar">
        <svg viewBox="0 0 48 48" width="80" height="80" fill="none">
          <circle cx="24" cy="24" r="22" fill="#e3f2fd" stroke="#1565c0" stroke-width="2" />
          <circle cx="24" cy="20" r="8" fill="#90caf9" />
          <ellipse cx="24" cy="36" rx="12" ry="7" fill="#bbdefb" />
        </svg>
      </div>
      <div class="profile-info">
        <div class="profile-name">听众用户</div>
        <div class="profile-desc">个人中心功能开发中...</div>
      </div>
      <button class="logout-btn" @click="logout">退出登录</button>
    </section>

    <nav class="bottom-tabs">
      <div class="tab-item" :class="{active: activeTab==='home'}" @click="activeTab='home'">
        <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
        <span>加入演讲</span>
      </div>
      <div class="tab-item" :class="{active: activeTab==='history'}" @click="activeTab='history'">
        <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2"></rect><path d="M16 2v4M8 2v4M3 10h18"></path></svg>
        <span>历史数据</span>
      </div>
      <div class="tab-item" :class="{active: activeTab==='profile'}" @click="activeTab='profile'">
        <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="7" r="4"></circle><path d="M5.5 21a8.38 8.38 0 0 1 13 0"></path></svg>
        <span>个人中心</span>
      </div>
    </nav>
  </div>
</template>

<script setup>
import { onMounted, ref, computed, watch } from 'vue';
const heatmapData = ref([]);
// 获取个人历史正确率
async function fetchPersonalHistoryRate() {
  const uid = localStorage.getItem('uid');
  if (!uid) return;
  try {
    // 取近14天
    const form = new FormData();
    form.append('uid', uid);
    form.append('day', 14);
    const res = await api.post('/statistics/personal_history_rate', form, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
    if (res && Array.isArray(res.rates) && Array.isArray(res.date)) {
      heatmapData.value = res.date.map((date, i) => ({ date, rate: res.rates[i] }));
    }
  } catch (e) {
    // 可加全局提示
  }
}


function getHeatColor(rate) {
  if (rate === null) return '#f5f5f5';
  if (rate >= 95) return '#43a047';
  if (rate >= 80) return '#8bc34a';
  if (rate >= 60) return '#ffe082';
  return '#ef5350';
}
const logout = () => {
  localStorage.removeItem('uid');
  localStorage.removeItem('type');
  router.replace('/login');
}
const activeTab = ref('home');

// 历史演讲数据
const historyLectures = ref([]);

// 获取历史加入的演讲
async function fetchHistoryLectures() {
  const uid = localStorage.getItem('uid');
  if (!uid) return;
  try {
    const form = new FormData();
    form.append('uid', uid);
    const res = await api.post('/listener/history', form, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
    if (res && Array.isArray(res.data)) {
      historyLectures.value = res.data.map(item => ({
        ...item,
        status: item.state === 'ongoing' ? '进行中' : item.state === 'upcoming' ? '即将开始' : '已结束'
      }));
    }
  } catch (e) {
    // 可加全局提示
  }
}
import { useRouter } from 'vue-router';

const router = useRouter();
const searchQuery = ref('');
const sortOption = ref('timeAsc');

import api from '@/utils/api.js';
const lectures = ref([]);

// 页面加载时获取所有演讲信息
onMounted(async () => {
  try {
    const res = await api.post('/all_lecture');
    if (res) {
      // 兼容字段名，后端state转为status
      lectures.value = res.map(item => ({
        ...item,
        status: item.state === 'ongoing' ? '进行中' : item.state === 'upcoming' ? '即将开始' : '已结束'
      }));
    }
  } catch (e) {
    // 可加全局提示
  }
});

const filteredLectures = computed(() => {
  // 支持搜索和状态过滤
  let filtered = lectures.value.filter(l => l.status === '进行中');
  if (searchQuery.value) {
    const q = searchQuery.value.trim().toLowerCase();
    filtered = filtered.filter(l =>
      (l.name && l.name.toLowerCase().includes(q)) ||
      (l.speaker && l.speaker.toLowerCase().includes(q))
    );
  }
  return filtered.sort((a, b) => {
    const dateA = new Date(a.start_time).getTime();
    const dateB = new Date(b.start_time).getTime();
    return sortOption.value === 'timeAsc' ? dateA - dateB : dateB - dateA;
  });
});

const formatDate = (dateString) => {
  const date = new Date(dateString);
  return `${date.getMonth() + 1}月${date.getDate()}日`;
};
// 监听tab切换到history时拉取数据
watch(() => activeTab.value, (val) => {
  if (val === 'history') {
    fetchPersonalHistoryRate();
    fetchHistoryLectures();
  }
});
const joinLecture = (lecture) => {
  // 跳转到详情页只传lid
  router.push({
    path: '/lecture-detail',
    query: {
      lid: lecture.lid
    }
  });
};

const navigateToDetail = (id) => {
  // 仅卡片点击时不跳转
};

const toggleSort = () => {
  sortOption.value = sortOption.value === 'timeAsc' ? 'timeDesc' : 'timeAsc';
};

const goToHistory = () => {
  router.push('/audience-history');
};
const goToProfile = () => {
  router.push('/audience-profile');
};
</script>

<style scoped>
.heatmap-section {
  max-width: 900px;
  margin: 24px auto 0 auto;
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
  padding: 18px 18px 12px 18px;
}
.heatmap-title {
  font-size: 1.1rem;
  color: #1976d2;
  font-weight: 600;
  margin-bottom: 10px;
}
.heatmap-container {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}
.heatmap-row {
  display: flex;
  gap: 6px;
  margin-bottom: 6px;
}
.heatmap-cell {
  width: 36px;
  height: 36px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.95rem;
  color: #222;
  font-weight: 600;
  box-shadow: 0 1px 3px rgba(0,0,0,0.04);
  transition: background 0.2s;
}
.heatmap-labels {
  display: flex;
  gap: 6px;
  margin-top: 2px;
}
.heatmap-label {
  width: 36px;
  text-align: center;
  font-size: 0.8rem;
  color: #888;
}
.history-list {
  max-width: 900px;
  margin: 30px auto;
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
  padding: 24px 18px;
}
.history-card {
  background: #f8f9fb;
  border-radius: 8px;
  padding: 18px 16px;
  margin-bottom: 18px;
  box-shadow: 0 2px 8px rgba(44, 62, 80, 0.06);
}
.history-title {
  font-size: 1.15rem;
  color: #2e7d32;
  font-weight: 700;
  margin-bottom: 8px;
}
.history-meta {
  color: #1565c0;
  font-size: 0.98rem;
  margin-bottom: 6px;
  display: flex;
  gap: 18px;
}
.history-status {
  color: #888;
  font-size: 0.95rem;
}
.empty-tip {
  color: #aaa;
  text-align: center;
  margin: 40px 0;
  font-size: 1.1rem;
}
.profile-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 32px;
}
.profile-avatar {
  margin-bottom: 18px;
}
.profile-name {
  font-size: 1.2rem;
  color: #2e7d32;
  font-weight: 700;
  margin-bottom: 8px;
}
.profile-desc {
  color: #888;
  font-size: 1.05rem;
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
/* 延续演讲者页面样式并优化 */
.audience-home {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f8f9fb;
}

.ah-header {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
  padding: 1.5rem;
  background: white;
  box-shadow: 0 2px 15px rgba(0, 0, 0, 0.05);
}

.header-title {
  font-size: 1.35rem;
  color: #1a1a1a;
  margin: 0;
}

.search-box {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  padding: 0.8rem 1.2rem;
  background: #f5f5f5;
  border-radius: 12px;
}

.search-box input {
  flex: 1;
  border: none;
  background: transparent;
  font-size: 0.95rem;
}

.search-box input:focus {
  outline: none;
}

.lecture-list-header {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  padding: 1.2rem 1.5rem 0 1.5rem;
}
.sort-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: none;
  border: none;
  color: #4caf50;
  font-size: 1rem;
  cursor: pointer;
  padding: 0.2rem 0.8rem;
  border-radius: 8px;
  transition: background 0.2s;
}
.sort-btn:hover {
  background: #e8f5e9;
}
.active-sort {
  color: #2e7d32;
  font-weight: 600;
}

.lecture-card {
  position: relative;
  background: white;
  border-radius: 16px;
  padding: 1.5rem;
  margin-bottom: 1rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
  transition: transform 0.3s ease;
}

.lecture-card:hover {
  transform: translateY(-3px);
}

.join-btn {
  width: 100%;
  padding: 0.9rem;
  margin-top: 1.2rem;
  background: linear-gradient(135deg, #4caf50 0%, #2e7d32 100%);
  color: white;
  border: none;
  border-radius: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: opacity 0.2s;
}

.join-btn:hover {
  opacity: 0.9;
}

.lecture-grid {
  display: grid;
  gap: 1.5rem;
  margin: 0;
  padding: 0 1.5rem;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
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

.status-indicator {
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 100%;
}

.status-indicator.active {
  background: #4caf50 !important;
}

.status-indicator.ended {
  background: #9e9e9e;
}

.status-indicator.upcoming {
  background: #2196f3;
}

.bottom-tabs {
  position: fixed;
  left: 0;
  right: 0;
  bottom: 0;
  height: 62px;
  background: #fff;
  box-shadow: 0 -2px 12px rgba(0,0,0,0.06);
  display: flex;
  justify-content: space-around;
  align-items: center;
  z-index: 10;
}
.tab-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  color: #888;
  font-size: 0.95rem;
  cursor: pointer;
  padding: 0.2rem 0.5rem;
  transition: color 0.2s;
}
.tab-item.active {
  color: #4caf50;
  font-weight: 600;
}
.tab-item svg {
  margin-bottom: 2px;
}

.lecture-title {
  color: #222;
  font-weight: 600;
}

</style>
