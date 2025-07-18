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

    <section v-if="activeTab === 'home'" class="lecture-list">
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
            :key="lecture.id"
            class="lecture-card"
            @click="navigateToDetail(lecture.id)">
          <div class="status-indicator active"></div>
          <div class="card-content">
            <h3 class="lecture-title">{{ lecture.title }}</h3>
            <div class="lecture-info">
              <div class="info-row">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <circle cx="12" cy="12" r="10"></circle>
                  <polyline points="12 6 12 12 16 14"></polyline>
                </svg>
                <span>{{ formatDate(lecture.date) }} {{ lecture.time }}</span>
              </div>
              <div class="info-row">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
                  <circle cx="12" cy="10" r="3"></circle>
                </svg>
                <span>{{ lecture.location }}</span>
              </div>
              <div class="info-row">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                  <circle cx="9" cy="7" r="4"></circle>
                  <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                  <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
                </svg>
                <span>{{ lecture.participants }}人参与</span>
              </div>
            </div>
          </div>
          <button class="join-btn" @click.stop="joinLecture(lecture)">
            立即加入
          </button>
        </li>
      </ul>
    </section>

    <section v-else-if="activeTab === 'history'" class="history-list">
      <div v-if="historyLectures.length === 0" class="empty-tip">暂无历史演讲</div>
      <ul v-else>
        <li v-for="lecture in historyLectures" :key="lecture.id" class="history-card">
          <div class="history-title">{{ lecture.title }}</div>
          <div class="history-meta">
            <span>时间：{{ formatDate(lecture.date) }} {{ lecture.time }}</span>
            <span>地点：{{ lecture.location }}</span>
            <span>参与人数：{{ lecture.participants }}</span>
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
const activeTab = ref('home');

// 历史数据假数据
const historyLectures = ref([
  {
    id: 1,
    title: 'AI与未来教育变革趋势分析',
    date: '2025-07-15',
    time: '14:00-16:00',
    location: '线上会议',
    participants: 120,
    status: '已结束'
  },
  {
    id: 2,
    title: '大数据分析实战技巧与应用',
    date: '2025-06-28',
    time: '10:00-12:00',
    location: '科技大厦B座201',
    participants: 85,
    status: '已结束'
  }
]);
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const searchQuery = ref('');
const sortOption = ref('timeAsc');

// 模拟进行中的演讲数据
const lectures = ref([
  {
    id: 1,
    title: 'AI与未来教育变革趋势分析',
    date: '2025-07-15',
    time: '14:00-16:00',
    location: '线上会议',
    participants: 120,
    status: '进行中',
    correctRate: 0.82,
    totalAnswers: 150
  },
  {
    id: 2,
    title: '大数据分析实战技巧与应用',
    date: '2025-06-28',
    time: '10:00-12:00',
    location: '科技大厦B座201',
    participants: 85,
    status: '已结束',
    correctRate: 0.76,
    totalAnswers: 110
  },
  {
    id: 3,
    title: '高效PPT设计与演讲技巧',
    date: '2025-05-15',
    time: '13:30-15:30',
    location: '创新中心报告厅',
    participants: 92,
    status: '已结束',
    correctRate: 0.68,
    totalAnswers: 98
  },
  {
    id: 4,
    title: '云计算架构设计与实践',
    date: '2025-08-22',
    time: '09:00-11:30',
    location: '线上会议',
    participants: 67,
    status: '即将开始',
    correctRate: null,
    totalAnswers: 0
  },
  {
    id: 5,
    title: '前端工程化与性能优化',
    date: '2025-08-05',
    time: '15:00-17:00',
    location: '研发中心会议室',
    participants: 45,
    status: '即将开始',
    correctRate: null,
    totalAnswers: 0
  },
  {
    id: 6,
    title: '区块链技术应用实践',
    date: '2025-07-10',
    time: '13:00-15:00',
    location: '科技园区A栋101',
    participants: 78,
    status: '进行中',
    correctRate: 0.88,
    totalAnswers: 120
  },
]);

const filteredLectures = computed(() => {
  const filtered = lectures.value.filter(l => l.status === '进行中');
  return filtered.sort((a, b) => {
    const dateA = new Date(a.date).getTime();
    const dateB = new Date(b.date).getTime();
    return sortOption.value === 'timeAsc' ? dateA - dateB : dateB - dateA;
  });
});

const formatDate = (dateString) => {
  const date = new Date(dateString);
  return `${date.getMonth() + 1}月${date.getDate()}日`;
};

const joinLecture = (lecture) => {
  // 跳转到详情页并传递id和lectures数据
  router.push({
    path: '/lecture-detail',
    query: {
      id: lecture.id,
      lectures: JSON.stringify(lectures.value)
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
