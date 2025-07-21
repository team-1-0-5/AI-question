<template>
  <div>
      <el-button type="text" @click="$router.push('/')" icon="ArrowLeft" style="font-size:1.08rem;color:#1565c0;">
        返回首页
      </el-button>
  </div>
  <div class="container">

    <el-card class="data-card">
      <h3 class="section-title">总体正确率</h3>
      <el-progress type="circle" :percentage="correctRate" :color="progressColor" />
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
</template>

<script setup>
import { ref, computed } from 'vue'
const correctRate = ref(80)
const progressColor = computed(() => correctRate.value > 80 ? '#67C23A' : '#E6A23C')
const rankingData = ref([
  { rank: 1, name: "张三", accuracy: 90 },
  { rank: 2, name: "李四", accuracy: 80 },
  { rank: 3, name: "王五", accuracy: 70 }
])
</script>

<style scoped>
.container { max-width: 900px; margin: 40px auto; background: #fff; border-radius: 8px; box-shadow: 0 2px 12px rgba(0,0,0,0.08); padding: 32px; display: grid; grid-template-columns: 1fr 1fr; gap: 32px; }
.data-card { background: #fff; border-radius: 12px; box-shadow: 0 2px 8px rgba(44, 62, 80, 0.08); padding: 18px 16px; display: flex; flex-direction: column; align-items: center; justify-content: flex-start; min-height: 320px; }
.section-title { color: #1565c0; font-size: 1.08rem; font-weight: 600; margin-bottom: 8px; }
.table-rank { color: #2e7d32; font-weight: 700; }
.table-name { color: #1565c0; font-weight: 500; }
.table-accuracy { color: #E6A23C; font-weight: 700; }
.ranking-table { margin-top: 20px; }
</style>
