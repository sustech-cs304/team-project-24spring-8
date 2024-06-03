<!-- /**
* AI-generated-content
* tool: ChatGPT
* version: 4
* usage: Add avatar before the comment content
*/ -->

<template>
  <div class="post-details">
    <h1>{{ post ? post.title : "Post Not Found" }}</h1>
    <p v-if="post">{{ post.content }}</p>
    <p v-else-if="error">{{ error }}</p>
    <p v-else>The requested post does not exist or could not be loaded.</p>
    <router-link to="/posts" class="back-link">返回讨论列表</router-link>

    <!-- 可展开的内容区域 -->
    <div class="comment-list">
      <span>评论区</span>

      <!-- 评论表单 -->
      <form @submit.prevent="submitComment">
        <div class="comment_content">
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
          <img :src="comment.avatarUrl" alt="用户头像" class="avatar">
          {{ comment.content }}
        </li>
      </ul>
      <div v-if="loading" class="loading">加载中...</div>
      <div v-if="error" class="error">{{ error }}</div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      post: null,
      error: null,
      comments: [],
      newComment: {
        content: "",
      },
      loading: false,
      isExpanded: false,
      avatarUrl: "http://localhost:8001/avatars/default_avatar.png",
    };
  },
  created() {
    this.fetchPost(this.$route.params.postId);
    this.fetchComments(this.$route.params.postId);
  },
  methods: {
    async fetchPost(postId) {
      try {
        const response = await axios.get(`http://localhost:8001/posts/${postId}`);
        this.post = response.data;
      } catch (error) {
        if (error.response && error.response.status === 404) {
          this.error = "The requested post does not exist.";
        } else {
          this.error = "An error occurred while loading the post.";
        }
      }
    },
    async fetchComments(postId) {
      this.loading = true;
      try {
        const response = await axios.get(`http://localhost:8001/post_comments/${postId}`);
        this.comments = response.data;
        for (let comment of this.comments) {
          const userId = comment.owner_id;
          const accessToken = localStorage.getItem('access_token');
          if (userId && accessToken) {
            try {
              const userResponse = await axios.get(`http://localhost:8001/users/${userId}`, {
                headers: {
                  Authorization: `Bearer ${accessToken}`
                }
              });
              comment.avatarUrl = userResponse.data.avatar_path ? `http://localhost:8001/${userResponse.data.avatar_path}` : this.avatarUrl;
            } catch (error) {
              console.error('无法获取用户数据:', error);
              comment.avatarUrl = this.avatarUrl; // 使用默认头像
            }
          } else {
            comment.avatarUrl = this.avatarUrl; // 使用默认头像
          }
        }
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
        console.log("提交的评论内容：", this.newComment.content);
        const response = await axios.post(
          `http://localhost:8001/post_comments/${this.$route.params.postId}`,
          {
            content: this.newComment.content,
          },
          {
            headers: { Authorization: `Bearer ${token}` }, // 确保Token正确添加到请求头
          }
        );
        console.log("服务器返回的响应：", response.data);
        this.comments.push(response.data);
        this.newComment.content = "";
      } catch (error) {
        console.error("发送评论失败：", error);
        this.error = "发送评论失败。" + (error.response && error.response.data ? error.response.data.detail : error.message); // 显示从后端获取的错误信息
      }
    },
  }
}
</script>

<style scoped>
@font-face {
  font-family: "zql";
  src: url("../assets/font/zql.woff2") format("woff2");
}

.post-details {
  font-family: "zql";
  width: 95%;
  max-width: 800px;
  margin: 20px auto;
  padding: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  text-align: left;
}

header h1 {
  color: #34495e;
  font-size: 24px;
  margin-bottom: 20px;
}

.post-content {
  font-size: 16px;
  line-height: 1.6;
  color: #333;
  text-indent: 2em;
  margin-bottom: 20px;
}

.error, .no-content {
  color: #ff4d4f;
  text-align: center;
}

.back-link {
  display: block;
  text-align: center;
  margin-top: 20px;
  color: white;
  text-decoration: none;
  background-color: #007bff;
  padding: 10px 15px;
  border-radius: 5px;
  transition: background-color 0.3s;
}

.back-link:hover {
  background-color: #0056b3;
  text-decoration: underline;
}

.comment-list {
  margin-top: 20px;
}

.comment-list span {
  display: block;
  font-size: 20px;
  color: #34495e;
  margin-bottom: 10px;
}

.comment_content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.comment_content input {
  flex: 1;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 5px;
  margin-right: 10px;
}

.comment_content .submit-button {
  background-color: #28a745;
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.comment_content .submit-button:hover {
  background-color: #218838;
}

.post-item {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.post-item .avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 10px;
}

.loading {
  text-align: center;
  font-size: 16px;
  color: #888;
}

.error {
  text-align: center;
  font-size: 16px;
  color: #ff4d4f;
}
</style>
