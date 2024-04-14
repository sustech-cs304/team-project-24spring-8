<template>
  <div class="post-list">
    <h1>南科大计算机系讲座讨论</h1>
    <ul>
      <li v-for="post in posts" :key="post.id" class="post-item">
        <router-link :to="{ name: 'PostDetails', params: { postId: post.id.toString() }}" class="post-link">{{ post.title }}</router-link>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  data() {
    return {
      posts: [
        { id: 1, title: '探讨最近的机器学习讲座' },
        { id: 2, title: '人工智能与未来社会的讲座回顾' },
        { id: 3, title: '大数据技术的前景和挑战' }
      ]
    };
  }
}
</script>

<style scoped>
.post-list {
  max-width: 800px;
  margin: 20px auto;
  padding: 20px;
  background: linear-gradient(135deg, #957DAD, #D291BC); /* Updated background to a purple gradient */
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.post-list h1 {
  color: #6A0DAD; /* Deep purple color for the heading */
  text-align: center;
  margin-bottom: 20px; /* Added margin for better spacing */
}

.post-list ul {
  list-style: none;
  padding: 0;
}

.post-list li {
  margin: 10px 0;
  transition: all 0.3s ease;
}

.post-item {
  border-bottom: 1px solid #eee;
  padding: 10px;
  transition: background-color 0.3s ease;
}

.post-item:last-child {
  border-bottom: none;
}

.post-link {
  text-decoration: none;
  color: #5E2D79; /* A lighter shade of purple for links to make them stand out */
  font-size: 18px;
  display: block;
  transition: color 0.3s ease;
}

.post-link:hover {
  color: #9A4DCE; /* A lighter, more vivid purple for hover */
  text-decoration: underline;
}

.post-item:hover {
  background-color: #f4eaff; /* A very light purple background on hover for list items */
}
</style>
