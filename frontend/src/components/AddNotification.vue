<!--
 * @Author: lerrorgk lerrorgk@163.com
 * @Date: 2024-05-31 19:49:44
 * @LastEditors: lerrorgk lerrorgk@163.com
 * @LastEditTime: 2024-05-31 19:49:54
 * @FilePath: \team-project-24spring-8\frontend\src\components\AddNotification.vue
 * @Description: 
-->
<template>
    <div class="add-notification-page">
      <h1>增加通知</h1>
      <form @submit.prevent="addNotification">
        <input v-model="message" placeholder="Enter notification message" required />
        <input v-model="sender" placeholder="Enter sender name" required />
        <button type="submit">Add Notification</button>
      </form>
      <div v-if="error" class="error-message">{{ error }}</div>
      <div v-if="notification" class="success-message">
        <p>Notification added successfully!</p>
        <p>Message: {{ notification.message }}</p>
        <p>Sender: {{ notification.sender }}</p>
        <p>Created At: {{ notification.created_at }}</p>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'AddNotification',
    data() {
      return {
        message: '',
        sender: '',
        notification: null,
        error: ''
      };
    },
    methods: {
      async addNotification() {
        const accessToken = localStorage.getItem('access_token');
        if (!accessToken) {
          this.error = '请先登录';
          return;
        }
  
        try {
          const response = await axios.post(
            'http://localhost:8001/notifications/',
            {
              message: this.message,
              sender: this.sender
            },
            {
              headers: {
                Authorization: `Bearer ${accessToken}`
              }
            }
          );
          this.notification = response.data;
          this.error = '';
          this.message = '';
          this.sender = '';
        } catch (error) {
          this.error = error.response && error.response.data ? error.response.data.detail : 'Failed to add notification';
        }
      }
    }
  };
  </script>
  
  <style>
  /* 添加适当的 CSS 样式 */
  .add-notification-page {
    padding: 20px;
  }
  
  .error-message {
    color: red;
  }
  
  .success-message {
    margin-top: 10px;
  }
  </style>
  