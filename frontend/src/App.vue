<template>
  <div id="app">
    <h1>{{ message }}</h1>
    <button @click="fetchMessage">Fetch Message from FastAPI</button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
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
  },
};
</script>
