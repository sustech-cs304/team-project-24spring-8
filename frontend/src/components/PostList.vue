<template>
  <div class="post-list">
    <h1>南科大计算机系讲座讨论</h1>

    <!-- 发帖表单 -->
    <form @submit.prevent="submitPost">
      <div>
        <label for="postTitle">标题:</label>
        <input id="postTitle" v-model="newPost.title" type="text" required>
      </div>
      <div>
        <label for="postContent">内容:</label>
        <textarea id="postContent" v-model="newPost.content" required></textarea>
      </div>
      <button type="submit" class="submit-button">发帖</button>
    </form>

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
      newPost: {
        title: '',
        content: ''
      },
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
        const response = await axios.get('http://localhost:8001/posts');
        this.posts = response.data;
      } catch (error) {
        this.error = '无法加载帖子。' + error.message;
      } finally {
        this.loading = false;
      }
    },
    async submitPost() {
    if (!this.newPost.title || !this.newPost.content) {
      alert('标题和内容不能为空！');
      return;
    }
    try {
      const token = localStorage.getItem('access_token');  // 确保Token被正确获取
      if (!token) {
        this.error = '未授权：无Token';
        return;  // 如果没有Token，不发送请求
      }
      const response = await axios.post('http://localhost:8001/posts', {
        title: this.newPost.title,
        content: this.newPost.content
      }, {
        headers: { 'Authorization': `Bearer ${token}` }  // 确保Token正确添加到请求头
      });
      this.posts.push(response.data);
      this.newPost.title = '';
      this.newPost.content = '';
    } catch (error) {
      this.error = '发帖失败。' + error.response.data.detail;  // 显示从后端获取的错误信息
    }
  }


  }
}
</script>


<style scoped>
@font-face {
  font-family: "zql";
  src: url("../assets/font/zql.woff2") format("woff2");
}
.post-list {
  font-family: "zql";
  width: 95%;
  max-width: 800px;
  margin: 20px auto;
  padding: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  text-align: left;
}

header h1 {
  color: #34495e;
  font-size: 24px;
}

.input-group label {
  display: block;
  margin-bottom: 5px;
  color: #34495e;
}

input[type="text"], textarea {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

.post-form {
  margin-bottom: 20px;
}

.submit-button {
  width: 100%;
  padding: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
}

.submit-button:hover {
  background-color: #0056b3;
}

.post-list ul {
  list-style: none;
  padding: 0;
}

.post-item {
  margin: 10px 0;
  padding: 10px;
  border-bottom: 1px solid #ccc;
  transition: background-color 0.3s;
}

.post-item:hover {
  background-color: #f0f0f0;
}

.post-link {
  text-decoration: none;
  color: #000000;
  font-size: 18px;
}

.loading, .error {
  text-align: center;
  color: #ff4d4f;
  margin-top: 20px;
}
</style>
