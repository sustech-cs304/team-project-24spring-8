<template>
  <div class="modal" @click.self="$emit('close')">
    <div class="modal-content">
      <span class="close" @click="$emit('close')">&times;</span>
      <h2>详细信息</h2>
      <h3>{{ event.name }}</h3>
      <p>Date: {{ formatDate(event.event_time) }}</p>
      <p>Description: {{ event.description }}</p>
      <p>Duration: {{ formatDuration(event.duration_hours, event.duration_minutes) }}</p>


      <button @click="toggleExpand">查看更多</button>

      <!-- 可展开的内容区域 -->
      <div v-if="isExpanded">
        <button @click="bookTickets">购票</button>
        <div class="comments-section">
          <h3>评论</h3>
          <ul>
            <li v-for="comment in comments" :key="comment.id">
              {{ comment.user }}: {{ comment.text }}
            </li>
          </ul>
          <form @submit.prevent="submitComment">
            <input v-model="newComment" placeholder="添加评论" />
            <button type="submit">提交</button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>



<script>
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
      comments: [],  // 存储评论的数组
      newComment: '' // 绑定到输入框的新评论文本
    };
  },
  methods: {
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
      this.$router.push({ name: 'EventBooking', params: { eventId: this.event.id } });
    },
    submitComment() {
      // 提交评论的方法
      const comment = {
        user: '当前用户',  // 这里应该替换为实际的用户标识
        text: this.newComment,
        id: Date.now()   // 简单生成唯一ID的方法
      };
      this.comments.push(comment); // 添加评论到数组
      this.newComment = '';        // 清空输入框
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

.comments-section {
  margin-top: 20px;
}

.comments-section h3 {
  margin-bottom: 10px;
}

.comments-section ul {
  list-style: none;
  padding: 0;
}

.comments-section li {
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
</style>
