<template>
  <div class="post-details">
    <h1>{{ post ? post.title : "Post Not Found" }}</h1>
    <p v-if="post">{{ post.content }}</p>
    <p v-else-if="error">{{ error }}</p>
    <p v-else>The requested post does not exist or could not be loaded.</p>
    <router-link to="/posts" class="back-link">返回讨论列表</router-link>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      post: null,
      error: null
    };
  },
  created() {
    this.fetchPost(this.$route.params.postId);
  },
  methods: {
    async fetchPost(postId) {
      try {
        const response = await axios.get(`http://localhost:8001/posts/${postId}`);
        this.post = response.data;
      } catch (error) {
        if (error.response && error.response.status === 404) {
          this.error = "The requested post does not exist.";
        } else {
          this.error = "An error occurred while loading the post.";
        }
      }
    }
  }
}
</script>

<style scoped>
.post-details {
  max-width: 800px;
  margin: 20px auto;
  padding: 20px;
  background: linear-gradient(135deg, #957DAD, #D291BC);
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  text-align: left;
  color: #FFFFFF;
}

.post-details h1 {
  color: #6A0DAD;
  text-align: center;
  margin-bottom: 20px;
}

p {
  font-size: 16px;
  line-height: 1.6;
}

.back-link {
  display: block;
  text-align: center;
  margin-top: 20px;
  color: #FFFFFF;
  text-decoration: none;
  background-color: #957DAD;
  padding: 10px 15px;
  border-radius: 5px;
  transition: background-color 0.3s;
}

.back-link:hover {
  background-color: #B48B9E;
  text-decoration: underline;
}
</style>
