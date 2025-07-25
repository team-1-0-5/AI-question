<template>
  <div class="create-lecture-page">
    <header class="cl-header">
      <button class="back-btn" @click="goBack">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
          <path d="M19 12H5M5 12L12 5M5 12L12 19"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"/>
        </svg>
      </button>
      <h2 class="page-title">
        <span class="title-gradient">创建新演讲</span>
      </h2>
    </header>
    <form class="cl-form" @submit.prevent="onSubmit">
      <div class="form-group required">
        <label for="lectureName">演讲名称</label>
        <input id="lectureName" v-model="lectureName" type="text" placeholder="请输入演讲名称" required maxlength="50" />
      </div>
      <div class="form-group">
        <label for="lectureDesc">简介</label>
        <textarea id="lectureDesc" v-model="lectureDesc" rows="3" placeholder="可填写演讲简介"></textarea>
      </div>
      <div class="form-group">
        <label>课件上传（可多选）</label>
        <input type="file" multiple @change="onFilesChange" accept=".ppt,.pptx,.pdf,.mp3,.wav,.mp4" />
        <ul v-if="fileList.length" class="file-list">
          <li v-for="(file, idx) in fileList" :key="file.fid || file.name">
            <span>{{ file.name }}</span>
            <span v-if="file.status === 'pending'" style="color:#2196F3;">上传中...</span>
            <span v-else-if="file.status === 'success'" style="color:#4CAF50;">上传成功</span>
            <span v-else style="color:#F44336;">上传失败</span>
            <button type="button" @click="removeFile(idx)">移除</button>
          </li>
        </ul>
      </div>
      <div class="form-group">
        <label for="startTime">开始时间</label>
        <input id="startTime" v-model="startTime" type="datetime-local" />
      </div>
      <div class="form-group">
      <button class="submit-btn" type="submit" :disabled="!lectureName.trim() || submitting">
        {{ submitting ? '提交中...' : '创建演讲' }}
      </button>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import api from '@/utils/api.js';

const lectureName = ref('');
const lectureDesc = ref('');
interface UploadedFile {
  name: string;
  fid?: number;
  status: 'pending' | 'success' | 'fail';
}
const fileList = ref<UploadedFile[]>([]);
const startTime = ref('');
const submitting = ref(false);

async function onFilesChange(e: Event) {
  const files = (e.target as HTMLInputElement).files;
  console.log('文件选择事件触发，files:', files);
  let uid = localStorage.getItem('uid');
  if(!uid){
    uid = '1'; // 如果没有登录，使用默认用户ID
  }
  if (files && uid) {
    for (const file of Array.from(files)) {
      // if (fileList.value.some(f => f.name === file.name)) continue;
      // 先添加到列表，状态为 pending
      const newFile: UploadedFile = { name: file.name, status: 'pending' };
      fileList.value.push(newFile);
      fileList.value = [...fileList.value];
      console.log('已添加到 fileList:', fileList.value);
      const formData = new FormData();
      formData.append('file', file);
      formData.append('uid', uid);
      formData.append('type', 'courseware');
      try {
        const res = await api.post('/upload', formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        }) as { fid?: number };
        if (res && res.fid) {
          const idx = fileList.value.findIndex(f => f.name === file.name && f.status === 'pending');
          if (idx !== -1) {
            fileList.value[idx].fid = res.fid;
            fileList.value[idx].status = 'success';
            fileList.value = [...fileList.value];
            console.log('上传成功，更新 fileList:', fileList.value);
          }
        } else {
          const idx = fileList.value.findIndex(f => f.name === file.name && f.status === 'pending');
          if (idx !== -1) fileList.value[idx].status = 'fail';
          fileList.value = [...fileList.value];
          console.log('上传失败，更新 fileList:', fileList.value);
        }
      } catch {
        const idx = fileList.value.findIndex(f => f.name === file.name && f.status === 'pending');
        if (idx !== -1) fileList.value[idx].status = 'fail';
        fileList.value = [...fileList.value];
        console.log('上传异常，更新 fileList:', fileList.value);
      }
    }
  }
  console.log('最终 fileList:', fileList.value);
}
function removeFile(idx: number) {
  fileList.value.splice(idx, 1);
}
async function onSubmit() {
  if (!lectureName.value.trim()) return;
  submitting.value = true;
  const uid = localStorage.getItem('uid');
  const file_ids = fileList.value.filter(f => f.status === 'success' && f.fid).map(f => f.fid);
  try {
    const params = new URLSearchParams();
    params.append('name', lectureName.value);
    params.append('uid', uid || '');
    params.append('describe', lectureDesc.value);
    if (startTime.value && startTime.value.trim() !== '') {
      params.append('start_time', startTime.value);
    }
    file_ids.forEach(fid => params.append('file_ids', String(fid)));
    const res = await api.post('/speaker/lecture_create', params, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    }) as { lids?: number };
    if (res && res.lids) {
      alert('演讲创建成功！ID: ' + res.lids);
      history.back();
    } else {
      alert('演讲创建失败，请重试');
    }
  } catch (e) {
    alert('创建失败，请检查网络或稍后再试');
  }
  submitting.value = false;
}
function goBack() {
  history.back();
}
</script>

