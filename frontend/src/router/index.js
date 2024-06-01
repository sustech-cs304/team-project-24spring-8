import { createRouter, createWebHistory } from 'vue-router';
import ActivityReminders from '../components/ActivityReminders.vue';
import UserProfile from '../components/UserProfile.vue';
import RecommendationsList from '../components/RecommendationsList.vue';
import PostList from '../components/PostList.vue';
import PostDetails from '../components/PostDetails.vue';
import EventsPage from '../components/EventsPage.vue';
import EventBooking from '../components/EventBooking.vue';
import LoginPage from '../components/LoginPage.vue';
import RegisterPage from '../components/RegisterPage.vue';
import HomePage from '../components/HomePage.vue';
import UserDetail from '../components/UserDetail.vue';
import NotificationsPage from '../components/NotificationsPage.vue';
import MyTicketsPage from '@/components/MyTicketsPage.vue';
import AddNotification from '../components/AddNotification.vue';

const routes = [
  {
    path: '/',
    name: 'LoginPage',
    component: LoginPage,
  },
  {
    path: '/home',
    name: 'HomePage',
    component: HomePage,
    meta: { requiresAuth: true },
  },
  {
    path: '/register',
    name: 'RegisterPage',
    component: RegisterPage,
    meta: { requiresAuth: false },
  },
  {
    path: '/reminders',
    name: 'ActivityReminders',
    component: ActivityReminders,
    meta: { requiresAuth: true },
  },
  {
    path: '/user-profile',
    name: 'UserProfile',
    component: UserProfile,
    meta: { requiresAuth: true },
  },
  {
    path: '/recommendations',
    name: 'RecommendationsList',
    component: RecommendationsList,
    meta: { requiresAuth: true },
  },
  {
    path: '/eventspage',
    name: 'EventsPage',
    component: EventsPage,
    meta: { requiresAuth: true },
  },
  {
    path: '/eventbooking',
    name: 'EventBooking',
    component: EventBooking,
    meta: { requiresAuth: true },
  },
  {
    path: '/posts',
    name: 'PostList',
    component: PostList,
    meta: { requiresAuth: true },
  },
  {
    path: '/posts/:postId',
    name: 'PostDetails',
    component: PostDetails,
    props: true,
    meta: { requiresAuth: true },
  },
  {
    path: '/discussions',
    name: 'Discussions',
    component: PostList,
    meta: { requiresAuth: true },
  },
  {
    path: '/events',
    name: 'Events',
    component: EventsPage,
    meta: { requiresAuth: true },
  },
  {
    path: '/user-detail',
    name: 'UserDetail',
    component: UserDetail,
    meta: { requiresAuth: true },
  },
  {
    path: '/notifications',
    name: 'Notifications',
    component: NotificationsPage,
    meta: { requiresAuth: true },
  },
  {
    path: '/add-notification',
    name: 'AddNotification',
    component: AddNotification,
    meta: { requiresAuth: true },
  },
  {
    path: '/event-booking/:eventID',
    name: 'EventBookingDetails',
    component: () => import('@/components/EventBooking.vue'),
    props: true,
    meta: { requiresAuth: true },
  },
  {
    path: '/my-tickets',
    name: 'MyTicketsPage',
    component: MyTicketsPage,
    meta: { requiresAuth: true },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  // const publicPages = ['/'];
  const authRequired = to.matched.some(record => record.meta.requiresAuth);
  const loggedIn = localStorage.getItem('access_token');

  if (authRequired && !loggedIn) {
    return next('/');
  }

  next();
});

export default router;
