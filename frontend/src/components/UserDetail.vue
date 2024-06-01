<template>
  <div class="user-detail-container">
    <h1>用户详情</h1>
    <p>用户名: {{ username }}</p>

    <div class="user-profile">
      <h2>个人信息</h2>
      <form @submit.prevent="updateProfile" class="profile-form">
        <div class="form-group">
          <label for="name">姓名:</label>
          <input type="text" id="name" v-model="profile.name" placeholder="请输入姓名" />
        </div>
        <div class="form-group">
          <label for="email">邮箱:</label>
          <input type="email" id="email" v-model="profile.email" placeholder="请输入邮箱" />
        </div>
        <div class="form-group">
          <label for="avatar">头像:</label>
          <input type="file" id="avatar" @change="previewAvatar" />
          <div class="avatar-upload">
            <img v-if="profile.avatar" :src="profile.avatar" alt="User Avatar" class="user-avatar" />
          </div>
        </div>
        <button type="submit" class="save-btn">保存</button>
      </form>
    </div>

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
      error: '',
      profile: {
        name: '张三',
        email: 'zhangsan@example.com',
        avatar: null
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
    updateProfile() {
      alert('个人信息已更新！');
    },
    previewAvatar(event) {
      const reader = new FileReader();
      reader.onload = (e) => {
        this.profile.avatar = e.target.result;
      };
      reader.readAsDataURL(event.target.files[0]);
    }
  }
};
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

.user-profile {
  max-width: 500px;
  margin: auto;
  background: linear-gradient(135deg, #957DAD, #D291BC);
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
  color: #fff;
}

.user-profile h2 {
  color: #5e3370;
  text-align: center;
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
  color: #f0e8f0;
}

input[type="text"], input[type="email"], input[type="file"] {
  width: 100%;
  padding: 10px;
  border-radius: 5px;
  background: #ffffff30;
  color: #fff;
  border: 2px solid #ffffff50;
  box-shadow: none;
}

input::placeholder {
  color: #e6e6e6;
}

.save-btn {
  background-color: #8e44ad;
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.save-btn:hover {
  background-color: #5e3370;
}

.avatar-upload {
  text-align: center;
  margin-bottom: 20px;
}

.user-avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  border: 2px solid #8e44ad;
  object-fit: cover;
}

.upload-label {
  display: block;
  color: #8e44ad;
  cursor: pointer;
  font-size: 0.9em;
  transition: color 0.3s ease;
}

.upload-label:hover {
  color: #5e3370;
}

</style>
