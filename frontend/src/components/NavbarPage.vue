<template>
  <div class="navbar">
    <button @click="setCurrentComponent('community')">community</button>
    <button @click="setCurrentComponent('events')">events</button>
    <button @click="setCurrentComponent('recommendations')">recommend</button>
  </div>
</template>

<script>
export default {
  methods: {
    setCurrentComponent(component) {
      this.$emit('update:currentComponent', component); // 触发父组件的事件，更新currentComponent的值
    },
  },
};
</script>

<style>
.navbar {
  display: flex;
  justify-content: space-around;
  align-items: center;
}
</style>
