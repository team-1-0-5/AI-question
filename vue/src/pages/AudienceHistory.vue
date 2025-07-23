<template>
  <div class="audience-history">
    <header class="top-bar">
      <button class="back-btn" @click="$router.go(-1)">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polyline points="15 18 9 12 15 6"></polyline>
        </svg>
      </button>
      <span class="bar-title">历史数据</span>
    </header>
    <div class="history-list">
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
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
// 假数据，实际可从后端获取
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
const formatDate = (dateString) => {
  const date = new Date(dateString);
  return `${date.getMonth() + 1}月${date.getDate()}日`;
};
</script>

<style scoped>
.audience-history {
  max-width: 900px;
  margin: 30px auto;
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
  padding: 24px 18px;
}
.top-bar {
  display: flex;
  align-items: center;
  height: 56px;
  background: #fff;
  box-shadow: 0 2px 12px rgba(0,0,0,0.06);
  padding: 0 1.5rem;
  position: sticky;
  top: 0;
  z-index: 20;
}
.back-btn {
  background: none;
  border: none;
  cursor: pointer;
  margin-right: 1rem;
  color: #4caf50;
  display: flex;
  align-items: center;
}
.bar-title {
  font-size: 1.18rem;
  color: #1a1a1a;
  font-weight: 600;
}
.history-list {
  margin-top: 24px;
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
</style>
