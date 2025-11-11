<script setup lang="ts">
// Root app component
</script>

<template>
  <div id="app">
    <NuxtPage />
  </div>
</template>

<style>
/* Import global CSS - must be first */
@import '../assets/css/global.css';

/* Additional base styles */
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html, body, #__nuxt, #app {
  height: 100%;
  width: 100%;
}

body {
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, sans-serif;
  background: #0b1220;
  color: #e5e7eb;
}
</style>
