<template>
  <div class="event-list">
    <ul>
      <li
        v-for="event in events"
        :key="event.id"
        class="list-group-item d-flex justify-content-between align-items-start"
        @click="selectEvent(event)"
      >
        <div class="ms-2 me-auto">
          <div class="fw-bold">{{ event.name }}</div>
          <span class="time_still"
            >持续时长：{{
              formatDuration(event.duration_hours, event.duration_minutes)
            }}</span
          >
        </div>
        <span class="badge bg-primary rounded-pill">{{
          event.event_time
        }}</span>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  props: {
    events: {
      type: Array,
      required: true,
    },
  },
  methods: {
    selectEvent(event) {
      this.$emit("selectEvent", event);
    },
    formatDuration(hours, minutes) {
      // 新增方法
      if (hours == null && minutes == null) return "N/A";
      const hrs = hours ? `${hours}h` : "";
      const mins = minutes ? `${minutes}m` : "";
      return `${hrs} ${mins}`.trim();
    },
  },
};
</script>

<style scoped>
.event-list ul {
  list-style-type: none;
  padding: 0;
}
.fw-bold {
  font-size: 18px;
}
.event-list li {
  padding: 10px;
  cursor: pointer;
  border-bottom: 1px solid #ccc;
}

.event-list li:hover {
  background-color: #f0f0f0;
}

.time_still {
  font-size: 14px;
  color: gray;
}
</style>
