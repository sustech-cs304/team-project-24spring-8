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
            component: HomePage
        },
        {
            path: '/reminders',
            name: 'ActivityReminders',
            component: ActivityReminders
        },
        {
            path: '/user-profile',
            name: 'UserProfile',
            component: UserProfile
        },
        {
            path: '/recommendations',
            name: 'RecommendationsList',
            component: RecommendationsList
        },
        {
            path: '/eventspage',
            name: 'EventsPage',
            component: EventsPage
        },
        {
            path: '/eventbooking',
            name: 'EventBooking',
            component: EventBooking
        },
        {
            path: '/posts',
            name: 'PostList',
            component: PostList
        },
        {
            path: '/posts/:postId',
            name: 'PostDetails',
            component: PostDetails,
            props: true
        }
    ]
});

export default router;
