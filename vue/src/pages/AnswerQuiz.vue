<template>
  <div class="quiz-container">
    <!-- 进度指示器 -->
    <div class="progress-indicator">
      <div
        v-for="(_, index) in questions"
        :key="index"
        class="progress-dot"
        :class="{
          active: index === currentQuestionIndex,
          answered: answered[index]
        }"
        @click="jumpToQuestion(index)"
      >
        {{ index + 1 }}
      </div>
    </div>

    <!-- 题目内容 -->
    <div class="question-card">
      <div class="question-header">
        <h2 class="question-text">{{ currentQuestion.text }}</h2>
        <div class="question-count">
          {{ currentQuestionIndex + 1 }} / {{ questions.length }}
        </div>
      </div>

      <!-- 选项列表 -->
      <div class="options-container">
        <div
          v-for="(option, index) in currentQuestion.options"
          :key="index"
          class="option-card"
          :class="{ selected: selectedOption === index }"
          @click="selectOption(index)"
        >
          <div class="option-index">{{ String.fromCharCode(65 + index) }}</div>
          <div class="option-text">{{ option }}</div>
        </div>
      </div>

      <!-- 导航按钮 -->
      <div class="navigation-buttons">
        <button
          class="nav-button prev"
          :disabled="currentQuestionIndex === 0"
          @click="prevQuestion"
        >
          上一题
        </button>
        <button
          class="nav-button next"
          :disabled="currentQuestionIndex === questions.length - 1"
          @click="nextQuestion"
        >
          下一题
        </button>
      </div>

      <!-- 提交按钮 -->
      <button
        class="submit-button"
        :disabled="!isAllAnswered"
        @click="submitAnswers"
      >
        提交答案
      </button>
    </div>
  </div>
</template>

<script>
import { useRoute } from 'vue-router';
import api from '../utils/api';
export default {
  data() {
    return {
      currentQuestionIndex: 0,
      selectedOption: null,
      answers: {},
      answered: [],
      questions: []
    };
  },
  computed: {
    currentQuestion() {
      return this.questions[this.currentQuestionIndex] || {};
    },
    isAllAnswered() {
      return Object.keys(this.answers).length === this.questions.length;
    }
  },
  created() {
    // 自动解析路由参数
    let questions = [];
    try {
      const route = this.$route;
      if (route.query.questions) {
        questions = JSON.parse(decodeURIComponent(route.query.questions));
        // 兼容后端字段
        this.questions = questions.map(q => ({
          id: q.qid,
          text: q.question,
          options: q.choices
        }));
      }
    } catch (e) {
      this.questions = [];
    }
    this.answered = new Array(this.questions.length).fill(false);
  },
  methods: {
    selectOption(index) {
      this.selectedOption = index;
      this.answered[this.currentQuestionIndex] = true;
      this.answers[this.currentQuestionIndex] = index;
    },
    prevQuestion() {
      if (this.currentQuestionIndex > 0) {
        this.currentQuestionIndex--;
        this.selectedOption = this.answers[this.currentQuestionIndex] !== undefined ? this.answers[this.currentQuestionIndex] : null;
      }
    },
    nextQuestion() {
      if (this.currentQuestionIndex < this.questions.length - 1) {
        this.currentQuestionIndex++;
        this.selectedOption = this.answers[this.currentQuestionIndex] !== undefined ? this.answers[this.currentQuestionIndex] : null;
      }
    },
    async submitAnswers() {
      if (!this.isAllAnswered) return;
      const uid = localStorage.getItem('uid') || '';
      const qids = this.questions.map(q => q.id);
      const answers = qids.map((_, idx) => this.answers[idx]);
      try {
        // 构造表单数据
        const form = new URLSearchParams();
        form.append('uid', uid);
        qids.forEach(qid => form.append('qids', qid));
        answers.forEach(ans => form.append('answers', ans));
        // 表单方式提交
        const res = await api.post('/listener/post_answer', form, {
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
        });
        console.log('提交结果:', res);
        if (res && res.score !== undefined && !isNaN(Number(res.score))) {
          if (window.confirm(`答案提交成功！得分：${res.score}\n\n点击“确定”查看解析，点击“取消”返回听演讲`)) {
            this.$router.push({
              path: '/answer-res',
              query: {
                lid: this.$route.query.lid,
                times: this.$route.query.times || 1,
              }
            });
          } else {
            this.$router.push({
              path: '/audience-lecture-play',
              query: { lid: this.$route.query.lid }
            });
          }
        } else {
          alert('提交成功，但未返回得分');
        }
      } catch (e) {
        alert('提交失败，请重试');
      }
    },
    jumpToQuestion(index) {
      if (index >= 0 && index < this.questions.length) {
        this.currentQuestionIndex = index;
        this.selectedOption = this.answers[this.currentQuestionIndex] !== undefined ? this.answers[this.currentQuestionIndex] : null;
      }
    }
  }
};
</script>

