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
          <h2 class="lecture-title">{{ currentLecture.title }}</h2>
          <div class="meta-info">
            <span>时间：{{ formatDateTime(currentLecture.date, currentLecture.time) }}</span>
            <span>地点：{{ currentLecture.location }}</span>
            <span>参与人数：{{ currentLecture.participants }}</span>
          </div>
          <p class="lecture-desc">{{ currentLecture.description || '暂无简介' }}</p>
        </div>
      </el-tab-pane>
      <el-tab-pane label="听演讲" name="play">
        <div class="ppt-viewer">
          <img :src="currentSlide" class="slide-image" />
          <div class="navigation">
            <span class="slide-page">第 {{ currentPage }} / {{ totalPages }} 页</span>
          </div>
        </div>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const activeTab = ref('play');
const lectures = ref([]);
const currentLecture = ref({});

onMounted(() => {
  if (route.query.lectures) {
    try {
      lectures.value = JSON.parse(route.query.lectures);
    } catch (e) {
      lectures.value = [];
    }
  }
  currentLecture.value = lectures.value.find(l => l.id == route.query.id) || {};
});

const currentPage = ref(1);
const totalPages = 15;
const currentSlide = computed(() => `/slides/slide-${currentPage.value}.jpg`);

// 听众端不能翻页

const formatDateTime = (date, time) => {
  if (!date) return '';
  const dateObj = new Date(date);
  return `${dateObj.getMonth() + 1}月${dateObj.getDate()}日 ${time || ''}`;
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
