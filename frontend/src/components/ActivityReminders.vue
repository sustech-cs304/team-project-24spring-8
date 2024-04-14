<template>
    <div class="reminders">
      <h2>活动提醒</h2>
      <ul>
        <li v-for="reminder in reminders" :key="reminder.id">
          {{ reminder.message }} - {{ reminder.time }}
        </li>
      </ul>
  
      <h3>通知设置</h3>
      <label>
        <input type="checkbox" v-model="notificationsEnabled">
        启用通知
      </label>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        reminders: [
          { id: 1, message: '会议时间', time: '9:00 AM' },
          { id: 2, message: '医生预约', time: '1:00 PM' }
        ],
        notificationsEnabled: true
      };
    }
  }
  </script>
  
  <style scoped>
  .reminders h2 {
    color: #2c3e50;
  }
  .reminders ul {
    list-style-type: none;
  }
  </style>
  