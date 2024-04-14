<template>
    <div class="post-details">
      <h3>{{ post.title }}</h3>
      <p>{{ post.content }}</p>
      <button @click="$emit('back')">返回</button>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      post: {
        type: Object,
        required: true,
      },
    },
  };
  </script>
  
  <style>
  /* 样式 */
  </style>
  