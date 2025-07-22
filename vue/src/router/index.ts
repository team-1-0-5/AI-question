import { createRouter, createWebHistory } from 'vue-router';
import SpeakerHome from '@/pages/SpeakerHome.vue';
import CreateLecture from '@/pages/CreateLecture.vue';
import AnswerQuiz from '@/pages/AnswerQuiz.vue';
import AnswerRes from '@/pages/AnswerRes.vue';
import Speaker_MainLct from '@/pages/Speaker_MainLct.vue';
import AudienceHome from '@/pages/AudienceHome.vue';
import LectureDetail from '@/pages/LectureDetail.vue';

const routes = [
  {
    path: '/speaker-home',
    name: 'SpeakerHome1',
    component: SpeakerHome
  },
  {
    path: '/speaker-upcoming-detail',
    name: 'SpeakerUpcomingDetail',
    component: () => import('@/pages/SpeakerUpcomingDetail.vue')
  },
  {
    path: '/speaker-ended-detail',
    name: 'SpeakerEndedDetail',
    component: () => import('@/pages/SpeakerEndedDetail.vue')
  },
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
  },
  {
    path: '/speaker-main-lct',
    name: 'Speaker_MainLct',
    component: Speaker_MainLct
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/pages/Login.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/pages/Register.vue')
  },
  {
    path: '/audience-home',
    name: 'AudienceHome',
    component: AudienceHome
  },
  {
    path: '/lecture-detail',
    name: 'LectureDetail',
    component: LectureDetail
  },
  {
    path: '/audience-lecture-play',
    name: 'Audience_LecturePlay',
    component: () => import('@/pages/Audience_LecturePlay.vue')
  },
  {
    path: '/audience-history',
    name: 'AudienceHistory',
    component: () => import('@/pages/AudienceHistory.vue')
  },
  {
    path: '/audience-profile',
    name: 'AudienceProfile',
    component: () => import('@/pages/AudienceProfile.vue')
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

// 全局前置守卫：访问/时自动检测登录状态
router.beforeEach((to, from, next) => {
  if (to.path === '/') {
    const uid = localStorage.getItem('uid');
    const type = localStorage.getItem('type');
    if (!uid || !type) {
      next('/login');
    } else {
      if (type === '演讲者') {
        next({ path: '/' }); // 保持在演讲者主页
      } else if (type === '听众') {
        next({ path: '/audience-home' });
      } else {
        next('/login');
      }
    }
  } else {
    next();
  }
});

export default router;
