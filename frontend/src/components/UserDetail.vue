<template>
    <div class="user-detail-container">
      <h1>用户详情</h1>
      <p>用户名: {{ username }}</p>
      <form @submit.prevent="changePassword">
        <div class="mb-3">
          <label for="password" class="form-label">新密码:</label>
          <input type="password" id="password" v-model="newPassword" class="form-control" required />
        </div>
        <button type="submit" class="btn btn-primary">修改密码</button>
      </form>
      <p v-if="message" class="text-success mt-3">{{ message }}</p>
      <p v-if="error" class="text-danger mt-3">{{ error }}</p>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'UserDetail',
    data() {
      return {
        username: localStorage.getItem('username'),
        newPassword: '',
        message: '',
        error: ''
      }
    },
    methods: {
      async changePassword() {
        try {
          const userId = localStorage.getItem('user_id'); // 获取存储的用户ID
          const token = localStorage.getItem('access_token');
          await axios.put(`http://localhost:8001/users/${userId}/password`, {
            password: this.newPassword
          }, {
            headers: {
              Authorization: `Bearer ${token}`
            }
          });
          this.message = '密码修改成功';
          this.error = '';
        } catch (error) {
          this.error = error.response && error.response.data ? error.response.data.detail : '密码修改失败，请重试';
          this.message = '';
        }
      }
    }
  }
  </script>
  
  <style scoped>
  .user-detail-container {
    max-width: 600px;
    margin: 50px auto;
    padding: 20px;
    background: white;
    border-radius: 10px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  }
  
  .text-success {
    color: green;
  }
  
  .text-danger {
    color: red;
  }
  </style>
  