<template>
  <nav class="navbar">
    <div>
      <router-link to="/home" class="nav-link">Home</router-link>
      <router-link to="/discussions" class="nav-link">Discussion</router-link>
      <router-link to="/events" class="nav-link">Event</router-link>
      <router-link to="/tickets" class="nav-link">Tickets</router-link>
    </div>
    <div>
      <router-link to="/notifications" class="notification-bell" @click="markAllNotificationsRead">
        <span class="bell-icon">🔔</span>
        <span class="notification-count" v-if="notifications > 0">{{ notifications }}</span>
      </router-link>
      <div class="user-info">
        <router-link to="/user-detail" class="nav-link user-info">
        <img :src="avatarUrl" alt="用户头像" class="avatar">
        <span class="username-display">当前用户: {{ username }}</span>
        </router-link>
        <span class="user-money">余额: ¥{{ money }}</span>
      </div>
      <button @click="logout" class="action-button logout-button">退出登录</button>
    </div>
  </nav>
</template>



<script>
import axios from 'axios';

export default {
  name: 'NavbarPage',
  data() {
    return {
      notifications: 0,
      username: '未登录',
      avatarUrl: 'http://localhost:8001/avatars/default_avatar.png', // 默认头像 URL
      money: 0,
      intervalId: null
    };
  },
  created() {
    this.updateUserInfo();
    this.fetchNotificationCount();
    this.intervalId = setInterval(this.fetchNotificationCount, 100);
  },
  beforeUnmount() {
    if (this.intervalId) {
      clearInterval(this.intervalId);
    }
  },
  methods: {
    updateUserInfo() {
      const username = localStorage.getItem('username') || '未登录';
      const userId = localStorage.getItem('user_id');
      const accessToken = localStorage.getItem('access_token');

      if (userId && accessToken) {
        axios.get(`http://localhost:8001/users/${userId}`, {
          headers: {
            Authorization: `Bearer ${accessToken}`
          }
        })
        .then(response => {
          this.username = response.data.username;
          this.avatarUrl = response.data.avatar_path ? `http://localhost:8001/${response.data.avatar_path}` : this.avatarUrl;
          this.money = response.data.money;
          console.log('User data response:', `http://localhost:8001/${response.data.avatar_path}`);  // 添加这一行来输出 response 以进行调试
        })
        .catch(error => {
          console.error('无法获取用户数据:', error);
        });
      } else {
        this.username = username;
      }
    },
    async fetchNotificationCount() {
      const userId = localStorage.getItem('user_id');
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
        this.notifications = notifications.filter(notification => !notification.haven_read).length;

        const userResponse = await axios.get(`http://localhost:8001/users/${userId}`, {
          headers: {
            Authorization: `Bearer ${accessToken}`
          }
        });
        this.money = userResponse.data.money;
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
        await this.fetchNotificationCount();
      } catch (error) {
        console.error('Failed to mark notifications as read:', error);
      }
    },
    logout() {
      localStorage.removeItem('access_token');
      localStorage.removeItem('username');
      localStorage.removeItem('user_id');
      localStorage.removeItem('avatar_url');
      delete axios.defaults.headers.common['Authorization'];
      window.location.reload();
    }
  },
  watch: {
    '$route'() {
      this.updateUserInfo();
    }
  }
}
</script>

<style scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 20px;
  background: #ffffff;
  color: black;
  width: 100%;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.navbar > div {
  display: flex;
  align-items: center;
}

.nav-link {
  color: black;
  text-decoration: none;
  margin-right: 20px;
}

.notification-bell {
  cursor: pointer;
  position: relative;
  margin-right: 20px;
}

.notification-count {
  position: absolute;
  top: -10px;
  right: -10px;
  background-color: red;
  color: black;
  border-radius: 50%;
  padding: 2px 6px;
  font-size: 12px;
}

.user-info {
  display: flex;
  align-items: center;
  color: #fff;
}

.avatar {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  margin-right: 10px;
}

.username-display, .user-money {
  color: black;
  margin-right: 10px;
}

.username-display:hover {
  text-decoration: underline;
}

.logout-button {
  background-color: red;
  color: white;
  border: none;
  padding: 10px 20px;
  cursor: pointer;
  border-radius: 5px;
}

.logout-button:hover {
  background-color: darkred;
}
</style>
