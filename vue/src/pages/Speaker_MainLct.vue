
<template>
  <div class="container">
    <div>
      <el-button type="link" @click="$router.push('/')" icon="ArrowLeft" style="font-size:1.08rem;color:#1565c0;">
        返回首页
      </el-button>
    </div>
    <el-tabs type="border-card" class="custom-tabs" @tab-click="handleTabClick">
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
              <el-statistic title="开始时间" :value="new Date(presentation.startTime)" class="stat-blue" />
            </div>
            <p class="description main-desc">{{ presentation.description }}</p>
            <div style="margin-top: 28px; text-align: right;">
              <el-button type="danger" @click="endPresentation">结束演讲</el-button>
            </div>
          </div>

          <div class="courseware-section">
            <h3 class="section-title">课件管理</h3>
            <el-upload :http-request="customUpload" show-file-list="false">
              <el-button type="primary">上传课件</el-button>
            </el-upload>
            <ul class="file-list">
              <li v-for="file in presentation.files" :key="file.name">
                <a
                  class="file-name"
                  :href="'#'"
                  @click.prevent="downloadFile(file)"
                  style="color:#2e7d32;text-decoration:underline;cursor:pointer;"
                >{{ file.name }}</a>
                <span class="upload-time">({{ (file.size/1024/1024).toFixed(2) }}MB)</span>
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
                <span class="slide-page">第
                  <el-input-number v-model="currentPage" :min="1" :max="totalPages" size="small" :style="{width: (String(totalPages).length * 18 + 50) + 'px', margin: '0 6px'}" />
                  / {{ totalPages }} 页
                </span>
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
// 标签页切换时自动刷新正确率和排名
function handleTabClick(tab) {
  // 仅在切换到“数据统计”或“演讲控制”时刷新
  if (tab.label === '数据统计' || tab.label === '演讲控制') {
    fetchRateAndRanking();
  }
}
// 发送题目功能，表单方式请求 /speaker/post_answer
const sendQuiz = async () => {
  if (!lid.value) {
    window.$message?.error('演讲ID缺失');
    return;
  }
  // 获取当前选中的课件文件fid
  let fid = '';
  if (selectedFile.value) {
    const fileObj = presentation.value.files.find(f => f.name === selectedFile.value);
    if (fileObj && fileObj.fid) fid = fileObj.fid;
  }
  const params = new FormData();
  params.append('lid', String(lid.value));
  if (fid) params.append('fid', String(fid));
  if (startPage.value) params.append('start_page', String(startPage.value));
  if (endPage.value) params.append('end_page', String(endPage.value));
  try {
    const res = await axios.post('/speaker/post_answer', params, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
    if (res && res.res) {
      window.$message?.success('题目已成功发送！');
    } else {
      window.$message?.error('题目发送失败');
    }
  } catch (e) {
    window.$message?.error('题目发送异常');
  }
}
import { ref, computed, onMounted } from 'vue'
import axios from '@/utils/api.js'
import { useRoute } from 'vue-router'

// 获取路由参数 lid
const route = useRoute();
const lid = computed(() => Number(route.query.lid) || Number(route.params.lid) || 1);

// 演讲详情数据
const presentation = ref({
  title: '',
  participants: 0,
  startTime: '',
  description: '',
  speaker: '',
  files: [],
  lid: 0,
  join_num: 0
});

onMounted(async () => {
  const form = new FormData();
  form.append('lid', String(lid.value));
  try {
    const res = await axios.post('/lecture_detail', form, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
    if (res && res.lid) {
      presentation.value.lid = res.lid;
      presentation.value.title = res.name || '';
      presentation.value.speaker = res.speaker || '';
      presentation.value.startTime = res.start_time || '';
      presentation.value.join_num = res.join_num || 0;
      presentation.value.participants = res.join_num || 0;
      // 文件id列表转为文件对象，补充详细信息
      presentation.value.files = [];
      const uid = localStorage.getItem('uid');
      if (Array.isArray(res.fids) && uid) {
        for (const fid of res.fids) {
          const fileForm = new FormData();
          fileForm.append('fid', String(fid));
          fileForm.append('uid', String(uid));
          try {
            const fileRes = await axios.post('/file_info', fileForm, {
              headers: { 'Content-Type': 'multipart/form-data' }
            });
            if (fileRes && fileRes.fid) {
              presentation.value.files.push({
                fid: fileRes.fid,
                name: fileRes.file_name || `文件${fid}`,
                owner: fileRes.owner || '',
                size: fileRes.size || '',
                uploadTime: fileRes.uploadTime || ''
              });
            }
          } catch {}
        }
      }
    }
  } catch (e) {
    window.$message?.error('演讲详情获取失败');
  }
});

// PPT控制
const currentPage = ref(1)
const totalPages = ref(1)
const currentSlide = ref('') // 用于展示ppt图片
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

// 正确率及排名数据
const correctRate = ref(80)
const rankingData = ref([])
const progressColor = computed(() => {
  return correctRate.value > 80 ? '#67C23A' : '#E6A23C'
})

// 获取单次演讲正确率和参与者排名
async function fetchRateAndRanking() {
  const params = new URLSearchParams();
  params.append('lid', String(lid.value));
  try {
    const res = await axios.post('/speaker/speak_rate', params, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    });
    if (res && typeof res.total_rate === 'number') {
      correctRate.value = res.total_rate;
    }
    // personal_rate: {uid: rate}
    if (res && res.personal_rate && typeof res.personal_rate === 'object') {
      // personal_rate: {username: rate}
      const arr = Object.entries(res.personal_rate)
        .sort((a, b) => b[1] - a[1])
        .map(([username, rate], idx) => ({
          rank: idx + 1,
          name: username,
          accuracy: rate
        }));
      rankingData.value = arr;
    }
  } catch {}
}

// 题目发送
const startPage = ref(1)
const endPage = ref(currentPage.value)
const isRangeValid = computed(() => startPage.value <= endPage.value)

// 自动同步 endPage
import { watch } from 'vue'
watch(currentPage, (val) => {
  endPage.value = val
})

// 切换课件时自动请求第一页并获取总页数和图片，同时刷新正确率和排名
watch(selectedFile, () => {
  if (selectedFile.value) {
    currentPage.value = 1;
    showPPT(1);
    fetchRateAndRanking();
  }
});
// 翻页时请求对应页图片，同时刷新正确率和排名
watch(currentPage, (val) => {
  endPage.value = val;
  if (selectedFile.value) {
    showPPT(val);
    fetchRateAndRanking();
  }
});
// 上传成功后自动获取文件信息并补充到文件列表
const handleUploadSuccess = async (response, file) => {
  const uid = localStorage.getItem('uid');
  const lidVal = presentation.value.lid;
  if (!response || !response.fid || !uid || !lidVal) return;
  // 1. 添加文件到演讲
  const addForm = new FormData();
  addForm.append('lid', String(lidVal));
  addForm.append('fid', String(response.fid));
  try {
    const addRes = await axios.post('/speaker/add_file', addForm, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
    if (!addRes || addRes.res !== true) {
      window.$message?.error('文件未成功加入演讲');
      return;
    }
  } catch (e) {
    window.$message?.error('文件加入演讲失败');
    return;
  }
  // 2. 获取文件详细信息
  const form = new FormData();
  form.append('fid', String(response.fid));
  form.append('uid', String(uid));
  try {
    const res = await axios.post('/file_info', form, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
    if (res && res.fid) {
      presentation.value.files.push({
        fid: res.fid,
        name: res.file_name || file.name,
        owner: res.owner || '',
        size: (file.size / 1024 / 1024).toFixed(2) + 'MB',
        uploadTime: new Date().toLocaleTimeString()
      });
    }
  } catch (e) {
    window.$message?.error('文件信息获取失败');
  }
}
// 文件下载，表单方式请求 /download，自动下载
const downloadFile = async (file) => {
  const uid = localStorage.getItem('uid');
  if (!file.fid || !uid) {
    window.$message?.error('文件信息缺失，无法下载');
    return;
  }
  const form = new FormData();
  form.append('fid', String(file.fid));
  form.append('uid', String(uid));
  try {
    // 用 fetch 直接下载文件，始终走后端服务
    const baseURL = 'http://localhost:8000';
    const res = await fetch(baseURL + '/download', {
      method: 'POST',
      body: form
    });
    if (!res.ok) {
      window.$message?.error('文件下载失败');
      return;
    }
    const blob = await res.blob();
    // 获取文件名
    let filename = file.name || 'downloaded_file';
    // 创建下载链接
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);
  } catch (e) {
    window.$message?.error('文件下载异常');
  }
}

// 通过POST表单下载图片并显示
async function fetchPPTImage(fid, uid) {
  const form = new FormData();
  form.append('fid', String(fid));
  form.append('uid', String(uid));
  try {
    const baseURL = 'http://localhost:8000';
    const res = await fetch(baseURL + '/download', {
      method: 'POST',
      body: form
    });
    if (!res.ok) return '';
    const blob = await res.blob();
    return URL.createObjectURL(blob);
  } catch {
    return '';
  }
}

// PPT展示接口，支持传入页码
const showPPT = async (page = currentPage.value) => {
  console.log(`请求PPT页码: ${page}, 当前课件: ${selectedFile.value},lid: ${lid.value}`);

  if (!lid.value || !selectedFile.value || !page) {
    if (!selectedFile.value) {
      window.$message?.error('请选择课件文件');
    }
    return;
  }
  const fileObj = presentation.value.files.find(f => f.name === selectedFile.value);
  const fid = fileObj && fileObj.fid ? fileObj.fid : undefined;
  if (!fid) {
    window.$message?.error('课件文件信息异常');
    return;
  }
  const params = new URLSearchParams();
  params.append('lid', String(lid.value));
  params.append('fid', String(fid));
  params.append('page', String(page));
  try {
    const res = await axios.post('/speaker/show_ppt', params, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    });
    if (res && res.res) {
      if (res.page_num) totalPages.value = res.page_num;
      if (res.pic_fid) {
        // 通过POST表单下载图片
        const uid = localStorage.getItem('uid') || '';
        currentSlide.value = await fetchPPTImage(res.pic_fid, uid);
      }
    }
    else{
      if (!res){
        window.$message?.error('PPT展示失败');
      }
      else if (res.msg){
        window.$message?.error(res.msg);
      }
      else{
        window.$message?.error('PPT展示失败');
      }
    }
  } catch (e) {
    window.$message?.error('PPT展示异常');
  }
}

onMounted(async () => {
  const form = new FormData();
  form.append('lid', String(lid.value));
  try {
    const res = await axios.post('/lecture_detail', form, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
    if (res && res.lid) {
      presentation.value.lid = res.lid;
      presentation.value.title = res.name || '';
      presentation.value.speaker = res.speaker || '';
      presentation.value.startTime = res.start_time || '';
      presentation.value.join_num = res.join_num || 0;
      presentation.value.participants = res.join_num || 0;
      // 文件id列表转为文件对象，补充详细信息
      presentation.value.files = [];
      const uid = localStorage.getItem('uid');
      if (Array.isArray(res.fids) && uid) {
        for (const fid of res.fids) {
          const fileForm = new FormData();
          fileForm.append('fid', String(fid));
          fileForm.append('uid', String(uid));
          try {
            const fileRes = await axios.post('/file_info', fileForm, {
              headers: { 'Content-Type': 'multipart/form-data' }
            });
            if (fileRes && fileRes.fid) {
              presentation.value.files.push({
                fid: fileRes.fid,
                name: fileRes.file_name || `文件${fid}`,
                owner: fileRes.owner || '',
                size: fileRes.size || '',
                uploadTime: fileRes.uploadTime || ''
              });
            }
          } catch {}
        }
      }
      // 初始化时刷新正确率和排名
      fetchRateAndRanking();
    }
  } catch (e) {
    window.$message?.error('演讲详情获取失败');
  }
});

// 修复：上传课件的自定义方法，必须包裹为函数 customUpload
const customUpload = async (option) => {
  const uid = localStorage.getItem('uid');
  if (!uid) {
    window.$message?.error('未登录，无法上传');
    option.onError && option.onError();
    return;
  }
  const form = new FormData();
  form.append('file', option.file);
  form.append('uid', uid);
  form.append('type', 'courseware');
  try {
    const res = await axios.post('/upload', form, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
    if (res && res.fid) {
      // 上传成功后自动获取文件信息
      await handleUploadSuccess(res, option.file);
      window.$message?.success('文件上传成功');
      option.onSuccess && option.onSuccess(res);
    } else {
      window.$message?.error('文件上传失败');
      option.onError && option.onError();
    }
  } catch (e) {
    window.$message?.error('文件上传异常');
    option.onError && option.onError(e);
  }
}

// 结束演讲按钮事件
async function endPresentation() {
  const params = new URLSearchParams();
  params.append('lid', String(lid.value));
  try {
    const res = await axios.post('/speaker/end_lecture', params, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    });
    if (res && res.res) {
      window.$message?.success('演讲已结束！');
      // 结束后自动跳转主页
      setTimeout(() => {
        window.$router ? window.$router.push('/') : (typeof $router !== 'undefined' && $router.push('/'));
      }, 600);
    } else {
      window.$message?.error('结束演讲失败');
    }
  } catch (e) {
    window.$message?.error('结束演讲异常');
  }
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
