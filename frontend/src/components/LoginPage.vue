<!--
 * @Author: lerrorgk lerrorgk@163.com
 * @Date: 2024-05-27 15:15:01
 * @LastEditors: lerrorgk lerrorgk@163.com
 * @LastEditTime: 2024-05-27 16:50:10
 * @FilePath: \team-project-24spring-8\frontend\src\components\LoginPage.vue
 * @Description: 
-->
<template>
  <div class="d-flex justify-content-center align-items-center vh-100 login-background">
    <div class="card p-4 login-box" style="width: 400px;">
      <h1 class="card-title text-center mb-4">南科中心</h1>
      <form @submit.prevent="login">
        <div class="mb-3">
          <label for="username" class="form-label">用户名:</label>
          <input type="text" id="username" v-model="username" class="form-control" required />
        </div>
        <div class="mb-3">
          <label for="password" class="form-label">密码:</label>
          <input type="password" id="password" v-model="password" class="form-control" required />
        </div>
        <button type="submit" class="btn btn-primary w-100">登录</button>
      </form>
      <p v-if="error" class="text-danger mt-3">{{ error }}</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'LoginPage',
  data() {
    return {
      username: '',
      password: '',
      error: ''
    };
  },
  methods: {
    async login() {
      const formData = new URLSearchParams();
      formData.append('username', this.username);
      formData.append('password', this.password);

      try {
        const response = await axios.post('http://localhost:8001/token', formData);
        const { access_token, user_id } = response.data;
        localStorage.setItem('access_token', access_token); // Store the access token in local storage
        localStorage.setItem('username', this.username); // Store the username in local storage
        localStorage.setItem('user_id', user_id); // Store the user id in local storage
        this.$router.push({ name: 'HomePage' }); // Redirect to home page
      } catch (error) {
        this.error = error.response && error.response.data ? error.response.data.detail : '登录失败，请重试';
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
