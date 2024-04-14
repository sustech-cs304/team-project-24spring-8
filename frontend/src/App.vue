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
    <h1>{{ message }}</h1>
    <button @click="fetchMessage">Fetch Message from FastAPI</button>
    <button @click="goToReminders">查看提醒</button>
    <button @click="goToUserProfile">用户配置</button>
    <button @click="goToPostList">帖子列表</button>
    <router-view></router-view>
  </div>
</template>

<script>
import axios from 'axios';
import router from './router';

export default {
  router,
  data() {
    return {
      currentComponent: 'home'
    };
  },
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
    },
    goToPostList() {
      this.$router.push({ name: 'PostList' });
    }
  },
};
</script>
