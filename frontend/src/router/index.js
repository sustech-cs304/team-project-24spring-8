import { createRouter, createWebHistory } from 'vue-router';
import ActivityReminders from '../components/ActivityReminders.vue';
import UserProfile from '../components/UserProfile.vue';
import RecommendationsList from '../components/RecommendationsList.vue';
import PostList from '../components/PostList.vue';
import PostDetails from '../components/PostDetails.vue';

const router = createRouter({
    history: createWebHistory(),
    routes: [
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
