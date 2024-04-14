// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import ActivityReminders from '../components/ActivityReminders.vue';
import UserProfile from '../components/UserProfile.vue';
import EventsPage from '../components/EventsPage.vue';
import EventBooking from '../components/EventBooking.vue';

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
            path: '/eventspage',
            name: 'EventsPage',
            component: EventsPage
        },
        {
            path: '/eventbooking',
            name: 'EventBooking',
            component: EventBooking
        }
    ]
});

export default router;
