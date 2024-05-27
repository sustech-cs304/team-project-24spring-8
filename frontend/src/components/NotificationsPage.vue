<template>
    <div class="notifications-page">
      <h1>通知</h1>
      <button @click="fetchNotifications">刷新通知</button>
      <p v-if="error">{{ error }}</p>
      <ul v-if="notificationsList.length > 0">
        <li v-for="notification in notificationsList" :key="notification.id">
          {{ notification.message }}
        </li>
      </ul>
      <p v-else>暂无通知</p>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'NotificationsPage',
    data() {
      return {
        notificationsList: [],  // 存储通知列表
        notificationsCount: 0,  // 存储通知数量
        error: ''
      };
    },
    async created() {
      await this.fetchNotifications();
    },
    methods: {
      async fetchNotifications() {
        const accessToken = localStorage.getItem('access_token');
        if (!accessToken) {
          this.error = '请先登录';
          return;
        }
        
        try {
          const response = await axios.get('http://localhost:8001/notifications/', {
            headers: {
              Authorization: `Bearer ${accessToken}`
            }
          });
          // 解构赋值，从响应中提取通知数量和通知列表
          const { count, notifications } = response.data;
          this.notificationsCount = count;  // 更新通知数量
          this.notificationsList = notifications;  // 更新通知列表
          this.error = ''; // 清除之前的错误
        } catch (error) {
          // 错误处理，检查并使用错误响应的详细信息
          this.error = error.response && error.response.data ? error.response.data.detail : '获取通知失败，请重试';
        }
      }
    }
  }
  </script>
  
  <style scoped>
  .notifications-page {
    padding: 20px;
    background: #f4f4f4;
    color: #333;
  }
  
  h1 {
    color: #333;
  }
  
  button {
    margin: 10px 0;
    padding: 8px 16px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #0056b3;
  }
  
  ul {
    list-style: none;
    padding: 0;
  }
  
  li {
    background: white;
    margin: 10px 0;
    padding: 10px;
    border-radius: 5px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  }
  </style>
  