<style scoped>
.create-lecture-page {
  min-height: 100vh;
  background: #f8f9fb;
  display: flex;
  flex-direction: column;
}
.cl-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.2rem 1.5rem 0.5rem 1.2rem;
  background: #fff;
  box-shadow: 0 2px 10px rgba(0,0,0,0.04);
  position: sticky;
  top: 0;
  z-index: 10;
}
.cl-header h2 {
  font-size: 1.15rem;
  font-weight: 600;
  margin: 0;
}
.back-btn {
  background: none;
  border: none;
  padding: 0.2rem;
  cursor: pointer;
  border-radius: 50%;
  transition: background 0.2s;
  display: flex;
  align-items: center;
}
.back-btn:hover {
  background: #f0f0f0;
}
.cl-form {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  padding: 2rem 1.5rem 1.5rem 1.5rem;
  max-width: 720px;
  margin: 0 auto;
  overflow-y: auto;
}
.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
.form-group label {
  font-size: 1rem;
  font-weight: 500;
  color: #333;
}
.form-group.required label:after {
  content: '*';
  color: #f44336;
  margin-left: 4px;
}
input[type="text"],
input[type="datetime-local"],
textarea {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 0.7rem 1rem;
  font-size: 1rem;
  background: #fff;
  transition: border 0.2s;
}
input:focus, textarea:focus {
  outline: none;
  border-color: #4caf50;
}
textarea {
  resize: vertical;
  min-height: 60px;
  max-height: 180px;
}
input[type="file"] {
  margin-top: 0.3rem;
}
.file-list {
  margin: 0.5rem 0 0 0;
  padding: 0;
  list-style: none;
}
.file-list li {
  display: flex;
  align-items: center;
  gap: 0.7rem;
  font-size: 0.97rem;
  color: #555;
  margin-bottom: 0.2rem;
}
.file-list button {
  background: none;
  border: none;
  color: #f44336;
  cursor: pointer;
  font-size: 0.95rem;
  padding: 0.1rem 0.5rem;
  border-radius: 4px;
  transition: background 0.2s;
}
.file-list button:hover {
  background: #ffeaea;
}
.submit-btn {
  margin-top: 1.5rem;
  background: linear-gradient(135deg, #4caf50 0%, #2e7d32 100%);
  color: #fff;
  border: none;
  border-radius: 10px;
  padding: 0.9rem 0;
  font-size: 1.08rem;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(76,175,80,0.13);
  transition: all 0.2s;
}
.submit-btn:disabled {
  background: #bdbdbd;
  cursor: not-allowed;
  box-shadow: none;
}
@media (max-width: 600px) {
  .cl-form { padding: 1.2rem 0.7rem 1.2rem 0.7rem; }
  .cl-header { padding: 1rem 0.7rem 0.5rem 0.7rem; }
}
/* 新增CSS变量 */
:root {
  --primary-color: #2196F3;
  --primary-dark: #1976D2;
  --success-color: #4CAF50;
}

.create-lecture-page {
  background: linear-gradient(160deg, #f5f7fa 0%, #e4e8eb 100%);
}

.cl-header {
  padding: 1.5rem 2rem;
  background: linear-gradient(135deg, #ffffff 0%, #f8f9fd 100%);
  border-bottom: 1px solid rgba(0,0,0,0.08);
}

.cl-header h2 {
  font-size: 1.4rem; /* 增大字号 */
  font-weight: 700; /* 加粗 */
  color: #2c3e50; /* 深色文字 */
  letter-spacing: 0.5px;
  text-shadow: 0 1px 2px rgba(0,0,0,0.05); /* 文字阴影 */
}

/* 输入框美化 */
input[type="text"],
input[type="datetime-local"],
textarea {
  border: 2px solid #e0e4e8; /* 加粗边框 */
  border-radius: 10px;
  padding: 0.85rem 1.2rem;
  font-size: 1rem;
  background: #ffffff;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 4px rgba(0,0,0,0.03);
}

input:focus, textarea:focus {
  border-color: var(--primary-color);
  box-shadow: 0 4px 12px rgba(33,150,243,0.15);
}

/* 按钮动效优化 */


.submit-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(33,150,243,0.35);
}

/* 文件列表美化 */
.file-list li {
  background: #ffffff;
  padding: 0.8rem 1.2rem;
  border-radius: 8px;
  margin-bottom: 0.5rem;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  display: flex;
  align-items: center;
  gap: 1rem;
}

/* 新增图标美化 */
.file-list li::before {
  content: "📎";
  font-size: 1.1em;
}

/* 必填项标识优化 */
.form-group.required label:after {
  content: "•";
  color: var(--success-color);
  margin-left: 6px;
  font-size: 1.2em;
}

/* 响应式优化 */
@media (max-width: 600px) {
  .cl-header h2 {
    font-size: 1.25rem;
  }
  .cl-form {
    padding: 1.5rem;
  }
}
:root {
  --primary-gradient: linear-gradient(135deg, #2777FF 0%, #00C7C7 100%);
  --secondary-color: #FF7E5F;
  --text-primary: #2D3436;
  --text-secondary: #636E72;
  --border-radius: 12px;
  --shadow-sm: 0 4px 12px rgba(0,0,0,0.08);
  --shadow-lg: 0 8px 32px rgba(0,0,0,0.1);
}

.create-lecture-page {
  background: linear-gradient(135deg, #F8F9FD 0%, #EFF1FA 100%);
}

.cl-header {
  background: rgba(255,255,255,0.95);
  backdrop-filter: blur(8px);
  border-bottom: 1px solid rgba(255,255,255,0.2);
  padding: 1.5rem 2rem;
}

.page-title {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 700;
  position: relative;
}

.title-gradient {
  background: var(--primary-gradient);
  -webkit-background-clip: text;
  background-clip: text;
  text-shadow: 0 2px 4px rgba(39,119,255,0.1);
  position: relative;
  padding-left: 1.2rem;
}

.title-gradient::before {
  content: "";
  position: absolute;
  left: 0;
  top: 50%;
  width: 6px;
  height: 80%;
  background: var(--primary-gradient);
  border-radius: 3px;
}

/* 优化表单元素 */
input[type="text"],
input[type="datetime-local"],
textarea {
  border: 2px solid #EBECF0;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

input:focus, textarea:focus {
  border-color: #2777FF;
  box-shadow: 0 0 0 3px rgba(39,119,255,0.1);
}


/* 新增文件列表样式 */
.file-list li {
  background: rgba(255,255,255,0.8);
  padding: 0.8rem 1.2rem;
  border-radius: var(--border-radius);
  border: 1px solid rgba(0,0,0,0.05);
  transition: transform 0.2s ease;
}

.file-list li:hover {
  transform: translateX(4px);
  background: white;
}

/* 响应式优化 */
@media (max-width: 480px) {
  .page-title {
    font-size: 1.3rem;
  }

  .cl-header {
    padding: 1rem;
  }
}
</style>
