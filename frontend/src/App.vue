<template>
  <div id="app" class="app-container">
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

    <div class="button-container">
      <button @click="fetchMessage" class="action-button">Fetch Message</button>
      <button @click="goToReminders" class="action-button">查看提醒</button>
      <button @click="goToUserProfile" class="action-button">用户配置</button>
      <button @click="goToPostList" class="action-button">帖子列表</button>
      <button @click="goToRecommendationsList" class="action-button">个性化推荐</button>
      <button @click="goToEventsPage" class="action-button">活动</button>
      <button @click="goToEventBooking" class="action-button">活动预订</button>
      <button @click="fetchFirstUsername" class="action-button">获取第一个用户的用户名</button>
    </div>
    <p v-if="username">第一个用户的用户名: {{ username }}</p>
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
      currentComponent: 'home',
      message: '',
      username: ''
    };
  },
  methods: {
    async fetchMessage() {
      try {
        const response = await axios.get('http://localhost:8002/hello');
        this.message = response.data.message;
      } catch (error) {
        console.error(error);
      }
    },
    async fetchFirstUsername() {
      try {
        const response = await axios.get('http://localhost:8002/users/user1');
        this.username = response.data.username;
        console.messages(this.username);
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
    goToEventsPage() {
      this.$router.push({ name: 'EventsPage' });
    },
    goToEventBooking() {
      this.$router.push({ name: 'EventBooking' });
    },
    goToRecommendationsList() {
      this.$router.push({ name: 'RecommendationsList' });
    },
    goToPostList() {
      this.$router.push({ name: 'PostList' });
    }
  }
};
</script>

<style scoped>
.app-container {
  text-align: center;
  padding: 20px;
  background: linear-gradient(135deg, #957DAD, #D291BC);
  color: white;
}

h1 {
  color: #fff;
  margin-bottom: 20px;
}

.button-container {
  margin: 20px 0;
}

.action-button {
  margin: 0 10px;
  background-color: #6A0DAD;
  color: #fff;
  border: none;
  padding: 10px 15px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.action-button:hover {
  background-color: #B48B9E;
}

p {
  color: #fff;
  margin-top: 20px;
}
</style>
