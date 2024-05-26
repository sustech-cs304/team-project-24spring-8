<template>
  <nav class="navbar">
    <router-link to="/discussions" class="nav-link">Discussion</router-link>
    <router-link to="/events" class="nav-link">Event</router-link>
    <router-link to="/reminders" class="notification-bell">
      <span class="bell-icon">🔔</span>
      <span class="notification-count" v-if="notifications > 0">{{ notifications }}</span>
    </router-link>
  </nav>
</template>

<script>
export default {
  name: 'NavbarPage',
  data() {
    return {
      notifications: 3 // 假设有3个通知
    };
  }
}
</script>

<style scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  padding: 10px 20px;
  background: #333;
  color: #fff;
}

.nav-link {
  color: #fff;
  text-decoration: none;
}

.notification-bell {
  cursor: pointer;
  position: relative;
}

.notification-count {
  position: absolute;
  top: -5px;
  right: -10px;
  background-color: red;
  color: white;
  border-radius: 50%;
  padding: 2px 6px;
  font-size: 12px;
}
</style>
