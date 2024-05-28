import { createRouter, createWebHistory } from 'vue-router';
import ActivityReminders from '../components/ActivityReminders.vue';
import UserProfile from '../components/UserProfile.vue';
import RecommendationsList from '../components/RecommendationsList.vue';
import PostList from '../components/PostList.vue';
import PostDetails from '../components/PostDetails.vue';
import EventsPage from '../components/EventsPage.vue';
import EventBooking from '../components/EventBooking.vue';
import LoginPage from '../components/LoginPage.vue';
import HomePage from '../components/HomePage.vue';
import UserDetail from '../components/UserDetail.vue';
import NotificationsPage from '../components/NotificationsPage.vue';  // 确保引入通知页面组件

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
            meta: { requiresAuth: true }
        },
        {
            path: '/reminders',
            name: 'ActivityReminders',
            component: ActivityReminders,
            meta: { requiresAuth: true }
        },
        {
            path: '/user-profile',
            name: 'UserProfile',
            component: UserProfile,
            meta: { requiresAuth: true }
        },
        {
            path: '/recommendations',
            name: 'RecommendationsList',
            component: RecommendationsList,
            meta: { requiresAuth: true }
        },
        {
            path: '/eventspage',
            name: 'EventsPage',
            component: EventsPage,
            meta: { requiresAuth: true }
        },
        {
            path: '/eventbooking',
            name: 'EventBooking',
            component: EventBooking,
            meta: { requiresAuth: true }
        },
        {
            path: '/posts',
            name: 'PostList',
            component: PostList,
            meta: { requiresAuth: true }
        },
        {
            path: '/posts/:postId',
            name: 'PostDetails',
            component: PostDetails,
            props: true,
            meta: { requiresAuth: true }
        },
        {
            path: '/discussions',
            name: 'Discussions',
            component: PostList,
            meta: { requiresAuth: true }
        },
        {
            path: '/events',
            name: 'Events',
            component: EventsPage,
            meta: { requiresAuth: true }
        },
        {
            path: '/user-detail',
            name: 'UserDetail',
            component: UserDetail
        },
        {
            path: '/notifications',
            name: 'Notifications',
            component: NotificationsPage  // 添加通知页面路由
        }
    ]
});

// 添加全局前置守卫
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
