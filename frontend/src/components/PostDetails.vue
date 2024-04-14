<template>
  <div class="post-details">
    <h1>{{ post ? post.title : "Post Not Found" }}</h1>
    <p v-if="post">{{ post.content }}</p>
    <p v-else>The requested post does not exist or could not be loaded.</p>
    <!-- Ensuring the router-link is correctly pointed to the posts list -->
    <router-link to="/posts">返回讨论列表</router-link>
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
      // Simulated API call to fetch post details
      const posts = [
        { id: 1, title: '探讨最近的机器学习讲座', content: '最近在南科大的机器学习讲座非常精彩，讲师从基础到深入...' },
        { id: 2, title: '人工智能与未来社会的讲座回顾', content: '这次讲座主要讨论了人工智能如何影响我们的未来生活...' },
        { id: 3, title: '大数据技术的前景和挑战', content: '大数据技术作为信息时代的产物，它的发展速度和应用范围都在迅速扩大...' }
      ];
      // Ensure postId is converted to a string to match string type ids if necessary
      this.post = posts.find(post => post.id.toString() === postId.toString());
    }
  }
}
</script>

<style scoped>
.post-details {
  border: 1px solid #eee;
  padding: 20px;
  border-radius: 10px;
}
.post-details h1 {
  color: #333;
}
</style>
