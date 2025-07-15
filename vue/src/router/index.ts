import { createRouter, createWebHistory } from 'vue-router';
import SpeakerHome from '@/pages/SpeakerHome.vue';
import CreateLecture from '@/pages/CreateLecture.vue';
import AnswerQuiz from '@/pages/AnswerQuiz.vue';
import AnswerRes from '@/pages/AnswerRes.vue';

const routes = [
  {
    path: '/',
    name: 'SpeakerHome',
    component: SpeakerHome
  },
  {
    path: '/create-lecture',
    name: 'CreateLecture',
    component: CreateLecture
  },
  {
    path: '/answer-quiz',
    name: 'AnswerQuiz',
    component: AnswerQuiz
  },
  {
    path: '/answer-res',
    name: 'AnswerRes',
    component: AnswerRes
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
