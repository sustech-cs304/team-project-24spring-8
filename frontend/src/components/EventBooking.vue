<template>
  <div class="eventbooking">
    <h2>活动预订</h2>
    <form @submit.prevent="updatebookingData" class="eventbooking">
      <div class="form-group">
          <label for="name">姓名:</label>
          <input id="name" v-model="bookingData.name" placeholder="您的姓名">
      </div>
      <div class="form-group">
          <label for="IDcard">身份证号码:</label>
          <input id="IDcard" v-model="bookingData.IDcard" placeholder="身份证号码">
      </div>
      <div class="form-group">
          <label for="phonenumber">电话号码:</label>
          <input id="phonenumber" v-model="bookingData.phonenumber" placeholder="电话号码">
      </div>
      <div class="form-group">
          <label for="tickets">票数:</label>
          <input id="tickets" v-model="bookingData.tickets" placeholder="票数">
      </div>
      <!-- <label for="ticketType">Ticket Type:</label>
      <select id="ticketType" v-model="bookingData.ticketType" required>
        <option value="regular">Regular</option>
        <option value="vip">VIP</option>
      </select> -->
      <button type="submit" class="save-btn">提交订单</button>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      bookingData: {
        name: '',
        IDcard: '',
        phonenumber: '',
        tickets: 1,
        ticketType: 'regular'
      }
    };
  },
  methods: {
      updatebookingData() {
          alert('订单已提交！');
          // console.log('Booking form submitted:', this.bookingData);// 在此处向后端发送预订请求并处理响应
      }
  }
};
</script>
<!-- 使用一个表单来收集用户的预订信息，包括姓名、电子邮件、票数和票务类型。
通过 v-model 指令将表单输入的值绑定到 bookingData 对象中，以便在表单提交时收集用户输入的信息。
当用户提交表单时，调用 submitBookingForm 方法处理表单提交。
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