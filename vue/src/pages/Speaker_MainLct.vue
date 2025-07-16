<template>
  <div class="container">
    <el-tabs type="border-card" class="custom-tabs">
      <!-- 主要信息选项卡 -->
      <el-tab-pane label="基本信息">
        <div class="info-container">
          <div class="main-info">
            <div class="info-header">
              <span class="speaker-avatar">
                <svg viewBox="0 0 48 48" width="60" height="60" fill="none">
                  <circle cx="24" cy="24" r="22" fill="#e3f2fd" stroke="#1565c0" stroke-width="2" />
                  <circle cx="24" cy="20" r="8" fill="#90caf9" />
                  <ellipse cx="24" cy="36" rx="12" ry="7" fill="#bbdefb" />
                </svg>
              </span>
              <div>
                <h2 class="main-title">{{ presentation.title }}</h2>
              </div>
            </div>
            <div class="stats">
              <el-statistic title="参与人数" :value="presentation.participants" class="stat-green" />
              <el-statistic title="开始时间" :value="presentation.startTime" class="stat-blue" />
            </div>
            <p class="description main-desc">{{ presentation.description }}</p>
          </div>

          <div class="courseware-section">
            <h3 class="section-title">课件管理</h3>
            <el-upload action="/api/upload" :on-success="handleUploadSuccess">
              <el-button type="primary">上传课件</el-button>
            </el-upload>
            <ul class="file-list">
              <li v-for="file in presentation.files" :key="file.name">
                <span class="file-name">{{ file.name }}</span>
                <span class="upload-time">({{ file.size }})</span>
              </li>
            </ul>
          </div>
        </div>
      </el-tab-pane>

      <!-- 演讲控制选项卡 -->
      <el-tab-pane label="演讲控制">
        <div class="presentation-control">
          <div class="ppt-viewer">
            <div class="ppt-container">
              <img :src="currentSlide" class="slide-image" />
              <div class="navigation">
                <el-button @click="prevSlide" :disabled="currentPage === 1">上一页</el-button>
                <span class="slide-page">第
                  <el-input-number v-model="currentPage" :min="1" :max="totalPages" size="small" :style="{width: (String(totalPages).length * 18 + 50) + 'px', margin: '0 6px'}" />
                  / {{ totalPages }} 页
                </span>
                <el-button @click="nextSlide" :disabled="currentPage === totalPages">下一页</el-button>
              </div>
              <div class="file-select">
                <el-select v-model="selectedFile" placeholder="选择课件" style="width:180px;">
                  <el-option v-for="file in presentation.files" :key="file.name" :label="file.name" :value="file.name" />
                </el-select>
              </div>
            </div>

            <div class="control-cards">
              <el-card class="accuracy-card">
                <h4 class="card-title">总体正确率</h4>
                <el-progress
                  type="dashboard"
                  :percentage="correctRate"
                  :color="progressColor"
                />
              </el-card>

              <el-card class="quiz-card">
                <h4 class="card-title">发送题目</h4>
                <div class="quiz-input">
                  <el-input-number v-model="startPage" :min="1" :max="totalPages" />
                  <span class="quiz-range">至</span>
                  <el-input-number v-model="endPage" :min="1" :max="totalPages" />
                </div>
                <el-button
                  type="success"
                  @click="sendQuiz"
                  :disabled="!isRangeValid"
                >
                  发送当前页题目
                </el-button>
              </el-card>
            </div>
          </div>
        </div>
      </el-tab-pane>

      <!-- 详细数据选项卡 -->
      <el-tab-pane label="数据统计">
        <div class="data-analytics">
          <el-card class="data-card">
            <h3 class="section-title">总体正确率</h3>
            <el-progress
              type="circle"
              :percentage="correctRate"
              :color="progressColor"
            />
          </el-card>
          <el-card class="data-card">
            <h3 class="section-title">参与者排名</h3>
            <el-table :data="rankingData" class="ranking-table" border>
              <el-table-column prop="rank" label="排名" width="80">
                <template #default="{ row }">
                  <span class="table-rank">{{ row.rank }}</span>
                </template>
              </el-table-column>
              <el-table-column prop="name" label="参与者">
                <template #default="{ row }">
                  <span class="table-name">{{ row.name }}</span>
                </template>
              </el-table-column>
              <el-table-column prop="accuracy" label="正确率" sortable>
                <template #default="{ row }">
                  <span class="table-accuracy">{{ row.accuracy }}%</span>
                </template>
              </el-table-column>
            </el-table>
          </el-card>
        </div>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

