<!-- /**
* AI-generated-content
* tool: ChatGPT
* version: 4
* usage: Make sure home page can work properly on different browsers.
*/ -->
<template>
  <div>
    <!-- <h1>{{ title }}</h1> -->
    <video ref="homeVideo" class="home-video" autoplay muted>
      <source src="../assets/demo.mp4" type="video/mp4">
      Your browser does not support the video tag.
    </video>
    <!-- <button @click="toggleFullScreen" class="fullscreen-button">
      {{ isFullScreen ? 'Exit Full Screen' : 'Play Full Screen' }}
    </button> -->
  </div>
</template>

<script>
export default {
  data() {
    return {
      title: "Welcome to SUSTech Center",
      isFullScreen: false
    };
  },
  methods: {
    toggleFullScreen() {
      const videoElement = this.$refs.homeVideo;
      if (!this.isFullScreen) {
        if (videoElement.requestFullscreen) {
          videoElement.requestFullscreen();
        } else if (videoElement.mozRequestFullScreen) { // Firefox
          videoElement.mozRequestFullScreen();
        } else if (videoElement.webkitRequestFullscreen) { // Chrome, Safari, and Opera
          videoElement.webkitRequestFullscreen();
        } else if (videoElement.msRequestFullscreen) { // IE/Edge
          videoElement.msRequestFullscreen();
        }
      } else {
        if (document.exitFullscreen) {
          document.exitFullscreen();
        } else if (document.mozCancelFullScreen) { // Firefox
          document.mozCancelFullScreen();
        } else if (document.webkitExitFullscreen) { // Chrome, Safari, and Opera
          document.webkitExitFullscreen();
        } else if (document.msExitFullscreen) { // IE/Edge
          document.msExitFullscreen();
        }
      }
      this.isFullScreen = !this.isFullScreen;
    }
  }
}
</script>

<style scoped>
@font-face {
  font-family: "zql";
  src: url("../assets/font/zql.woff2") format("woff2");
}

.home-video {
  width: 100%;
  height: auto;
}

.fullscreen-button {
  margin-top: 20px;
  padding: 10px 20px;
  font-size: 16px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.fullscreen-button:hover {
  background-color: #0056b3;
}
</style>
