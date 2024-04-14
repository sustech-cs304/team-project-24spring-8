<template>
    <div>
      <h2>Events Page</h2>
      <EventList :events="events" @selectEvent="showEventDetails" />
      <EventDetailsModal :event="selectedEvent" v-if="selectedEvent" @close="closeEventDetails" />
    </div>
  </template>
  
  <script>
  import EventList from './eventpagelist/EventList.vue';
  import EventDetailsModal from './eventpagelist/EventDetailsModal.vue';
  
  export default {
    data() {
      return {
        events: [
          { id: 1, name: 'Event 1', date: '2024-04-16', description: 'Description of Event 1' },
          { id: 2, name: 'Event 2', date: '2024-04-17', description: 'Description of Event 2' },
          // Add more events as needed
        ],
        selectedEvent: null
      };
    },
    components: {
      EventList,
      EventDetailsModal
    },
    methods: {
      showEventDetails(event) {
        this.selectedEvent = event;
      },
      closeEventDetails() {
        this.selectedEvent = null;
      }
    }
  };
  </script>
  
  <style scoped>
  /* Add your styles here */
  </style>
  
  

<style>
/* 样式 */
</style>
