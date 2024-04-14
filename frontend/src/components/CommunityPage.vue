<template>
    <div class="community-page">
      <h2>Community</h2>
      <PostList v-if="!selectedPost" :posts="posts" @selectPost="showPostDetails" />
      
      <PostDetails v-if="selectedPost" :post="selectedPost" @back="clearSelectedPost" />
    </div>
  </template>
  
  <script>
  import PostList from './PostList.vue';
  import PostDetails from './PostDetails.vue';
  
  export default {
    components: {
      PostList,
      PostDetails,
    },
    data() {
      return {
        posts: [
          { id: 1, title: 'Post1', content: 'Content1' },
          { id: 2, title: 'Post2', content: 'Content2' },
        ],
        selectedPost: null,
      };
    },
    methods: {
      showPostDetails(post) {
        this.selectedPost = post;
      },
      clearSelectedPost() {
        this.selectedPost = null;
      },
    },
  };
  </script>
  
  <style>
  .community-page {
  }
  </style>
  