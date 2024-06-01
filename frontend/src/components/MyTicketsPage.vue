<template>
    <div class="my-tickets-page">
      <h2>我的购票</h2>
      <ul v-if="tickets.length > 0">
        <li v-for="ticket in tickets" :key="ticket.id">
          <div>活动: {{ ticket.event_name }}</div>
          <div>票数: {{ ticket.number }}</div>
          <div>时间: {{ new Date(ticket.event_time).toLocaleString() }}</div>
        </li>
      </ul>
      <p v-else>没有已购买的票。</p>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'MyTicketsPage',
    data() {
      return {
        tickets: []
      };
    },
    async created() {
      try {
        const userId = localStorage.getItem('user_id'); // 获取当前用户ID
        if (userId) {
          const response = await axios.get(`http://localhost:8001/users/${userId}/tickets`);
          this.tickets = response.data;
        } else {
          console.error('User ID not found in localStorage');
        }
      } catch (error) {
        console.error('Error fetching tickets:', error);
      }
    }
  };
  </script>
  
  <style scoped>
  .my-tickets-page {
    padding: 20px;
    background: #fff;
    color: #333;
  }
  
  .my-tickets-page ul {
    list-style-type: none;
    padding: 0;
  }
  
  .my-tickets-page li {
    background: #f9f9f9;
    padding: 10px;
    margin-bottom: 10px;
    border: 1px solid #ddd;
    border-radius: 5px;
  }
  </style>
  