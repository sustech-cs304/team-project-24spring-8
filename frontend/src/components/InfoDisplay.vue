<template>
    <div class="info-display">
      <h2>{{ activity.category }}</h2>
      <p>Date: {{ activity.date }}</p>
      <p>Location: {{ activity.location }}</p>
      <p>Description: {{ activity.description }}</p>
    </div>
  </template>
  
  <script>
  export default {
    name: 'InfoDisplay',
    props: {
      activity: {
        type: Object,
        required: true
      }
    }
  };
  </script>