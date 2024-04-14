<template>
    <div>
      <h2>Events Page</h2>
      <event-list :events="events" @select="showEventDetails" />
      <event-details
        v-if="selectedEvent"
        :event="selectedEvent"
        @close="selectedEvent = null"
        @book="bookEvent"
      />
    </div>
  </template>
  
  <script>
  import EventList from './EventList.vue';
  import EventDetails from './EventDetails.vue';
  
  export default {
    components: {
      EventList,
      EventDetails
    },
    data() {
      return {
        events: [
          { id: 1, name: 'Event 1', date: '2024-05-01', description: 'Description of Event 1' },
          { id: 2, name: 'Event 2', date: '2024-05-15', description: 'Description of Event 2' },
          { id: 3, name: 'Event 3', date: '2024-05-30', description: 'Description of Event 3' }
        ],
        selectedEvent: null
      };
    },
    methods: {
      showEventDetails(event) {
        this.selectedEvent = event;
      },
      bookEvent(event) {
        // Implement booking logic here
        console.log('Booking event:', event);
      }
    }
  };
  </script>
  <!-- 在这个组件中：

  <event-list> 组件接收一个 events prop，用于显示活动列表，并通过 @select 事件将选定的活动发送给父组件。
  <event-details> 组件接收一个 event prop，用于显示选定的活动的详细信息，并允许用户预订活动。它通过 @close 事件关闭模态窗口，并通过 @book 事件将用户的预订信息发送给父组件。
  还需要创建两个子组件 EventList.vue 和 EventDetails.vue 分别用于显示事件列表和事件详情，然后在父组件中引入-->