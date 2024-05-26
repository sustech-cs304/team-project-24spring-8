<template>
  <nav class="navbar">
    <div>
      <router-link to="/home" class="nav-link">Home</router-link> <!-- 新增 Home 链接 -->
      <router-link to="/discussions" class="nav-link">Discussion</router-link>
      <router-link to="/events" class="nav-link">Event</router-link>
    </div>
    <div>
      <router-link to="/reminders" class="notification-bell">
        <span class="bell-icon">🔔</span>
        <span class="notification-count" v-if="notifications > 0">{{ notifications }}</span>
      </router-link>
      <router-link to="user-detail" class="nav-link">
        <span class="username-display">当前用户: {{ username }}</span>
      </router-link>
    </div>
  </nav>
</template>






<script>
export default {
  name: 'NavbarPage',
  data() {
    return {
      notifications: 3, // 假设有3个通知
      username: localStorage.getItem('username') || '未登录' // 获取存储的用户名或显示默认值
    };
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


