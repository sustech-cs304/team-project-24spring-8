<template>
  <div class="eventspage">
    <header>
      <h2>活动</h2>
    </header>
    <div class="controls-container">
      <div class="search-container">
        <input type="text" v-model="searchQuery" placeholder="搜索活动" @keyup.enter="searchEvents" />
        <button @click="searchEvents">搜索</button>
      </div>
      <button @click="toggleSortOrder('time')">
        {{ timeSortOrder === 'asc' ? '按时间从晚到早排序' : '按时间从早到晚排序' }}
      </button>
      <button @click="toggleSortOrder('duration')">
        {{ durationSortOrder === 'asc' ? '按时长从长到短排序' : '按时长从短到长排序' }}
      </button>
    </div>
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
      events: [],
      selectedEvent: null,
      searchQuery: '',
      timeSortOrder: 'asc', // 默认时间排序顺序
      durationSortOrder: 'asc' // 默认时长排序顺序
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
    },
    searchEvents() {
      fetch(`http://127.0.0.1:8001/events/?search=${encodeURIComponent(this.searchQuery)}`)
        .then(response => response.json())
        .then(data => {
          this.events = data;
          this.sortEvents('time');
        })
        .catch(error => {
          console.error('Error fetching events:', error);
        });
    },
    toggleSortOrder(type) {
      if (type === 'time') {
        this.timeSortOrder = this.timeSortOrder === 'asc' ? 'desc' : 'asc';
        this.sortEvents('time');
      } else if (type === 'duration') {
        this.durationSortOrder = this.durationSortOrder === 'asc' ? 'desc' : 'asc';
        this.sortEvents('duration');
      }
    },
    sortEvents(type) {
      if (type === 'time') {
        this.events.sort((a, b) => {
          const dateA = new Date(a.event_time);
          const dateB = new Date(b.event_time);
          return this.timeSortOrder === 'asc' ? dateA - dateB : dateB - dateA;
        });
      } else if (type === 'duration') {
        this.events.sort((a, b) => {
          const durationA = a.duration_hours * 60 + a.duration_minutes;
          const durationB = b.duration_hours * 60 + b.duration_minutes;
          return this.durationSortOrder === 'asc' ? durationA - durationB : durationB - durationA;
        });
      }
      console.log(`Events sorted by ${type}:`, this.events); // 调试输出
    }
  },
  mounted() {
    fetch('http://127.0.0.1:8001/events/')
      .then(response => response.json())
      .then(data => {
        this.events = data;
        this.sortEvents('time');
      })
      .catch(error => {
        console.error('Error fetching events:', error);
      });
  }
};
</script>

<style scoped>
.eventspage {
  max-width: 600px;
  margin: 20px auto;
  padding: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  text-align: left;
}

header h2 {
  color: #34495e;
  font-size: 24px;
}

.controls-container {
  margin-bottom: 20px;
  display: flex;
  justify-content: space-between;
}

.search-container {
  flex-grow: 1;
  display: flex;
}

.search-container input {
  flex-grow: 1;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

.search-container button {
  padding: 8px;
  margin-left: 5px;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.search-container button:hover {
  background-color: #2980b9;
}

button {
  padding: 8px;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #2980b9;
}
</style>
