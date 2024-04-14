// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import ActivityReminders from '../components/ActivityReminders.vue';
import UserProfile from '../components/UserProfile.vue';

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
        }
    ]
});

export default router;
