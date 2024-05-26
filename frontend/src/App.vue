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
</style>