// 演示数据
const presentation = ref({
  title: "人工智能发展趋势",
  participants: 128,
  startTime: "2024-03-20 14:30",
  description: "本次演讲将深入探讨AI领域的最新发展...",
  files: [
    { name: "PPT-Chapter1.pdf", size: "2.4MB", uploadTime: "14:25" },
    { name: "Case-Study.pdf", size: "1.8MB", uploadTime: "14:28" }
  ]
})

// PPT控制
const currentPage = ref(1)
const totalPages = 15
const currentSlide = computed(() => `/slides/slide-${currentPage.value}.jpg`)
const selectedFile = ref('')

// 翻页跳转输入
const jumpPage = ref('')
function handleJumpPage() {
  const page = Number(jumpPage.value)
  if (!isNaN(page) && page >= 1 && page <= totalPages) {
    currentPage.value = page
    jumpPage.value = ''
  }
}

// 正确率数据
const correctRate = ref(78.5)
const progressColor = computed(() => {
  return correctRate.value > 80 ? '#67C23A' : '#E6A23C'
})

// 题目发送
const startPage = ref(1)
const endPage = ref(currentPage.value)
const isRangeValid = computed(() => startPage.value <= endPage.value)

// 自动同步 endPage
import { watch } from 'vue'
watch(currentPage, (val) => {
  endPage.value = val
})

// 排名数据
const rankingData = ref([
  { rank: 1, name: "张三", accuracy: 92 },
  { rank: 2, name: "李四", accuracy: 88 },
  { rank: 3, name: "王五", accuracy: 85 }
])

const prevSlide = () => currentPage.value--
const nextSlide = () => currentPage.value++
const sendQuiz = () => {
  console.log(`发送题目：第${startPage.value}-${endPage.value}页`)
}
const handleUploadSuccess = (response) => {
  presentation.value.files.push({
    name: response.filename,
    size: response.size,
    uploadTime: new Date().toLocaleTimeString()
  })
}
</script>

<style scoped>




.info-header {
  display: flex;
  align-items: center;
  gap: 18px;
  margin-bottom: 10px;
}
.speaker-avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  object-fit: cover;
  box-shadow: 0 2px 8px rgba(44, 62, 80, 0.12);
}
.tags {
  display: flex;
  gap: 8px;
  margin-top: 4px;
}
.tag {
  background: #e3f2fd;
  color: #1565c0;
  font-size: 0.92rem;
  padding: 2px 10px;
  border-radius: 12px;
  font-weight: 500;
}
.main-title {
  color: #2e7d32;
  font-size: 1.25rem;
  font-weight: 700;
  margin-bottom: 2px;
}
.main-desc {
  color: #333;
  font-size: 1.02rem;
  margin-top: 8px;
}
.section-title {
  color: #1565c0;
  font-size: 1.08rem;
  font-weight: 600;
  margin-bottom: 8px;
}
.file-name {
  color: #2e7d32;
  font-weight: 500;
}
.file-size {
  color: #909399;
  margin-left: 6px;
}
.upload-time {
  color: #1565c0;
  margin-left: 12px;
  font-size: 0.95em;
}
.slide-page {
  color: #1565c0;
  font-size: 1.08rem;
  font-weight: 500;
  display: flex;
  align-items: center;
}
.slide-page-num {
  color: #2e7d32;
  font-weight: 700;
}
.file-select {
  margin-top: 12px;
  text-align: right;
}
.card-title {
  color: #2e7d32;
  font-size: 1.08rem;
  font-weight: 600;
  margin-bottom: 8px;
}
.quiz-range {
  color: #1565c0;
  font-weight: 500;
}
.table-rank {
  color: #2e7d32;
  font-weight: 700;
}
.table-name {
  color: #1565c0;
  font-weight: 500;
}
.table-accuracy {
  color: #E6A23C;
  font-weight: 700;
}
.stat-green .el-statistic__head, .stat-green .el-statistic__content {
  color: #2e7d32 !important;
}
.stat-blue .el-statistic__head, .stat-blue .el-statistic__content {
  color: #1565c0 !important;
}
.data-analytics {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  padding: 20px;
}
.data-card {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(44, 62, 80, 0.08);
  padding: 18px 16px;
  margin-bottom: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  min-height: 320px;
}
@media (max-width: 900px) {
  .container {
    max-width: 100vw;
    margin: 0;
    border-radius: 0;
    box-shadow: none;
  }
  .custom-tabs {
    height: auto;
    min-height: 100vh;
  }
  .info-container, .data-analytics {
    grid-template-columns: 1fr;
    gap: 18px;
    padding: 10px;
  }
  .ppt-viewer {
    grid-template-columns: 1fr;
    height: auto;
    gap: 10px;
  }
  .slide-image {
    height: 220px;
  }
  .accuracy-card, .quiz-card, .data-card {
    height: auto;
    min-height: 180px;
  }
  .data-analytics {
    grid-template-columns: 1fr;
    gap: 16px;
    padding: 8px;
  }
}

