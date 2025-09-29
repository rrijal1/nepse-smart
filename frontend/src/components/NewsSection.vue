<template>
  <div class="space-y-6">
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div
        v-for="news in newsItems"
        :key="news.id"
        class="bg-white p-6 rounded-xl shadow-sm border hover:shadow-md transition-shadow cursor-pointer"
      >
        <div class="flex items-start gap-4">
          <div
            class="w-2 h-2 bg-[rgb(var(--color-nepse-primary))] rounded-full mt-2 flex-shrink-0"
          ></div>
          <div class="flex-1">
            <h3 class="font-semibold text-gray-800 mb-2">
              {{ news.title }}
            </h3>
            <p class="text-gray-600 text-sm mb-3">{{ news.excerpt }}</p>
            <div
              class="flex items-center justify-between text-xs text-gray-500"
            >
              <span>{{ news.source }}</span>
              <span>{{ news.time }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive } from "vue";

const newsItems = reactive([
  {
    id: 1,
    title: "NEPSE Index Crosses 2,150 Mark",
    excerpt: "The benchmark index gained 0.30% in today's trading session...",
    source: "Market Report",
    time: "2 hours ago",
  },
  {
    id: 2,
    title: "Banking Sector Shows Mixed Performance",
    excerpt:
      "While some banks posted gains, overall sector declined by 0.67%...",
    source: "Sector Analysis",
    time: "3 hours ago",
  },
  {
    id: 3,
    title: "Hydropower Stocks Rally Continues",
    excerpt:
      "Hydropower sector gained 1.04% led by strong performance in major stocks...",
    source: "Energy News",
    time: "4 hours ago",
  },
  {
    id: 4,
    title: "New IPO Announcement Expected",
    excerpt:
      "Sources suggest a major company may announce IPO plans next week...",
    source: "IPO Updates",
    time: "5 hours ago",
  },
]);
</script>
