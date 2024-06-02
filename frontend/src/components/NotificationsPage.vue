<template>
  <div class="notifications-page">
    <h1>通知</h1>
    <button @click="fetchNotifications">刷新通知</button>
    <button @click="goToAddNotification">增加通知</button>
    <!-- 新增的按钮 -->
    <p v-if="error" class="error-message">{{ error }}</p>
    <ul v-if="notificationsList.length > 0">
      <li
        v-for="notification in notificationsList"
        :key="notification.id"
        class="notification-item"
      >
        <p><strong>消息:</strong> {{ notification.message }}</p>
        <p><strong>发送者:</strong> {{ notification.sender }}</p>
        <p><strong>时间:</strong> {{ notification.created_at }}</p>
      </li>
    </ul>
    <p v-else class="no-notifications">暂无通知</p>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "NotificationsPage",
  data() {
    return {
      notificationsList: [], // 存储通知列表
      notificationsCount: 0, // 存储通知数量
      error: "",
    };
  },
  async created() {
    await this.fetchNotifications();
  },
  methods: {
    async fetchNotifications() {
      const accessToken = localStorage.getItem("access_token");
      if (!accessToken) {
        this.error = "请先登录";
        return;
      }

      try {
        const response = await axios.get(
          "http://localhost:8001/notifications/",
          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          }
        );
        // 解构赋值，从响应中提取通知数量和通知列表
        const { count, notifications } = response.data;
        this.notificationsCount = count; // 更新通知数量
        this.notificationsList = notifications; // 更新通知列表
        this.error = ""; // 清除之前的错误
      } catch (error) {
        // 错误处理，检查并使用错误响应的详细信息
        this.error =
          error.response && error.response.data
            ? error.response.data.detail
            : "获取通知失败，请重试";
      }
    },
    goToAddNotification() {
      this.$router.push("/add-notification");
    },
  },
};
</script>

<style scoped>
@font-face {
  font-family: "zql";
  src: url("../assets/font/zql.woff2") format("woff2");
}
.notifications-page {
  font-family: "zql";
  width: 95%;
  max-width: 600px;
  margin: 20px auto;
  padding: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  text-align: left;
}

header h1 {
  color: #34495e;
  font-size: 24px;
}

.button_content {
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
}

button {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  margin-left: 10px;
}

button:hover {
  background-color: #0056b3;
}

.error-message {
  color: #ff4d4f;
  text-align: center;
  margin: 10px 0;
}

ul {
  list-style: none;
  padding: 0;
}

.notification-item {
  background: rgba(255, 255, 255, 0.8);
  margin: 10px 0;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s;
}

.notification-item:hover {
  transform: scale(1.02);
}

.no-notifications {
  text-align: center;
  color: #34495e;
  font-size: 16px;
}
</style>