.container {
  max-width: 1200px;
  margin: 20px auto;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.1);
}

.custom-tabs {
  height: 800px;
}
.el-card{
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
}

.info-container {
  display: grid;
  grid-template-columns: 1fr 300px;
  gap: 30px;
  padding: 20px;
}
@media (max-width: 900px) {
  .info-container {
    display: flex;
    flex-direction: column;
    gap: 18px;
    padding: 10px;
  }
}

.stats {
  display: flex;
  gap: 40px;
  margin: 20px 0;
}

.file-list {
  list-style: none;
  padding: 0;
  margin-top: 15px;
}

.file-list li {
  padding: 8px;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
}

.ppt-viewer {
  display: grid;
  grid-template-columns: 3fr 1fr;
  gap: 20px;
  height: 650px;
}
@media (max-width: 900px) {
  .ppt-viewer {
    display: flex;
    flex-direction: column;
    gap: 10px;
    height: auto;
  }
}

.slide-image {
  width: 100%;
  height: 500px;
  object-fit: contain;
  background: #f0f0f0;
  border-radius: 8px;
}

.navigation {
  margin-top: 20px;
  display: flex;
  align-items: center;
  gap: 15px;
  justify-content: center;
}

.control-cards {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.accuracy-card, .quiz-card, .el-card body, .el-card__body {
  height: 300px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
.quiz-card h4,
.quiz-card .quiz-input,
.quiz-card .el-button {
  width: 100%;
  text-align: center;
  display: flex;
  justify-content: center;
  align-items: center;
}
}
.el-card__body{
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
.quiz-input {
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 15px 0;
}


.data-analytics {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 30px;
  padding: 20px;
}
@media (max-width: 900px) {
  .data-analytics {
    display: flex;
    flex-direction: column;
    gap: 16px;
    padding: 8px;
  }
}

.data-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 400px;
}

.ranking-table {
  margin-top: 20px;
}
@media (max-width: 900px) {
  html, body, #app {
    height: auto !important;
    min-height: 100% !important;
    overflow-y: visible !important;
    width: 100%;
  }

  .custom-tabs {
    height: auto;
    min-height: auto;
  }

  .el-tabs {
    flex-direction: column;
    overflow: visible;
  }

  .ppt-viewer {
    height: auto;
    min-height: auto;
    width: 100vw;
    max-width: 100vw;
    box-sizing: border-box;
  }
  .ppt-container {
    width: 100vw;
    max-width: 100vw;
    box-sizing: border-box;
  }

  .container {
    overflow: visible;
    border-radius: 0;
    box-shadow: none;
  }
}
@media (max-width: 900px) {
  .ppt-container {
    width: 100vw;
    max-width: 100%;
    box-sizing: border-box;
    padding: 0 10px; /* 保持与父容器一致的边距 */
  }

  /* 优化图片显示 */
  .slide-image {
    height: auto;
    max-height: 60vh; /* 限制最大高度 */
    width: 100%;
    aspect-ratio: 16/9; /* 保持PPT比例 */
  }

  /* 修复控制卡片宽度 */
  .control-cards {
    width: 100%;
    padding: 0 10px;
  }
}
</style>
