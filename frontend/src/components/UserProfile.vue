<template>
  <div class="user-profile">
    <h2>个人信息</h2>
    <form @submit.prevent="updateProfile" class="profile-form">
      <div class="avatar-upload">
        <img :src="profile.avatar || 'default-avatar.png'" alt="avatar" class="user-avatar">
        <input type="file" @change="previewAvatar" id="avatarUpload" hidden>
        <label for="avatarUpload" class="upload-label">点击更换头像</label>
      </div>
      <div class="form-group">
        <label for="username">用户名:</label>
        <input id="username" v-model="profile.username" placeholder="请输入用户名">
      </div>
      <div class="form-group">
        <label for="name">姓名:</label>
        <input id="name" v-model="profile.name" placeholder="您的姓名">
      </div>
      <div class="form-group">
        <label for="email">邮箱:</label>
        <input id="email" v-model="profile.email" placeholder="电子邮件地址">
      </div>
      <button type="submit" class="save-btn">保存更改</button>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      profile: {
        username: 'zhangsan',
        name: '张三',
        email: 'zhangsan@example.com',
        avatar: null
      }
    };
  },
  methods: {
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
}
</script>

<style scoped>
.user-profile {
  max-width: 500px;
  margin: auto;
  background: linear-gradient(135deg, #957DAD, #D291BC);
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
  color: #fff; /* Ensuring text is visible on darker backgrounds */
}

.user-profile h2 {
  color: #D291BC; /* Consistent purple theme for headers */
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
  color: #f0e8f0; /* Light purple text for better readability */
}

input[type="text"], input[type="email"], input[type="file"] {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background: #ffffff50; /* Slightly transparent white for inputs */
  color: #000; /* Dark text for input for readability */
}

.save-btn {
  background-color: #8e44ad; /* Dark purple button */
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 5px;
  cursor: pointer;
  transition: background 0.3s ease;
}

.save-btn:hover {
  background-color: #5e3370; /* Lighter purple when hovered */
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
  color: #8e44ad; /* Maintaining the purple theme */
  cursor: pointer;
  font-size: 0.9em;
  transition: color 0.3s ease;
}

.upload-label:hover {
  color: #5e3370; /* Lighter purple on hover */
}
</style>
