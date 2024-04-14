<template>
  <div id="app">
    <h1>{{ message }}</h1>
    <button @click="fetchMessage">Fetch Message from FastAPI</button>
    <button @click="goToReminders">查看提醒</button>
    <button @click="goToUserProfile">用户配置</button>
    <router-view></router-view>
  </div>
</template>

<script>
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
