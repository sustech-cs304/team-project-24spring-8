<template>
    <div>
      <h2>Event Booking</h2>
      <form @submit.prevent="submitBookingForm">
        <label for="name">Name:</label>
        <input type="text" id="name" v-model="bookingData.name" required>
        <label for="email">Email:</label>
        <input type="email" id="email" v-model="bookingData.email" required>
        <label for="tickets">Number of Tickets:</label>
        <input type="number" id="tickets" v-model.number="bookingData.tickets" required>
        <label for="ticketType">Ticket Type:</label>
        <select id="ticketType" v-model="bookingData.ticketType" required>
          <option value="regular">Regular</option>
          <option value="vip">VIP</option>
        </select>
        <button type="submit">Submit Booking</button>
      </form>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        bookingData: {
          name: '',
          email: '',
          tickets: 1,
          ticketType: 'regular'
        }
      };
    },
    methods: {
      submitBookingForm() {
        // 这里可以添加表单验证逻辑
  
        // 提交预订表单
        console.log('Booking form submitted:', this.bookingData);
        // 在此处向后端发送预订请求并处理响应
      }
    }
  };
  </script>
<!-- 使用一个表单来收集用户的预订信息，包括姓名、电子邮件、票数和票务类型。
通过 v-model 指令将表单输入的值绑定到 bookingData 对象中，以便在表单提交时收集用户输入的信息。
当用户提交表单时，调用 submitBookingForm 方法处理表单提交。
在这个方法中添加表单验证逻辑，并向后端发送预订请求并处理响应。   -->