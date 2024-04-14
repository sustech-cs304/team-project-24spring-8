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
  </div>
</template>

<script>
import NavbarPage from './components/NavbarPage.vue';
import CommunityPage from './components/CommunityPage.vue';
import EventsPage from './components/EventsPage.vue';
import RecommendationsList from './components/RecommendationsList.vue';
import axios from 'axios';

export default {
  components: {
    NavbarPage,
    CommunityPage,
    EventsPage,
    RecommendationsList,
  },
  data() {
    return {
      currentComponent: 'community',
      message: '',
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
    setCurrentComponent(component) {
      this.currentComponent = component;
    },
  },
};
</script>
