<template>
  <div class="home-container">
    <h1>{{ title }}</h1>
    <!-- <video class="home-video" controls>
      <source src="../assets/video/home-video.mp4" type="video/mp4">
      Your browser does not support the video tag.
    </video> -->
    <router-link to="/posts" class="back-link">进入讨论列表</router-link>
  </div>
</template>

<script>
export default {
  data() {
    return {
      title: "Welcome to SUSTech Center"
    };
  }
}
</script>

<style scoped>
@font-face {
  font-family: "zql";
  src: url("../assets/font/zql.woff2") format("woff2");
}

.home-container {
  font-family: "zql";
  width: 95%;
  max-width: 800px;
  margin: 20px auto;
  padding: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.home-container h1 {
  color: #34495e;
  font-size: 24px;
  margin-bottom: 20px;
}

.home-video {
  width: 100%;
  height: auto;
  margin-bottom: 20px;
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
</style>
