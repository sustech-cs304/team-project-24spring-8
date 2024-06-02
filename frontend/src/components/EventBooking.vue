<template>
  <div class="eventbooking">
    <h2>购票</h2>
    <p>{{ eventName }}</p>
    <p>剩余票数：{{ ticketsLeft }}</p>
    <form @submit.prevent="createTicket" class="eventbooking">
      <div class="form-group">
        <label for="name">姓名:</label>
        <input id="name" v-model="bookingData.name" placeholder="您的姓名" required>
      </div>
      <div class="form-group">
        <label for="IDcard">身份证号码:</label>
        <input id="IDcard" v-model="bookingData.IDcard" placeholder="身份证号码" required>
      </div>
      <div class="form-group">
        <label for="phonenumber">电话号码:</label>
        <input id="phonenumber" v-model="bookingData.phonenumber" placeholder="电话号码" required>
      </div>
      <div class="form-group">
        <label for="tickets">票数:</label>
        <input type="number" id="tickets" v-model.number="bookingData.tickets" placeholder="票数" min="1" :max="ticketsLeft" @input="updateTicketsLeft" required>
      </div>
      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
      <div class="button_content">
        <button type="submit" class="save-btn">提交订单</button>
      </div>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      eventID: this.$route.params.eventID,
      bookingData: {
        name: '',
        IDcard: '',
        phonenumber: '',
        tickets: 1
      },
      ticketsLeft: 0, // 存储剩余票数
      eventName: "未定义", // 存储活动名称
      errorMessage: '' // 用于存储错误信息
    };
  },
  created() {
    this.fetchTicketsLeft();
    this.fetchEventName();
  },
  methods: {
    fetchEventName() {
      fetch(`http://127.0.0.1:8001/events/${this.eventID}/event_name`)
        .then(response => {
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          return response.json();
        })
        .then(data => {
          this.eventName = data.event_name; 
        })
        .catch(error => {
          console.error('Failed to fetch event details:', error);
          this.errorMessage = 'Failed to fetch event details.';
        });
    },
    fetchTicketsLeft() {
      fetch(`http://127.0.0.1:8001/events/${this.eventID}/tickets_left`)
        .then(response => response.json())
        .then(data => {
          this.ticketsLeft = data.tickets_left;
        })
        .catch(error => console.error('Failed to fetch tickets left:', error));
    },
    updateTicketsLeft(event) {
      const requestedTickets = parseInt(event.target.value);
      if (requestedTickets > this.ticketsLeft) {
        this.errorMessage = `您最多只能购买 ${this.ticketsLeft} 张票。`;
        this.bookingData.tickets = this.ticketsLeft;
      } else {
        this.errorMessage = '';
      }
    },
    async createTicket() {
      if (!this.validateForm()) {
        alert('内容不能为空！');
        return;
      }
      try {
        const token = localStorage.getItem('access_token');
        if (!token) {
          this.errorMessage = '未授权：无Token';
          return;
        }
        const response = await axios.post(`http://127.0.0.1:8001/tickets/${this.eventID}`, {
          name: this.bookingData.name,
          IDcard: this.bookingData.IDcard,
          phonenumber: this.bookingData.phonenumber,
          number: this.bookingData.tickets
        }, {
          headers: { 'Authorization': `Bearer ${token}` }
        });

        response.data.message
        

        // 添加发送通知的代码
        await this.sendNotification(`成功购买了${this.bookingData.tickets}张票`);

        this.resetBookingData();
        this.fetchTicketsLeft(); // 更新剩余票数
      } catch (error) {
        this.errorMessage = '购票失败。' + (error.response && error.response.data.detail ? error.response.data.detail : error.message);
      }
    },
    async sendNotification(message) {
      try {
        const token = localStorage.getItem('access_token');
        await axios.post('http://127.0.0.1:8001/notifications/', {
          message: message,
          sender: "购票系统"
        }, {
          headers: { 'Authorization': `Bearer ${token}` }
        });
      } catch (error) {
        console.error('Failed to send notification:', error);
      }
    },
    // 重置预订数据的函数
    resetBookingData() {
      this.bookingData.name = '';
      this.bookingData.IDcard = '';
      this.bookingData.phonenumber = '';
      this.bookingData.tickets = 1;
    },
    // 表单验证函数
    validateForm() {
      // 简单的验证逻辑，确保所有字段都不为空
      return this.bookingData.name && this.bookingData.IDcard && this.bookingData.phonenumber && this.bookingData.tickets > 0;
    }
  }
};
</script>

<style scoped>
@font-face {
  font-family: "zql";
  src: url("../assets/font/zql.woff2") format("woff2");
}
.eventbooking {
  max-width: 600px;
  margin: 20px auto;
  padding: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  text-align: left;
}

.eventbooking h2 {
  color: #34495e;
  font-size: 24px;
}

.form-group {
  margin-bottom: 15px;
}

input[type="text"],
input[type="IDcard"],
input[type="phonenumber"],
input[type="tickets"] {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

input[type="text"]:focus,
input[type="IDcard"]:focus,
input[type="phonenumber"]:focus,
input[type="tickets"]:focus {
  border-color: #0056b3;
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

.save-btn {
  background-color: #0056b3;
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 5px;
  cursor: pointer;
  transition: background 0.3s ease;
}

.save-btn:hover {
  background-color: #34495e;
}

.error {
  color: red;
  font-size: 14px;
}
</style>
