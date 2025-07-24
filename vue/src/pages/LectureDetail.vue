<template>
  <div class="lecture-detail">
    <header class="ld-header">
      <button class="back-btn" @click="router.go(-1)">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polyline points="15 18 9 12 15 6"></polyline>
        </svg>
      </button>
      <h2 class="header-title">演讲详情</h2>
    </header>

    <section class="detail-content">
      <div class="status-tag active">进行中</div>
      <h1 class="lecture-title">{{ currentLecture.name }}</h1>

      <div class="meta-info">
        <div class="info-item">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"></circle>
            <polyline points="12 6 12 12 16 14"></polyline>
          </svg>
          <span>{{ formatDateTime(currentLecture.start_time) }}</span>
        </div>
        <div class="info-item">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
            <circle cx="12" cy="10" r="3"></circle>
          </svg>
          <span>{{ Array.isArray(currentLecture.fids) ? currentLecture.fids.length : 0 }}</span>
        </div>
      </div>

      <div class="join-section">
        <button class="primary-join-btn" @click="joinLecture">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
            <circle cx="8.5" cy="7" r="4"></circle>
            <line x1="20" y1="8" x2="20" y2="14"></line>
            <line x1="23" y1="11" x2="17" y2="11"></line>
          </svg>
          立即加入演讲
        </button>
        <div class="participant-count">
          当前参与人数：{{ currentLecture.join_num }}
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '@/utils/api.js';

const route = useRoute();
const router = useRouter();
const currentLecture = ref({});

onMounted(async () => {
  const lid = route.query.lid || route.query.id || '';
  if (lid) {
    try {
      const params = new URLSearchParams();
      params.append('lid', lid);
      const res = await api.post('/lecture_detail', params, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
      });
      if (res && res.lid) {
        currentLecture.value = res;
      }
    } catch (e) {
      currentLecture.value = {};
    }
  }
});

const formatDateTime = (dateTime) => {
  if (!dateTime) return '';
  const dateObj = new Date(dateTime);
  return `${dateObj.getMonth() + 1}月${dateObj.getDate()}日 ${dateObj.getHours()}:${String(dateObj.getMinutes()).padStart(2, '0')}`;
};

const joinLecture = async () => {
  const uid = localStorage.getItem('uid');
  const lid = currentLecture.value.lid;
  if (!uid || !lid) {
    window.$message?.error('用户信息缺失');
    return;
  }
  const form = new FormData();
  form.append('uid', uid);
  form.append('lid', lid);
  try {
    const res = await api.post('/listener/join', form, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
    if (res && res.res) {
      router.push({
        path: '/audience-lecture-play',
        query: {
          lid: lid
        }
      });
    } else {
      window.$message?.error('加入演讲失败');
    }
  } catch (e) {
    window.$message?.error('加入演讲异常');
  }
};
</script>

<style scoped>
.lecture-detail {
  height: 100vh;
  background: white;
}

.ld-header {
  display: flex;
  align-items: center;
  padding: 1.2rem;
  background: white;
  box-shadow: 0 2px 15px rgba(0, 0, 0, 0.05);
}

.back-btn {
  background: none;
  border: none;
  cursor: pointer;
  margin-right: 1rem;
  color: #4caf50;
}

.header-title {
  font-size: 1.2rem;
  color: #1a1a1a;
}

.detail-content {
  padding: 2rem 1.5rem;
}

.status-tag {
  display: inline-block;
  padding: 0.4rem 1rem;
  border-radius: 20px;
  background: rgba(76, 175, 80, 0.15);
  color: #2e7d32;
  font-size: 0.9rem;
  margin-bottom: 1.5rem;
}

.lecture-title {
  font-size: 1.8rem;
  color: #1a1a1a;
  margin: 0 0 2rem 0;
}

.meta-info {
  display: grid;
  gap: 1.5rem;
  margin-bottom: 2.5rem;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  font-size: 1.05rem;
  color: #555;
}

.join-section {
  margin-top: 3rem;
  text-align: center;
}

.primary-join-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.8rem;
  padding: 1.2rem 2.5rem;
  background: linear-gradient(135deg, #4caf50 0%, #2e7d32 100%);
  color: white;
  border: none;
  border-radius: 16px;
  font-size: 1.1rem;
  cursor: pointer;
  transition: transform 0.2s;
}

.primary-join-btn:hover {
  transform: scale(1.05);
}

.participant-count {
  margin-top: 1.5rem;
  color: #666;
  font-size: 0.95rem;
}
</style>
