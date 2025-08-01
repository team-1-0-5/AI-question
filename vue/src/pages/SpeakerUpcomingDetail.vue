<template>
  <div class="container">
    <div>
      <el-button type="text" @click="$router.push('/')" icon="ArrowLeft" style="font-size:1.08rem;color:#1565c0;">
        返回首页
      </el-button>
    </div>
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
        <div style="margin-top: 28px; text-align: right;">
          <el-button type="success" @click="startPresentation">开始演讲</el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from '@/utils/api.js'
const router = useRouter()
const route = useRoute()
const presentation = ref({
  title: "即将开始的演讲",
  participants: 0,
  startTime: "",
  description: "",
  speaker: "",
  join_num: 0,
  fids: []
})

onMounted(async () => {
  const lid = Number(route.query.lid) || Number(route.params.lid)
  if (!lid) return
  const form = new FormData()
  form.append('lid', String(lid))
  try {
    const res = await axios.post('/lecture_detail', form, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    if (res && res.lid) {
      presentation.value.title = res.name || ''
      presentation.value.speaker = res.speaker || ''
      presentation.value.startTime = res.start_time || ''
      presentation.value.join_num = res.join_num || 0
      presentation.value.participants = res.join_num || 0
      presentation.value.fids = res.fids || []
      // 可选：补充描述
      presentation.value.description = `演讲者：${res.speaker || ''}`
    }
  } catch {}
})
async function startPresentation() {
  // 获取 lid（优先 query.lid，其次 params.lid）
  const lid = Number(route.query.lid) || Number(route.params.lid)
  if (!lid) {
    window.$message?.error('未获取到演讲ID')
    return
  }
  const params = new URLSearchParams()
  params.append('lid', String(lid))
  try {
    const res = await axios.post('/speaker/start_lecture', params, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    })
    if (res && res.res) {
      window.$message?.success('演讲已开始！')
      router.push({ path: '/speaker-main-lct', query: { lid } })
    } else {
      window.$message?.error('开始演讲失败')
    }
  } catch (e) {
    window.$message?.error('开始演讲异常')
  }
}
</script>

<style scoped>
.container { max-width: 600px; margin: 40px auto; background: #fff; border-radius: 8px; box-shadow: 0 2px 12px rgba(0,0,0,0.08); padding: 32px; }
.info-header { display: flex; align-items: center; gap: 18px; margin-bottom: 10px; }
.speaker-avatar { width: 60px; height: 60px; border-radius: 50%; object-fit: cover; box-shadow: 0 2px 8px rgba(44, 62, 80, 0.12); }
.main-title { color: #2e7d32; font-size: 1.25rem; font-weight: 700; margin-bottom: 2px; }
.stats { display: flex; gap: 40px; margin: 20px 0; }
.main-desc { color: #333; font-size: 1.02rem; margin-top: 8px; }
</style>
