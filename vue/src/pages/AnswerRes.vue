<template>
  <div class="result-container">
    <!-- 总体统计卡片 -->
    <div class="stats-card">
      <div class="stat-item">
        <div class="stat-value">{{ overallAccuracy }}%</div>
        <div class="stat-label">总体正确率</div>
      </div>
      <div class="divider"></div>
      <div class="stat-item">
        <div class="stat-value">{{ correctCount }}/{{ totalQuestions }}</div>
        <div class="stat-label">答对题数</div>
      </div>
    </div>

    <!-- 题目详情列表 -->
    <div v-if="!loading && !error" class="question-list">
      <div
        v-for="(question, index) in questions"
        :key="index"
        class="question-item"
        :class="{ 'correct': isCorrect(index), 'incorrect': isIncorrect(index) }"
      >
        <div class="question-header">
          <span class="question-index">第{{ index + 1 }}题</span>
          <span class="result-badge">
            {{ getResultText(index) }}
          </span>
        </div>
        <div class="question-content">{{ question.question }}</div>
        <div class="answer-comparison">
          <div class="answer-item">
            <span class="label">你的答案：</span>
            <span class="user-answer">
              {{ getAnswerText(index) || '未作答' }}
            </span>
          </div>
          <div class="answer-item">
            <span class="label">正确答案：</span>
            <span class="correct-answer">
              {{ getOptionText(question, trueAnswers[index]) }}
            </span>
          </div>
        </div>
        <div class="answer-reason" v-if="getReason(index)">
          <span class="label">解析：</span>
          <span class="reason-text">{{ getReason(index) }}</span>
        </div>
      </div>
    </div>
    <div v-if="loading" style="text-align:center;padding:2rem;">加载中...</div>
    <div v-if="error" style="color:red;text-align:center;padding:2rem;">{{ error }}</div>

    <!-- 操作按钮 -->
    <div class="action-buttons">
      <button class="btn back-btn" @click="goBackLecture">
        返回听演讲页面
      </button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      questions: [], // 接口返回的题目列表
      userAnswers: [], // 用户答案
      trueAnswers: [], // 正确答案
      reasons: [],     // 解析
      loading: true,
      error: '',
    }
  },
  computed: {
    totalQuestions() {
      return this.questions.length
    },
    correctCount() {
      return this.questions.reduce((count, _, index) => {
        return this.isCorrect(index) ? count + 1 : count
      }, 0)
    },
    overallAccuracy() {
      return this.totalQuestions
        ? Math.round((this.correctCount / this.totalQuestions) * 100)
        : 0
    }
  },
  methods: {
    isCorrect(index) {
      return this.userAnswers[index] === this.trueAnswers[index];
    },
    isIncorrect(index) {
      return this.userAnswers[index] !== undefined && !this.isCorrect(index);
    },
    getResultText(index) {
      if (this.userAnswers[index] === undefined) return '未作答';
      return this.isCorrect(index) ? '正确' : '错误';
    },
    getAnswerText(index) {
      const answer = this.userAnswers[index];
      if (answer === undefined) return '';
      return this.getOptionText(this.questions[index], answer);
    },
    getOptionText(question, idx) {
      if (!question || !question.choices) return '';
      return question.choices[idx] || '无效选项';
    },
    getReason(index) {
      return this.reasons[index] || '';
    },
    goBackLecture() {
      // 跳转回听演讲页面，带上lid参数
      const lid = this.$route.query.lid;
      this.$router.push({
        path: '/lecture-play',
        query: { lid }
      });
    },
  },
  async mounted() {
    // 自动调用接口获取数据
    this.loading = true;
    this.error = '';
    try {
      const uid = localStorage.getItem('uid') || '';
      const lid = this.$route.query.lid;
      const times = this.$route.query.times || 1;
      if (!uid || !lid) {
        this.error = '缺少必要参数';
        this.loading = false;
        return;
      }
      const params = new URLSearchParams();
      params.append('uid', uid);
      params.append('lid', lid);
      params.append('times', times);
      const api = (await import('@/utils/api.js')).default;
      const res = await api.post('/answer_res', params, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
      });
      if (res && Array.isArray(res.questions)) {
        this.questions = res.questions;
        this.userAnswers = res.user_answers || [];
        this.trueAnswers = res.true_answers || [];
        this.reasons = res.reason || [];
      } else {
        this.error = '接口返回数据异常';
      }
    } catch (e) {
      this.error = '获取作答结果失败';
    }
    this.loading = false;
  },
}
</script>

<style scoped>
/* 基础配色 */
:root {
  --primary-green: #2ecc71;
  --secondary-gray: #f5f6fa;
  --text-dark: #2d3436;
  --text-gray: #636e72;
  --border-color: #dfe6e9;
}

.result-container {
  max-width: 800px;
  width: 100%;
  margin: 0 auto;
  padding: 2rem;
  font-family: 'Segoe UI', system-ui, sans-serif;
  justify-content: center;
  align-items: center;
}

/* 统计卡片 */
.stats-card {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-around;
  align-items: center;
  margin-bottom: 2rem;
}

.stat-item {
  text-align: center;
  min-width: 120px;
}

.stat-value {
  font-size: 2.5rem;
  font-weight: 700;
  color: #2ecc71;
  line-height: 1.2;
}

.stat-label {
  color: #636e72;
  font-size: 0.9rem;
}

.divider {
  width: 1px;
  height: 60px;
  background: var(--border-color);
}

/* 题目列表 */
.question-list {
  display: grid;
  gap: 1rem;
  margin-bottom: 2rem;
}

.question-item {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  transition: transform 0.2s ease;
}

.question-item:hover {
  transform: translateY(-2px);
}

.question-item.correct {
  border-left: 4px solid #2ecc71;
}

.question-item.incorrect {
  border-left: 4px solid #e74c3c;
}

.question-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.question-index {
  font-weight: 600;
  color: #2d3436;
}

.result-badge {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 500;
}

.correct .result-badge {
  background: #e8f5e9;
  color: #2e7d32;
}

.incorrect .result-badge {
  background: #ffebee;
  color: #c62828;
}

.question-content {
  color: #2d3436;
  margin-bottom: 1.5rem;
  line-height: 1.6;
}

.answer-comparison {
  background: #f5f6fa;
  border-radius: 8px;
  padding: 1rem;
}

.answer-item {
  display: flex;
  margin: 0.5rem 0;
}

.answer-item .label {
  min-width: 80px;
  color: #636e72;
}

.user-answer {
  color: #2d3436;
  font-weight: 500;
}

.correct-answer {
  color: #2ecc71;
  font-weight: 600;
}

/* 操作按钮 */
.action-buttons {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
}

.btn {
  padding: 0.8rem 2rem;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.back-btn {
  background: #f5f6fa;
  color: #2d3436;
}

.back-btn:hover {
  background: #ecf0f1;
}

.review-btn {
  background: #2ecc71;
  color: white;
}

.review-btn:hover {
  background: #27ae60;
}

/* 响应式设计 */
@media (max-width: 640px) {
  .stats-card {
    flex-direction: column;
    gap: 1rem;
  }

  .divider {
    width: 60px;
    height: 1px;
  }

  .action-buttons {
    flex-direction: column;
  }

  .btn {
    width: 100%;
  }
}

</style>
