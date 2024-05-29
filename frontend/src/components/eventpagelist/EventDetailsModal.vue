<template>
  <div class="modal" @click.self="$emit('close')">
    <div class="modal-content">
      <span class="close" @click="$emit('close')">&times;</span>
      <h2>详细信息</h2>
      <h3>{{ event.name }}</h3>
      <p>Date: {{ formatDate(event.event_time) }}</p>
      <p>Description: {{ event.description }}</p>
      <p>Duration: {{ formatDuration(event.duration_hours, event.duration_minutes) }}</p> <!-- 新增行 -->
    </div>
  </div>
</template>

<script>
export default {
  props: {
    event: {
      type: Object,
      required: true
    }
  },
  methods: {
    formatDate(date) {
      if (!date) return '';
      const options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' };
      return new Date(date).toLocaleDateString(undefined, options);
    },
    formatDuration(hours, minutes) { // 新增方法
      if (hours == null && minutes == null) return 'N/A';
      const hrs = hours ? `${hours}h` : '';
      const mins = minutes ? `${minutes}m` : '';
      return `${hrs} ${mins}`.trim();
    }
  }
};
</script>

<style scoped>
.modal {
  display: block;
  position: fixed;
  z-index: 1;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgba(0,0,0,0.4);
}

.modal-content {
  background-color: #fefefe;
  margin: 10% auto;
  padding: 20px;
  border: 1px solid #888;
  width: 80%;
}

.close {
  color: #aaa;
  float: right;
  font-size: 28px;
  font-weight: bold;
}

.close:hover,
.close:focus {
  color: black;
  text-decoration: none;
  cursor: pointer;
}
</style>
