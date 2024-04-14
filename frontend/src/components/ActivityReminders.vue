<template>
  <section class="reminders">
    <header>
      <h2>活动提醒</h2>
    </header>
    <ul>
      <li v-for="reminder in reminders" :key="reminder.id" class="reminder-item">
        {{ reminder.message }} - {{ reminder.time }}
      </li>
    </ul>
    <div class="settings">
      <h3>通知设置</h3>
      <label class="switch">
        <input type="checkbox" v-model="notificationsEnabled">
        <span class="slider round"></span>
      </label>
    </div>
  </section>
</template>

<script>
export default {
  data() {
    return {
      reminders: [
        { id: 1, message: '南科大计算机系讲座预约', time: '2024.4.14 16:20 PM' },
        { id: 2, message: '计算机系趣味运动会', time: '2024.4.15 18:00 PM' }
      ],
      notificationsEnabled: true
    };
  }
}
</script>

<style scoped>
.reminders {
  max-width: 600px;
  margin: 20px auto;
  padding: 20px;
  background: linear-gradient(135deg, #957DAD, #D291BC); /* Purple gradient background */
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  text-align: left;
}

header h2 {
  color: #6A0DAD; /* Deep purple for header to stand out */
  font-size: 24px;
  text-align: center;
}

.reminder-item {
  padding: 10px 0;
  border-bottom: 1px solid #EEE;
  cursor: pointer;
  transition: background-color 0.3s;
  color: #FFFFFF; /* White text for better readability */
}

.reminder-item:hover {
  background-color: #f4eaff; /* Very light purple background on hover */
}

.settings {
  margin-top: 20px;
}

.switch {
  position: relative;
  display: inline-block;
  width: 60px;
  height: 34px;
}

.switch input { 
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  transition: .4s;
  border-radius: 34px;
}

.slider:before {
  position: absolute;
  content: "";
  height: 26px;
  width: 26px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  transition: .4s;
  border-radius: 50%;
}

input:checked + .slider {
  background-color: #8e44ad; /* Consistent purple theme for toggle */
}

input:focus + .slider {
  box-shadow: 0 0 1px #8e44ad;
}

input:checked + .slider:before {
  transform: translateX(26px);
}
</style>
