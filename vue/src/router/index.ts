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
  const uid = localStorage.getItem('uid');
  const type = localStorage.getItem('type');
  // 访问登录/注册页，已登录则自动跳转主页
  if ((to.path === '/login' || to.path === '/register') && uid && type) {
    if (type === '演讲者') {
      next('/speaker-home');
    } else if (type === '听众') {
      next('/audience-home');
    } else {
      next();
    }
    return;
  }
  // 访问根路径，根据登录状态和类型跳转
  if (to.path === '/') {
    if (!uid || !type) {
      next('/login');
    } else if (type === '演讲者') {
      next('/speaker-home');
    } else if (type === '听众') {
      next('/audience-home');
    } else {
      next('/login');
    }
    return;
  }
  next();
});

export default router;
