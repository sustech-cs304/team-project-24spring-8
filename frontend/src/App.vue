<template>
  <div id="app">
    <NavbarPage @update:currentComponent="setCurrentComponent" />
    <div v-if="currentComponent === 'community'">
      <CommunityPage />
    </div>
    <div v-else-if="currentComponent === 'events'">
      <EventsPage />
    </div>
    <div v-else-if="currentComponent === 'recommendations'">
      <RecommendationsList />
    </div>
    <!-- 其他组件 -->
    <h1>{{ message }}</h1>
    <button @click="fetchMessage">Fetch Message from FastAPI</button>
    <button @click="goToReminders">查看提醒</button>
    <button @click="goToUserProfile">用户配置</button>
    <router-view></router-view>
  </div>
</template>

<script>
import NavbarPage from './components/NavbarPage.vue';
import CommunityPage from './components/CommunityPage.vue';
import EventsPage from './components/EventsPage.vue';
import RecommendationsList from './components/RecommendationsList.vue';
import axios from 'axios';
import router from './router';

export default {
  router,
  methods: {
    async fetchMessage() {
      try {
        const response = await axios.get('http://localhost:8000/hello');
        this.message = response.data.message;
      } catch (error) {
        console.error(error);
      }
    },
    goToReminders() {
      this.$router.push({ name: 'ActivityReminders' });
    },
    goToUserProfile() {
      this.$router.push({ name: 'UserProfile' });
    }
  },
};
</script>
