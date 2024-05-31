<template>
  <div class="eventbooking">
    <h2>购票</h2>
    <p>剩余票数：{{ ticketsLeft }}</p>
    <p>id：{{ eventID}}</p>
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
        <input type="number" id="tickets" v-model.number="bookingData.tickets" placeholder="票数" min="1" required>
      </div>
      <button type="submit" class="save-btn">提交订单</button>
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
        // ticketType: 'regular'
      },
      ticketsLeft: 0, // 添加用于存储剩余票数的数据属性
    };
  },
  created() {
    this.fetchTicketsLeft();
  },
  methods: {
    fetchTicketsLeft() {
      fetch(`http://127.0.0.1:8001/events/${this.eventID}/tickets_left`)
        .then(response => response.json())
        .then(data => {
          this.ticketsLeft = data.tickets_left;
        })
        .catch(error => console.error('Failed to fetch tickets left:', error));
    },
    async createTicket() {
      if (!this.validateForm()) {  // 确保是调用方法，添加括号
        alert('内容不能为空！');
        return;
      }
      try {
        const token = localStorage.getItem('access_token');  // 确保Token被正确获取
        if (!token) {
          this.error = '未授权：无Token';
          return;  // 如果没有Token，不发送请求
        }
        const response = await axios.post(`http://127.0.0.1:8001/tickets/${this.eventID}`, {
          name: this.bookingData.name,
          IDcard: this.bookingData.IDcard,
          phonenumber: this.bookingData.phonenumber,
          number: this.bookingData.tickets  // 确保发送的字段名称与后端模型一致
        }, {
          headers: { 'Authorization': `Bearer ${token}` }  // 确保Token正确添加到请求头
        });
        if (response.data.message) {
          alert(response.data.message);  // 显示后端返回的成功信息
        }
        this.resetBookingData();
      } catch (error) {
        this.error = '购票失败。' + (error.response && error.response.data.detail ? error.response.data.detail : error.message);  // 显示从后端获取的错误信息
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

<!-- 使用一个表单来收集用户的预订信息，包括姓名、电子邮件、票数和票务类型。
通过 v-model 指令将表单输入的值绑定到 bookingData 对象中，以便在表单提交时收集用户输入的信息。
当用户提交表单时，调用 updatebookingData 方法处理表单提交。
在这个方法中添加表单验证逻辑，并向后端发送预订请求并处理响应。   -->

<style scoped>

  .eventbooking {
      max-width: 600px;
      margin: 20px auto;
      padding: 20px;
      background: white;
      border-radius: 8px;
      box-shadow: 0 4px 6px rgba(0,0,0,0.1);
      text-align: left;
  }

  .eventbooking h2 {
      color: #34495e;
      font-size: 24px;
  }
  .form-group {
      margin-bottom: 15px;
  }

  input[type="text"], input[type="IDcard"], input[type="phonenumber"],input[type="tickets"] {
      width: 100%;
      padding: 10px;
      border: 1px solid #ccc;
      border-radius: 5px;
  }

  .save-btn {
      background-color: #8e44ad;
      color: white;
      border: none;
      padding: 10px 15px;
      border-radius: 5px;
      cursor: pointer;
      transition: background 0.3s ease;
  }

  .save-btn:hover {
      background-color: #5e3370;
  }
</style>