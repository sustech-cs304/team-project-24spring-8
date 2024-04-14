<template>
    <div>
      <h3>Event List</h3>
      <ul>
        <li v-for="event in events" :key="event.id" @click="selectEvent(event)">
          {{ event.name }} - {{ event.date }}
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
  /* Add your styles here */
  </style>
  