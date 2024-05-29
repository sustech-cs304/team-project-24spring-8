<template>
  <div class="eventbooking">
    <h2>购票</h2>
    <form @submit.prevent="updatebookingData" class="eventbooking">
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
export default {
  data() {
    return {
      bookingData: {
        name: '',
        IDcard: '',
        phonenumber: '',
        tickets: 1
        // ticketType: 'regular'
      }
    };
  },
  methods: {
    createTicketApi(ticketData) {
      return fetch('http://127.0.0.1:8001/tickets/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(ticketData)
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      });
    },
    submitTicketForm() {
      this.createTicketApi(this.bookingData)
        .then(() => {
          alert('购票成功！');
          this.bookingData = { name: '', IDcard: '', phonenumber: '', tickets: 1};
        })
        .catch(error => {
          alert('购票失败，请重试。');
          console.error('购票错误:', error);
        });
    },
    updatebookingData() {
      if (this.validateForm()) {
        this.submitTicketForm();
      } else {
        alert('请填写所有必填项！');
      }
    },
    validateForm() {
      // 简单的验证逻辑
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