<template>
  <div class="modal" @click.self="$emit('close')">
    <div class="modal-content">
      <span class="close" @click="$emit('close')">&times;</span>
      <div style="text-align: center"><h2>详细信息</h2></div>
      <div class="a_name">{{ event.name }}</div>
      <div class="a_main">
        <p class="a_des">{{ event.description }}</p>
        <div class="a_time">
          <p>时间: {{ formatDate(event.event_time) }}</p>

          <p>
            持续:
            {{ formatDuration(event.duration_hours, event.duration_minutes) }}
          </p>
        </div>
        <div class="a_ticket">
          <p>已售票数: {{ event.tickets_sold }}</p>
          <p>最大参会: {{ event.max_tickets }}</p>
        </div>
      </div>
      <button @click="bookTickets" style="margin-bottom: 10px">购票</button>
      <button @click="toggleExpand">查看更多</button>

      <!-- 可展开的内容区域 -->
      <div v-if="isExpanded">
        <div class="comment-list">
          <span>评论区</span>

          <!-- 评论表单 -->
          <form @submit.prevent="submitComment">
            <div class="comment_content">
              <!-- <label for="commentContent">评论:</label> -->
              <input
                class="form-control"
                id="commentContent"
                v-model="newComment.content"
                type="text"
                required
              /><button type="submit" class="submit-button">评论</button>
            </div>
          </form>
          <ul>
            <li v-for="comment in comments" :key="comment.id" class="post-item">
              {{ comment.content }}
            </li>
          </ul>
          <div v-if="loading" class="loading">加载中...</div>
          <div v-if="error" class="error">{{ error }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  props: {
    event: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      isExpanded: false,
      comments: [],
      newComment: {
        content: "",
      },
      loading: false,
      error: null,
    };
  },
  created() {
    this.fetchComments();
  },
  methods: {
    async fetchComments() {
      this.loading = true;
      try {
        const response = await axios.get(
          `http://localhost:8001/comments/${this.event.id}`
        );
        this.comments = response.data;
      } catch (error) {
        this.error = "无法加载评论。" + error.message;
      } finally {
        this.loading = false;
      }
    },
    async submitComment() {
      if (!this.newComment.content) {
        alert("内容不能为空！");
        return;
      }
      try {
        const token = localStorage.getItem("access_token"); // 确保Token被正确获取
        if (!token) {
          this.error = "未授权：无Token";
          return; // 如果没有Token，不发送请求
        }
        const response = await axios.post(
          `http://localhost:8001/comments/${this.event.id}`,
          {
            content: this.newComment.content,
          },
          {
            headers: { Authorization: `Bearer ${token}` }, // 确保Token正确添加到请求头
          }
        );
        this.comments.push(response.data);
        this.newComment.content = "";
      } catch (error) {
        this.error = "发送评论失败。" + error.response.data.detail; // 显示从后端获取的错误信息
      }
    },
    formatDate(date) {
      if (!date) return "";
      const options = {
        year: "numeric",
        month: "long",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      };
      return new Date(date).toLocaleDateString(undefined, options);
    },
    formatDuration(hours, minutes) {
      // 新增方法
      if (hours == null && minutes == null) return "N/A";
      const hrs = hours ? `${hours}h` : "";
      const mins = minutes ? `${minutes}m` : "";
      return `${hrs} ${mins}`.trim();
    },

    bookTickets() {
      // 跳转到订票页面
      this.$router.push({
        name: "EventBooking",
        params: { eventID: this.event.id },
      });
    },
    toggleExpand() {
      this.isExpanded = !this.isExpanded;
    },
  },
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
  background-color: rgba(0, 0, 0, 0.4);
}

.modal-content {
  cursor: pointer;
  background-color: #fefefe;
  margin: 10% auto;
  padding: 20px;
  border: 1px solid #888;
  width: 80%;
  max-width: 450px;
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

.comment-list span {
  font-size: 16px;
  font-weight: 700;
}

input[type="text"] {
  margin-right: 10px;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  padding: 8px 16px;
  background-color: #007bff;
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
.comment_content {
  margin-top: 20px;
  display: flex;
}

.comment_content input {
  display: flex;
  flex: 3;
}
.submit-button {
  flex: 1;
}

.a_name {
  font-size: 18px;
  font-weight: 700;
  margin-bottom: 15px;
}
.a_des {
  /* 缩进 */
  text-indent: 2em;
  font-size: 16px;
  margin-bottom: 20px;
  border: black 1px dotted;
  padding: 10px;
}

.a_time {
  font-weight: 100;
  font-size: 13px;
  color: grey;
  display: flex;
  justify-content: space-between;
  margin-top: 15px;
}
.a_time p {
  margin-bottom: 0px;
}
.a_ticket {
  font-weight: 100;
  font-size: 13px;
  color: grey;
  display: flex;
  justify-content: space-between;
}

.post-item {
  border: 1px black solid;
  padding: 6px;
  padding-left: 15px;
  border-radius: 0px 15px 15px 23px;
}
</style>
