<template>
  <div class="modal" @click.self="$emit('close')">
    <div class="modal-content">
      <span class="close" @click="$emit('close')">&times;</span>
      <h2>详细信息</h2>
      <h3>{{ event.name }}</h3>
      <p>Date: {{ formatDate(event.event_time) }}</p>
      <p>Description: {{ event.description }}</p>
      <p>Duration: {{ formatDuration(event.duration_hours, event.duration_minutes) }}</p>
      <p>tickets_sold: {{ event.tickets_sold }}</p>
      <p>max_tickets: {{ event.max_tickets }}</p>

      <button @click="toggleExpand">查看更多</button>

      <!-- 可展开的内容区域 -->
      <div v-if="isExpanded">
        <button @click="bookTickets">购票</button>
        <div class="comment-list">
          <h1>评论区</h1>

          <!-- 评论表单 -->
          <form @submit.prevent="submitComment">
            <div>
              <label for="commentContent">评论:</label>
              <input id="commentContent" v-model="newComment.content" type="text" required>
            </div>
            <button type="submit" class="submit-button">评论</button>
          </form>
          <ul>
            <li v-for="comment in comments" :key="comment.id" class="post-item">{{ comment.content }}</li>
          </ul>
          <div v-if="loading" class="loading">加载中...</div>
          <div v-if="error" class="error">{{ error }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  props: {
    event: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      isExpanded: false,
      comments: [],
      newComment: {
        content: '',
      },
      loading: false,
      error: null
    };
  },
  created() {
    this.fetchComments();
  },
  methods: {
    async fetchComments() {
      this.loading = true;
      try {
        const response = await axios.get(`http://localhost:8001/comments/${this.event.id}`);
        this.comments = response.data;
      } catch (error) {
        this.error = '无法加载评论。' + error.message;
      } finally {
        this.loading = false;
      }
    },
    async submitComment() {
      if (!this.newComment.content) {
        alert('内容不能为空！');
        return;
      }
      try {
        const token = localStorage.getItem('access_token');  // 确保Token被正确获取
        if (!token) {
          this.error = '未授权：无Token';
          return;  // 如果没有Token，不发送请求
        }
        const response = await axios.post(`http://localhost:8001/comments/${this.event.id}`, {
          content: this.newComment.content,
        }, {
          headers: { 'Authorization': `Bearer ${token}` }  // 确保Token正确添加到请求头
        });
        this.comments.push(response.data);
        this.newComment.content = '';
      } catch (error) {
        this.error = '发送评论失败。' + error.response.data.detail;  // 显示从后端获取的错误信息
      }
    },
    formatDate(date) {
      if (!date) return '';
      const options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' };
      return new Date(date).toLocaleDateString(undefined, options);
    },
    formatDuration(hours, minutes) { // 新增方法
      if (hours == null && minutes == null) return 'N/A';
      const hrs = hours ? `${hours}h` : '';
      const mins = minutes ? `${minutes}m` : '';
      return `${hrs} ${mins}`.trim();
    },

    bookTickets() {
      // 跳转到订票页面
      this.$router.push({ name: 'EventBooking', params: { eventID: this.event.id } });
    },
    toggleExpand() {
      this.isExpanded = !this.isExpanded;
    }
  }
};
</script>

<style scoped>
.modal {
  display: block;
  position: fixed;
  z-index: 1;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgba(0,0,0,0.4);
}

.modal-content {
  background-color: #fefefe;
  margin: 10% auto;
  padding: 20px;
  border: 1px solid #888;
  width: 80%;
}

.close {
  color: #aaa;
  float: right;
  font-size: 28px;
  font-weight: bold;
}

.close:hover,
.close:focus {
  color: black;
  text-decoration: none;
  cursor: pointer;
}

.comment-list {
  margin-top: 20px;
}

.comment-list h3 {
  margin-bottom: 10px;
}

input[type="text"] {
  margin-right: 10px;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  padding: 8px 16px;
  background-color: #007BFF;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}

.comment-list ul {
  list-style: none;
  padding: 0;
}

.comment-list li {
  margin: 10px 0;
  transition: all 0.3s ease;
}
</style>
