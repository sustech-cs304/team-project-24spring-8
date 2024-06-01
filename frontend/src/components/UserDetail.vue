<template>
  <div class="user-detail-container">
    <h1 class="text-center mb-4">用户详情</h1>
    <div class="card user-card">
      <div class="card-body">
        <h2 class="card-title">个人信息</h2>
        <form @submit.prevent="updateProfile" class="profile-form">
          <div class="form-group">
            <label for="name">姓名:</label>
            <input type="text" id="name" v-model="profile.full_name" placeholder="请输入姓名" class="form-control" />
          </div>
          <div class="form-group">
            <label for="email">邮箱:</label>
            <input type="email" id="email" v-model="profile.email" placeholder="请输入邮箱" class="form-control" />
          </div>
          <button type="submit" class="btn btn-primary w-100">保存</button>
        </form>
      </div>
    </div>

    <div class="card user-card mt-4">
      <div class="card-body">
        <h2 class="card-title">修改密码</h2>
        <form @submit.prevent="changePassword" class="profile-form">
          <div class="form-group">
            <label for="password">新密码:</label>
            <input type="password" id="password" v-model="newPassword" placeholder="请输入新密码" class="form-control" required />
          </div>
          <button type="submit" class="btn btn-primary w-100">修改密码</button>
        </form>
        <p v-if="message" class="text-success mt-3">{{ message }}</p>
        <p v-if="error" class="text-danger mt-3">{{ error }}</p>
      </div>
    </div>
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
      error: '',
      profile: {
        full_name: '',
        email: ''
      }
    };
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
    },
    async updateProfile() {
      try {
        const userId = localStorage.getItem('user_id');
        const token = localStorage.getItem('access_token');
        const response = await axios.put(`http://localhost:8001/users/${userId}/profile`, {
          full_name: this.profile.full_name,
          email: this.profile.email
        }, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });

        this.profile.full_name = response.data.full_name;
        this.profile.email = response.data.email;
        this.message = '个人信息已更新！';
        this.error = '';
      } catch (error) {
        this.error = error.response && error.response.data ? error.response.data.detail : '个人信息更新失败，请重试';
        this.message = '';
      }
    },
    async fetchUserProfile() {
      try {
        const userId = localStorage.getItem('user_id');
        const token = localStorage.getItem('access_token');
        const response = await axios.get(`http://localhost:8001/users/${userId}`, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        this.profile.full_name = response.data.full_name;
        this.profile.email = response.data.email;
      } catch (error) {
        console.error("无法获取用户信息", error);
      }
    }
  },
  created() {
    this.fetchUserProfile();
  }
};
</script>

<style scoped>
.user-detail-container {
  max-width: 600px;
  margin: 50px auto;
  padding: 20px;
}

.user-card {
  background: white;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  padding: 20px;
  margin-bottom: 20px;
}

.card-title {
  color: #5e3370;
  text-align: center;
  margin-bottom: 20px;
}

.profile-form {
  display: flex;
  flex-direction: column;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
  color: #333;
}

input[type="text"], input[type="email"], input[type="file"], input[type="password"] {
  width: 100%;
  padding: 10px;
  border-radius: 5px;
  background: #f9f9f9;
  border: 1px solid #ddd;
  box-shadow: none;
}

input::placeholder {
  color: #999;
}

.btn-primary {
  background-color: #8e44ad;
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn-primary:hover {
  background-color: #5e3370;
}

.avatar-upload {
  text-align: center;
  margin-top: 10px;
}

.user-avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  border: 2px solid #8e44ad;
  object-fit: cover;
}
</style>
