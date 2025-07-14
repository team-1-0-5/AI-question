<script setup lang="ts">
  import SpeakerHome from './pages/SpeakerHome.vue';
</script>

<template>
  <div class="fullscreen-container" style="margin: 0; padding: 0;">
    <SpeakerHome />
  </div>
</template>

<style>
html, body {
  margin: 0;
  padding: 0;
  height: 100%;
  width: 100%;
  overflow: hidden;
  background: #f8f9fb;
  font-family: 'Segoe UI', 'PingFang SC', 'Hiragino Sans', Arial, sans-serif;
}

#app {
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: column;
  padding: 0;
}
</style>