<style scoped>
/* 基础样式 */
.quiz-container {
  max-width: 800px;
  width: 100%;
  margin: 0 auto;
  padding: 2rem;
  font-family: 'Segoe UI', system-ui, sans-serif;
}

/* 进度指示器 */
.progress-dots {
  display: flex;
  justify-content: center;
  gap: 8px;
  margin-bottom: 2rem;
}

.dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background-color: #e0e0e0;
  transition: all 0.3s ease;
}

.dot.active {
  background-color: #00c853;
  transform: scale(1.2);
}

/* 题目卡片 */
.question-card {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.question-header {
  margin-bottom: 2rem;
}
.option-text{
  color: #2d3436;
  font-size: 1rem;
}
.question-text {
  color: #2d3436;
  font-size: 1.5rem;
  margin-bottom: 1rem;
}

.question-count {
  color: #636e72;
  font-size: 0.9rem;
}

/* 选项样式 */
.options-container {
  display: grid;
  gap: 1rem;
  margin-bottom: 2rem;
}

.option-card {
  display: flex;
  align-items: center;
  padding: 1.2rem;
  border: 2px solid #e0e0e0;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.option-card:hover {
  border-color: #00c853;
}

.option-card.selected {
  border-color: #00c853;
  background-color: #f0fff4;
}

.option-index {
  width: 32px;
  height: 32px;
  background-color: #00c853;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 1rem;
  font-weight: bold;
}

/* 导航按钮 */
.navigation-buttons {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1.5rem;
}

.nav-button {
  padding: 0.8rem 2rem;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.nav-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.prev {
  background-color: #f5f5f5;
  color: #636e72;
}

.next {
  background-color: #00c853;
  color: white;
}

/* 提交按钮 */
.submit-button {
  width: 100%;
  padding: 1rem;
  background-color: #00c853;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.submit-button:disabled {
  background-color: #a5d6a7;
  cursor: not-allowed;
}

/* 响应式设计 */
@media (max-width: 480px) {
  .quiz-container {
    padding: 1rem;
  }

  .question-card {
    padding: 1.5rem;
  }

  .question-text {
    font-size: 1.2rem;
  }

  .option-card {
    padding: 1rem;
  }

  .nav-button {
    padding: 0.6rem 1.5rem;
  }
}
.progress-indicator {
  display: flex;
  justify-content: center;
  gap: 12px;
  margin: 20px 0;
  flex-wrap: wrap;
}

.progress-dot {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #e0e0e0;
  color: #666;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
}

/* 当前题目样式 */
.progress-dot.active {
  background: #2196F3;
  color: white;
  transform: scale(1.2);
  box-shadow: 0 2px 8px rgba(33,150,243,0.3);
}

/* 已答题样式 */
.progress-dot.answered {
  background: #4CAF50;
  color: white;
}

/* 当前题目已答题的特殊样式 */
.progress-dot.current-answered::after {
  content: '';
  position: absolute;
  width: 6px;
  height: 6px;
  background: white;
  border-radius: 50%;
  bottom: 4px;
}

/* 悬停效果 */
.progress-dot:hover:not(.active) {
  background: #bbdefb;
  transform: scale(1.1);
}
</style>
