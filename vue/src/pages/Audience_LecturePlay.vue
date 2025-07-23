<template>
  <div class="audience-lecture-play">
    <header class="top-bar">
      <button class="back-btn" @click="$router.go(-1)">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polyline points="15 18 9 12 15 6"></polyline>
        </svg>
      </button>
      <span class="bar-title">听演讲</span>
    </header>
    <el-tabs v-model="activeTab" class="custom-tabs">
      <el-tab-pane label="演讲详情" name="detail">
        <div class="lecture-detail-pane">
          <h2 class="lecture-title">{{ currentLecture.name }}</h2>
          <div class="meta-info">
            <span>时间：{{ formatDateTime(currentLecture.start_time) }}</span>
            <span>演讲者：{{ currentLecture.speaker }}</span>
            <span>参与人数：{{ currentLecture.join_num }}</span>
          </div>
        </div>
      </el-tab-pane>
      <el-tab-pane label="听演讲" name="play">
        <div class="ppt-viewer">
          <img :src="currentSlide" class="slide-image" />
          <img :src="currentSlide" class="slide-image" v-if="currentSlide" />
            <div class="navigation">
              <span class="slide-page">第 {{ currentPage }} 页</span>
            </div>
        </div>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '@/utils/api.js';

const route = useRoute();
const router = useRouter();
const activeTab = ref('play');
const currentLecture = ref({});
const currentPage = ref(1);
const currentPicFid = ref('');
const currentSlide = computed(() => {
  if (!currentPicFid.value) return '';
  const uid = localStorage.getItem('uid') || '';
  return `/download?fid=${currentPicFid.value}&uid=${uid}`;
});

let ws = null;
onMounted(async () => {
  // 只通过lid获取演讲详情
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

  // 建立WebSocket连接
  const uid = localStorage.getItem('uid') || '';
  if (uid && lid) {
    const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsHost = window.location.hostname + (window.location.port ? ':' + window.location.port : '');
    ws = new WebSocket(`ws://localhost:8000/ws/ppt?uid=${uid}&lid=${lid}`);
    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        // PPT翻页推送
        if (data.page && data.pic_fid) {
          currentPage.value = data.page;
          currentPicFid.value = data.pic_fid;
        }
        // 题目推送
        if (data.questions && Array.isArray(data.questions)) {
          // 跳转到答题页面并传递题目数据
          router.push({
            path: '/answer-quiz',
            query: {
              questions: encodeURIComponent(JSON.stringify(data.questions)),
              times: data.times || 1,
              lid: lid
            }
          });
        }
      } catch (e) {}
    };
  }
});
onUnmounted(() => {
  if (ws) ws.close();
});
const formatDateTime = (dateTime) => {
  if (!dateTime) return '';
  const dateObj = new Date(dateTime);
  return `${dateObj.getMonth() + 1}月${dateObj.getDate()}日 ${dateObj.getHours()}:${String(dateObj.getMinutes()).padStart(2, '0')}`;
};
</script>

<style scoped>
.audience-lecture-play {
  max-width: 1200px;
  margin: 40px 0;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 16px rgba(0,0,0,0.10);
  padding: 40px 40px 32px 40px;
}
.custom-tabs {
  min-height: 600px;
}
.lecture-detail-pane {
  padding: 18px 8px;
}
.lecture-title {
  font-size: 1.5rem;
  color: #2e7d32;
  font-weight: 700;
  margin-bottom: 10px;
}
.meta-info {
  color: #1565c0;
  font-size: 1.05rem;
  margin-bottom: 12px;
  display: flex;
  gap: 18px;
}
.lecture-desc {
  color: #333;
  font-size: 1.08rem;
  margin-top: 10px;
}
.ppt-viewer {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 18px;
  margin-top: 20px;
}
.slide-image {
  width: 100%;
  max-width: 1000px;
  height: 520px;
  object-fit: contain;
  background: #f0f0f0;
  border-radius: 10px;
}
@media (max-width: 900px) {
  .audience-lecture-play {
    max-width: 100vw;
    margin: 0;
    border-radius: 0;
    box-shadow: none;
    padding: 10px 0 0 0;
  }
  .custom-tabs {
    min-height: 100vh;
  }
  .slide-image {
    height: 220px;
    max-width: 100vw;
  }
}
.navigation {
  display: flex;
  align-items: center;
  gap: 18px;
  margin-top: 10px;
}
.slide-page {
  color: #1565c0;
  font-weight: 600;
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
</style>
