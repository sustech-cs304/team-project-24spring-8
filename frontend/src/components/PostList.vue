<template>
  <div class="post-list">
    <h1>南科大计算机系讲座讨论</h1>
    <ul>
      <li v-for="post in posts" :key="post.id" class="post-item">
        <router-link :to="{ name: 'PostDetails', params: { postId: post.id.toString() }}" class="post-link">{{ post.title }}</router-link>
      </li>
    </ul>
    <div v-if="loading" class="loading">加载中...</div>
    <div v-if="error" class="error">{{ error }}</div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      posts: [],
      loading: false,
      error: null
    };
  },
  created() {
    this.fetchPosts();
  },
  methods: {
    async fetchPosts() {
      this.loading = true;
      try {
        // 替换'/api/posts'为你的后端实际API路径
        const response = await axios.get('http://localhost:8001/posts');
        this.posts = response.data;
      } catch (error) {
        this.error = '无法加载帖子。' + error.message;
      } finally {
        this.loading = false;
      }
    }
  }
}
</script>

<style scoped>
.post-list {
  max-width: 800px;
  margin: 20px auto;
  padding: 20px;
  background: linear-gradient(135deg, #957DAD, #D291BC);
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.post-list h1 {
  color: #6A0DAD;
  text-align: center;
  margin-bottom: 20px;
}

.post-list ul {
  list-style: none;
  padding: 0;
}

.post-list li {
  margin: 10px 0;
  transition: all 0.3s ease;
}

.post-item {
  border-bottom: 1px solid #eee;
  padding: 10px;
  transition: background-color 0.3s ease;
}

.post-item:last-child {
  border-bottom: none;
}

.post-link {
  text-decoration: none;
  color: #5E2D79;
  font-size: 18px;
  display: block;
  transition: color 0.3s ease;
}

.post-link:hover {
  color: #9A4DCE;
  text-decoration: underline;
}

.post-item:hover {
  background-color: #f4eaff;
}

.loading, .error {
  text-align: center;
  margin-top: 20px;
  color: #FF6347; /* Tomato color for error or loading messages */
}
</style>
