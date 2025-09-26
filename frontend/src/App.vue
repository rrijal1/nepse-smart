<template>
  <div id="app">
    <Header />
    <main class="container mx-auto px-4 py-6">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
import Header from "./components/Header.vue";
</script>
