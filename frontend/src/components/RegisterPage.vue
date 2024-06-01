<template>
    <div class="d-flex justify-content-center align-items-center vh-100 login-background">
      <div class="card p-4 login-box" style="width: 400px;">
        <h1 class="card-title text-center mb-4">注册</h1>
        <form @submit.prevent="register">
          <div class="mb-3">
            <label for="username" class="form-label">用户名:</label>
            <input type="text" id="username" v-model="username" class="form-control" required />
          </div>
          <div class="mb-3">
            <label for="email" class="form-label">电子邮件:</label>
            <input type="email" id="email" v-model="email" class="form-control" required />
          </div>
          <div class="mb-3">
            <label for="full_name" class="form-label">全名:</label>
            <input type="text" id="full_name" v-model="full_name" class="form-control" required />
          </div>
          <div class="mb-3">
            <label for="password" class="form-label">密码:</label>
            <input type="password" id="password" v-model="password" class="form-control" required />
          </div>
          <button type="submit" class="btn btn-primary w-100">注册</button>
        </form>
        <p v-if="error" class="text-danger mt-3">{{ error }}</p>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'RegisterPage',
    data() {
      return {
        username: '',
        email: '',
        full_name: '',
        password: '',
        error: ''
      };
    },
    methods: {
      async register() {
        try {
          await axios.post('http://localhost:8001/users/', {
            username: this.username,
            email: this.email,
            full_name: this.full_name,
            hashed_password: this.password
          });
          this.$router.push({ name: 'LoginPage' }); // Redirect to login page after successful registration
        } catch (error) {
          this.error = error.response && error.response.data ? error.response.data.detail : '注册失败，请重试';
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .login-background {
    background: url('images/login_background.jpg') no-repeat center center fixed;
    background-size: cover;
  }
  
  .login-box {
    background: rgba(255, 255, 255, 0.8); /* 白色背景，80%透明度 */
    border-radius: 10px;
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
  }
  
  /* 调整按钮样式 */
  .btn-primary {
    background-color: #74ebd5;
    border-color: #74ebd5;
  }
  .btn-primary:hover {
    background-color: #66d3c1;
    border-color: #66d3c1;
  }
  
  /* 调整输入框样式 */
  .form-control {
    border-radius: 5px;
    border-color: #ddd;
    box-shadow: none;
  }
  .form-control:focus {
    border-color: #74ebd5;
    box-shadow: 0 0 5px rgba(116, 235, 213, 0.5);
  }
  
  /* 调整错误信息样式 */
  .text-danger {
    color: red;
  }
  </style>
  