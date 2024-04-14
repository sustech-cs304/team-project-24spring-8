<template>
    <div class="post-list">
      <h3>PostList</h3>
      <ul>
        <li v-for="post in posts" :key="post.id" @click="selectPost(post)">
          {{ post.title }}
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      posts: {
        type: Array,
        required: true,
      },
    },
    methods: {
      selectPost(post) {
        this.$emit('selectPost', post);
      },
    },
  };
  </script>
  
  <style>
  /* 样式 */
  </style>
  