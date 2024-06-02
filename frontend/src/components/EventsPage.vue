<template>
  <div class="eventspage">
    <header style="text-align: center">
      <h2>活动</h2>
    </header>
    <div class="controls-container">
      <div class="search-container mb-3">
        <input
          type="text"
          v-model="searchQuery"
          class="form-control"
          placeholder="搜索活动"
        />
      </div>
      <div class="button_content">
        <button type="button" class="btn btn-primary" @click="searchEvents">
          搜索
        </button>
        <span @click="toggleSortOrder('time')">
          {{ timeSortOrder === "asc" ? "时间从晚到早" : "时间从早到晚" }}
        </span>

        <span @click="toggleSortOrder('duration')">
          {{ durationSortOrder === "asc" ? "时长从长到短" : "时长从短到长" }}
        </span>
      </div>
    </div>
    <EventList :events="events" @selectEvent="showEventDetails" />
    <EventDetailsModal
      :event="selectedEvent"
      v-if="selectedEvent"
      @close="closeEventDetails"
    />
  </div>
</template>

<script>
import EventList from "./eventpagelist/EventList.vue";
import EventDetailsModal from "./eventpagelist/EventDetailsModal.vue";

export default {
  data() {
    return {
      events: [],
      selectedEvent: null,
      searchQuery: "",
      timeSortOrder: "asc", // 默认时间排序顺序
      durationSortOrder: "asc", // 默认时长排序顺序
    };
  },
  components: {
    EventList,
    EventDetailsModal,
  },
  methods: {
    showEventDetails(event) {
      this.selectedEvent = event;
    },
    closeEventDetails() {
      this.selectedEvent = null;
    },
    searchEvents() {
      fetch(
        `http://127.0.0.1:8001/events/?search=${encodeURIComponent(
          this.searchQuery
        )}`
      )
        .then((response) => response.json())
        .then((data) => {
          this.events = data;
          this.sortEvents("time");
        })
        .catch((error) => {
          console.error("Error fetching events:", error);
        });
    },
    toggleSortOrder(type) {
      if (type === "time") {
        this.timeSortOrder = this.timeSortOrder === "asc" ? "desc" : "asc";
        this.sortEvents("time");
      } else if (type === "duration") {
        this.durationSortOrder =
          this.durationSortOrder === "asc" ? "desc" : "asc";
        this.sortEvents("duration");
      }
    },
    sortEvents(type) {
      if (type === "time") {
        this.events.sort((a, b) => {
          const dateA = new Date(a.event_time);
          const dateB = new Date(b.event_time);
          return this.timeSortOrder === "asc" ? dateA - dateB : dateB - dateA;
        });
      } else if (type === "duration") {
        this.events.sort((a, b) => {
          const durationA = a.duration_hours * 60 + a.duration_minutes;
          const durationB = b.duration_hours * 60 + b.duration_minutes;
          return this.durationSortOrder === "asc"
            ? durationA - durationB
            : durationB - durationA;
        });
      }
      console.log(`Events sorted by ${type}:`, this.events); // 调试输出
    },
  },
  mounted() {
    fetch("http://127.0.0.1:8001/events/")
      .then((response) => response.json())
      .then((data) => {
        this.events = data;
        this.sortEvents("time");
      })
      .catch((error) => {
        console.error("Error fetching events:", error);
      });
  },
};
</script>

<style scoped>
@font-face {
  font-family: "zql";
  src: url("../assets/font/zql.woff2") format("woff2");
}
.eventspage {
  font-family: "zql";
}
.eventspage {
  width: 95%;
  max-width: 1200px;
  margin: 20px auto;
  padding: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  text-align: left;
}

header h2 {
  color: #34495e;
  font-size: 24px;
}

.controls-container {
  margin-bottom: 20px;
  display: flex;
  flex-direction: column;
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

.button_content {
  text-align: center;
  display: flex;
  align-items: flex-end;
  justify-content: center;
}

.button_content span {
  cursor: pointer;
  font-size: 13px;
  color: gray;
  /* 文字垂直居中 */
  margin-left: 10px;
}

.button_content button {
  padding-left: 20px;
  padding-right: 20px;
  margin-right: auto;
}
</style>
