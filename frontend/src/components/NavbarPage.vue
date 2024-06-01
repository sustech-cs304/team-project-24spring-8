<template>
  <nav class="navbar">
    <div>
      <router-link to="/home" class="nav-link">Home</router-link>
      <router-link to="/discussions" class="nav-link">Discussion</router-link>
      <router-link to="/events" class="nav-link">Event</router-link>
    </div>
    <div>
      <router-link to="/notifications" class="notification-bell" @click="markAllNotificationsRead">
        <span class="bell-icon">🔔</span>
        <span class="notification-count" v-if="notifications > 0">{{ notifications }}</span>
      </router-link>
      <router-link to="/user-detail" class="nav-link">
        <span class="username-display">当前用户: {{ username }}</span>
      </router-link>
    </div>
  </nav>
</template>

<script>
import axios from 'axios';

export default {
  name: 'NavbarPage',
  data() {
    return {
      notifications: 0, // 初始化通知数量为 0
      username: '未登录', // 初始化用户名为未登录
      intervalId: null // 用于存储定时器 ID
    };
  },
  created() {
    this.updateUsername();
    this.fetchNotificationCount();
    // 设置定时器每 10 秒刷新一次
    this.intervalId = setInterval(this.fetchNotificationCount, 10000);
  },
  beforeUnmount() {
    // 清除定时器
    if (this.intervalId) {
      clearInterval(this.intervalId);
    }
  },
  methods: {
    updateUsername() {
      this.username = localStorage.getItem('username') || '未登录';
    },
    async fetchNotificationCount() {
      const accessToken = localStorage.getItem('access_token');
      if (!accessToken) {
        console.error('请先登录');
        return;
      }
      try {
        const response = await axios.get('http://localhost:8001/notifications/', {
          headers: {
            Authorization: `Bearer ${accessToken}`
          }
        });
        const notifications = response.data.notifications;
        this.notifications = notifications.filter(notification => !notification.haven_read).length; // 计算未读通知数量
      } catch (error) {
        console.error('Failed to fetch notifications:', error);
      }
    },
    async markAllNotificationsRead() {
      const accessToken = localStorage.getItem('access_token');
      if (!accessToken) {
        console.error('请先登录');
        return;
      }
      try {
        await axios.put('http://localhost:8001/notifications/mark_all_read', {}, {
          headers: {
            Authorization: `Bearer ${accessToken}`
          }
        });
        // 更新通知计数
        await this.fetchNotificationCount();
      } catch (error) {
        console.error('Failed to mark notifications as read:', error);
      }
    }
  },
  watch: {
    '$route'() {
      // 每次路由变化时更新用户名
      this.updateUsername();
    }
  }
}
</script>

<style scoped>
.navbar {
  display: flex; /* 确保使用 flex 布局 */
  justify-content: space-between; /* 两端对齐 */
  align-items: center; /* 垂直居中 */
  padding: 10px 20px;
  background: #333;
  color: #fff;
  width: 100%; /* 确保导航条宽度为 100% */
}

.navbar > div {
  display: flex; /* 确保内部 div 也使用 flex 布局 */
  align-items: center; /* 垂直居中 */
}

.nav-link {
  color: #fff;
  text-decoration: none;
  margin-right: 20px; /* 为导航链接之间添加右边距 */
}

.notification-bell {
  cursor: pointer;
  position: relative; /* 相对定位用于通知计数 */
  margin-right: 20px; /* 右边距离下一个元素 */
}

.notification-count {
  position: absolute;
  top: -10px;
  right: -10px;
  background-color: red;
  color: white;
  border-radius: 50%;
  padding: 2px 6px;
  font-size: 12px;
}

.username-display {
  color: #fff;
}

.username-display:hover {
  text-decoration: underline;
}
</style>
