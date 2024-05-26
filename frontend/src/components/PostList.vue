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
/* 表单样式 */
label {
  display: block;
  margin: 10px 0 5px;
}

input[type="text"], textarea {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
  margin-bottom: 10px;
}

.submit-button {
  padding: 10px 15px;
  background-color: #6A0DAD;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.submit-button:hover {
  background-color: #B48B9E;
}
</style>
