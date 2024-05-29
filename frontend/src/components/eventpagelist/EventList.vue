<template>
  <div class="event-list">
    <ul>
      <li v-for="event in events" :key="event.id" @click="selectEvent(event)">
        {{ event.name }}
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  props: {
    events: {
      type: Array,
      required: true
    }
  },
  methods: {
    selectEvent(event) {
      this.$emit('selectEvent', event);
    }
  }
};
</script>

<style scoped>
.event-list ul {
  list-style-type: none;
  padding: 0;
}

.event-list li {
  padding: 10px;
  cursor: pointer;
  border-bottom: 1px solid #ccc;
}

.event-list li:hover {
  background-color: #f0f0f0;
}
</style>
