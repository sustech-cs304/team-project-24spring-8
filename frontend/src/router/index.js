import { createRouter, createWebHistory } from 'vue-router';
import ActivityReminders from '../components/ActivityReminders.vue';
import UserProfile from '../components/UserProfile.vue';
import RecommendationsList from '../components/RecommendationsList.vue';
import PostList from '../components/PostList.vue';
import PostDetails from '../components/PostDetails.vue';
import EventsPage from '../components/EventsPage.vue';
import EventBooking from '../components/EventBooking.vue';
import LoginPage from '../components/LoginPage.vue';  // 导入重命名后的登录组件
import HomePage from '../components/HomePage.vue';    // 导入重命名后的主界面组件
import UserDetail from '../components/UserDetail.vue';


const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            name: 'LoginPage',
            component: LoginPage
        },
        {
            path: '/home',
            name: 'HomePage',
            component: HomePage,
            meta: { requiresAuth: true } // 标记需要认证
        },
        {
            path: '/reminders',
            name: 'ActivityReminders',
            component: ActivityReminders,
            meta: { requiresAuth: true } // 标记需要认证
        },
        {
            path: '/user-profile',
            name: 'UserProfile',
            component: UserProfile,
            meta: { requiresAuth: true } // 标记需要认证
        },
        {
            path: '/recommendations',
            name: 'RecommendationsList',
            component: RecommendationsList,
            meta: { requiresAuth: true } // 标记需要认证
        },
        {
            path: '/eventspage',
            name: 'EventsPage',
            component: EventsPage,
            meta: { requiresAuth: true } // 标记需要认证
        },
        {
            path: '/eventbooking',
            name: 'EventBooking',
            component: EventBooking,
            meta: { requiresAuth: true } // 标记需要认证
        },
        {
            path: '/posts',
            name: 'PostList',
            component: PostList,
            meta: { requiresAuth: true } // 标记需要认证
        },
        {
            path: '/posts/:postId',
            name: 'PostDetails',
            component: PostDetails,
            props: true,
            meta: { requiresAuth: true } // 标记需要认证
        },
        {
            path: '/discussions',
            name: 'Discussions',
            component: PostList,
            meta: { requiresAuth: true } // 标记需要认证
        },
        {
            path: '/events',
            name: 'Events',
            component: () => import('../components/EventsPage.vue'),
            meta: { requiresAuth: true } // 标记需要认证
        },
        {
            path: '/reminders',
            name: 'ActivityReminders',
            component: ActivityReminders
        },
        {
            path: '/user-detail',
            name: 'UserDetail',
            component: UserDetail
        }
    ]
});

// 添加全局前置守卫
// src/router/index.js
// 导航守卫
router.beforeEach((to, from, next) => {
    const publicPages = ['/'];
    const authRequired = !publicPages.includes(to.path);
    const loggedIn = localStorage.getItem('access_token');
  
    if (authRequired && !loggedIn) {
      return next('/');
    }
  
    next();
  });
  

export default router;
