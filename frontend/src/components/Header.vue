<template>
  <header class="bg-[rgb(var(--color-nepse-primary))] text-white shadow-lg">
    <div class="container mx-auto px-4 py-4">
      <div class="flex items-center justify-between">
        <router-link
          to="/"
          class="text-2xl font-bold hover:text-gray-200 transition-colors"
          >NEPSE Analytics</router-link
        >
        <nav class="flex space-x-1">
          <router-link
            to="/"
            class="text-white hover:text-gray-200 px-4 py-2 rounded-lg transition-all duration-200 font-medium flex items-center gap-2"
            :class="{
              'bg-white/20 shadow-sm':
                $route.path === '/' || $route.path.startsWith('/market'),
            }"
          >
            <svg
              class="w-5 h-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z"
              />
            </svg>
            Market
          </router-link>
          <router-link
            to="/analytics"
            class="text-white hover:text-gray-200 px-4 py-2 rounded-lg transition-all duration-200 font-medium flex items-center gap-2"
            :class="{
              'bg-white/20 shadow-sm': $route.path.startsWith('/analytics'),
            }"
          >
            <svg
              class="w-5 h-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
              />
            </svg>
            Analytics
          </router-link>
          <router-link
            to="/my-corner"
            class="text-white hover:text-gray-200 px-4 py-2 rounded-lg transition-all duration-200 font-medium flex items-center gap-2"
            :class="{
              'bg-white/20 shadow-sm': $route.path.startsWith('/my-corner'),
            }"
          >
            <svg
              class="w-5 h-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
              />
            </svg>
            My Corner
          </router-link>
          <router-link
            to="/agent"
            class="text-white hover:text-gray-200 px-4 py-2 rounded-lg transition-all duration-200 font-medium flex items-center gap-2"
            :class="{
              'bg-white/20 shadow-sm': $route.path.startsWith('/agent'),
            }"
          >
            <svg
              class="w-5 h-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"
              />
            </svg>
            Agent
          </router-link>
        </nav>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
// Simple header component
</script>
