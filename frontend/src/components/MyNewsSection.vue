<template>
  <div class="space-y-6">
    <!-- Filter Tabs -->
    <div class="flex items-center gap-4 mb-6">
      <div class="flex bg-gray-100 rounded-lg p-1">
        <button
          v-for="filter in newsFilters"
          :key="filter"
          @click="activeNewsFilter = filter"
          :class="[
            'px-4 py-2 rounded-md text-sm font-medium transition-colors',
            activeNewsFilter === filter
              ? 'bg-white text-[rgb(var(--color-nepse-primary))] shadow-sm'
              : 'text-gray-600 hover:text-gray-900',
          ]"
        >
          {{ filter }}
        </button>
      </div>
    </div>

    <!-- News Cards -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div
        v-for="news in filteredNews"
        :key="news.id"
        class="bg-white border border-gray-200 rounded-xl p-6 hover:shadow-md transition-shadow cursor-pointer"
      >
        <div class="flex items-start justify-between mb-4">
          <div class="flex items-center gap-2">
            <span
              :class="[
                'px-2 py-1 rounded-full text-xs font-medium',
                news.priority === 'high'
                  ? 'bg-red-100 text-red-800'
                  : news.priority === 'medium'
                  ? 'bg-yellow-100 text-yellow-800'
                  : 'bg-gray-100 text-gray-800',
              ]"
            >
              {{ news.category }}
            </span>
            <span class="text-xs text-gray-500">{{ news.time }}</span>
          </div>
          <NewsIcon class="w-5 h-5 text-gray-400" />
        </div>
        <h3 class="font-semibold text-gray-800 mb-2">{{ news.title }}</h3>
        <p class="text-gray-600 text-sm mb-4">{{ news.excerpt }}</p>
        <div class="flex items-center justify-between">
          <span class="text-xs text-gray-500">{{ news.source }}</span>
          <button
            class="text-[rgb(var(--color-nepse-primary))] text-sm font-medium hover:underline"
          >
            Read More →
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from "vue";
import NewsIcon from "./icons/NewsIcon.vue";

const activeNewsFilter = ref("All");

const newsFilters = [
  "All",
  "My Stocks",
  "Banking",
  "Insurance",
  "Hydropower",
  "Finance",
];

const newsItems = reactive([
  {
    id: 1,
    title: "NABIL Bank Reports Strong Q3 Results",
    excerpt: "Net profit increased by 18% compared to previous quarter...",
    category: "Banking",
    priority: "high",
    source: "Company Report",
    time: "2 hours ago",
  },
  {
    id: 2,
    title: "Hydropower Sector Gets Government Support",
    excerpt: "New policy framework announced to boost renewable energy...",
    category: "Hydropower",
    priority: "medium",
    source: "Government News",
    time: "4 hours ago",
  },
  {
    id: 3,
    title: "SCBL Announces Dividend Distribution",
    excerpt: "Board recommends 15% bonus shares for shareholders...",
    category: "Banking",
    priority: "high",
    source: "Corporate Action",
    time: "6 hours ago",
  },
  {
    id: 4,
    title: "Market Analysis: Banking Sector Outlook",
    excerpt: "Expert analysis suggests continued growth in banking sector...",
    category: "Analysis",
    priority: "low",
    source: "Market Analysis",
    time: "8 hours ago",
  },
]);

const watchlistStocks = reactive([
  {
    symbol: "NABIL",
    ltp: 1235,
    change: 45,
    changePercent: 3.78,
    volume: "2.3M",
    holdings: 100,
    avgPrice: 1180,
    favorite: true,
  },
  {
    symbol: "SCBL",
    ltp: 567,
    change: -12,
    changePercent: -2.07,
    volume: "1.8M",
    holdings: 0,
    avgPrice: 0,
    favorite: false,
  },
]);

const filteredNews = computed(() => {
  if (activeNewsFilter.value === "All") return newsItems;
  if (activeNewsFilter.value === "My Stocks") {
    const myStockSymbols = watchlistStocks
      .filter((s) => s.holdings > 0)
      .map((s) => s.symbol);
    return newsItems.filter((news) =>
      myStockSymbols.some((symbol) => news.title.includes(symbol))
    );
  }
  return newsItems.filter((news) => news.category === activeNewsFilter.value);
});
</script>
