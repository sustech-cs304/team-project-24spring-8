<template>
    <div class="user-profile">
      <h2>个人信息</h2>
      <form @submit.prevent="updateProfile">
        <div>
          <label for="name">姓名:</label>
          <input id="name" v-model="profile.name">
        </div>
        <div>
          <label for="email">邮箱:</label>
          <input id="email" v-model="profile.email">
        </div>
        <button type="submit">保存</button>
      </form>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        profile: {
          name: '张三',
          email: 'zhangsan@example.com'
        }
      };
    },
    methods: {
      updateProfile() {
        alert('个人信息已更新！');
      }
    }
  }
  </script>
  
  <style scoped>
  .user-profile h2 {
    color: #8e44ad;
  }
  .user-profile form {
    margin-top: 20px;
  }
  </style>
  