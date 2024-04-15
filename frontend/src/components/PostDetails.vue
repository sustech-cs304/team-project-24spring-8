<template>
  <div class="post-details">
    <h1>{{ post ? post.title : "Post Not Found" }}</h1>
    <p v-if="post">{{ post.content }}</p>
    <p v-else>The requested post does not exist or could not be loaded.</p>
    <!-- Enhancing the back link to be consistent with the theme -->
    <router-link to="/posts" class="back-link">返回讨论列表</router-link>
  </div>
</template>

<script>
export default {
  data() {
    return {
      post: null
    };
  },
  created() {
    this.fetchPost(this.$route.params.postId);
  },
  methods: {
    fetchPost(postId) {
      const posts = [
        { id: 1, title: '探讨最近的机器学习讲座', content: '最近在南科大的机器学习讲座非常精彩，讲师从基础到深入...' },
        { id: 2, title: '人工智能与未来社会的讲座回顾', content: '这次讲座主要讨论了人工智能如何影响我们的未来生活...' },
        { id: 3, title: '大数据技术的前景和挑战', content: '大数据技术作为信息时代的产物，它的发展速度和应用范围都在迅速扩大...' }
      ];
      this.post = posts.find(post => post.id.toString() === postId.toString());
    }
  }
}
</script>

<style scoped>
.post-details {
  max-width: 800px;
  margin: 20px auto;
  padding: 20px;
  background: linear-gradient(135deg, #957DAD, #D291BC); /* Purple gradient background */
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  text-align: left;
  color: #FFFFFF; /* White text for better readability */
}

.post-details h1 {
  color: #6A0DAD; /* Deep purple for headers to stand out */
  text-align: center;
  margin-bottom: 20px;
}

p {
  font-size: 16px;
  line-height: 1.6;
}

.back-link {
  display: block;
  text-align: center;
  margin-top: 20px;
  color: #FFFFFF; /* White color text for the link */
  text-decoration: none;
  background-color: #957DAD;
  padding: 10px 15px;
  border-radius: 5px;
  transition: background-color 0.3s;
}

.back-link:hover {
  background-color: #B48B9E; /* Lighter purple on hover for the back link */
  text-decoration: underline;
}
</style>
