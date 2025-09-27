<template>
  <header class="bg-[rgb(var(--color-nepse-primary))] text-white shadow-lg">
    <div class="container mx-auto px-4 py-4">
      <div class="flex items-center justify-between">
        <h1 class="text-2xl font-bold">NEPSE Analytics</h1>
        <nav class="flex space-x-4">
          <router-link
            to="/"
            class="text-white hover:text-gray-200 px-3 py-2 rounded transition-colors"
            :class="{ 'bg-white/20': $route.path === '/' }"
          >
            Market
          </router-link>
          <router-link
            to="/trading"
            class="text-white hover:text-gray-200 px-3 py-2 rounded transition-colors"
            :class="{ 'bg-white/20': $route.path === '/trading' }"
          >
            Trading
          </router-link>
          <router-link
            to="/portfolio"
            class="text-white hover:text-gray-200 px-3 py-2 rounded transition-colors"
            :class="{ 'bg-white/20': $route.path === '/portfolio' }"
          >
            Portfolio
          </router-link>
        </nav>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
// Simple header component
</script>
