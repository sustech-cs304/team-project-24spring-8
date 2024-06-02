<template>
  <div id="app">
    <Navbar />   <!-- 引入导航栏 -->
    <router-view></router-view>  <!-- 页面内容 -->
  </div>
</template>

<script>
// 引入 Navbar 组件
import Navbar from './components/NavbarPage.vue';

export default {
  name: 'App',
  components: {
    Navbar
  }
}
</script>

<style>
/* 这里可以添加你的全局样式 */
#app {
  background-color: #f4f6f9; /* 你想要的背景颜色 */
  min-height: 100vh; /* 确保背景颜色覆盖整个视口高度 */
}
</style>
