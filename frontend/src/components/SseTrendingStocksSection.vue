<template>
  <div v-if="loading" class="flex justify-center items-center h-64">
    <Spinner />
  </div>
  <div v-else class="space-y-6">
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Top Gainers -->
      <div
        class="bg-gradient-to-br from-green-50 to-white p-6 rounded-xl shadow-sm border"
      >
        <h3
          class="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2"
        >
          <TrendingUpIcon class="w-5 h-5 text-green-600" />
          Top Gainers (Real-time)
        </h3>
        <div class="space-y-3">
          <div
            v-for="stock in topGainers"
            :key="stock.symbol"
            class="flex items-center justify-between p-3 bg-white rounded-lg shadow-sm"
          >
            <div>
              <span class="font-semibold text-gray-800">{{
                stock.symbol
              }}</span>
              <div class="text-sm text-gray-600">{{ stock.ltp }}</div>
            </div>
            <div class="text-right">
              <div class="text-green-600 font-semibold">
                +{{ stock.percentageChange }}%
              </div>
              <div class="text-sm text-gray-600">
                +{{ stock.pointChange }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Top Losers -->
      <div
        class="bg-gradient-to-br from-red-50 to-white p-6 rounded-xl shadow-sm border"
      >
        <h3
          class="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2"
        >
          <TrendingDownIcon class="w-5 h-5 text-red-600" />
          Top Losers (Real-time)
        </h3>
        <div class="space-y-3">
          <div
            v-for="stock in topLosers"
            :key="stock.symbol"
            class="flex items-center justify-between p-3 bg-white rounded-lg shadow-sm"
          >
            <div>
              <span class="font-semibold text-gray-800">{{
                stock.symbol
              }}</span>
              <div class="text-sm text-gray-600">{{ stock.ltp }}</div>
            </div>
            <div class="text-right">
              <div class="text-red-600 font-semibold">
                {{ stock.percentageChange }}%
              </div>
              <div class="text-sm text-gray-600">
                {{ stock.pointChange }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, onUnmounted } from "vue";
import TrendingUpIcon from "./icons/TrendingUpIcon.vue";
import TrendingDownIcon from "./icons/TrendingDownIcon.vue";
import Spinner from "./Spinner.vue";

const loading = ref(true);
const topGainers = reactive<any[]>([]);
const topLosers = reactive<any[]>([]);

let eventSource: EventSource;

onMounted(() => {
  eventSource = new EventSource("/api/trending-stocks-sse");

  eventSource.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.error) {
      console.error("SSE Error:", data.error);
      return;
    }

    if (data.gainers && data.gainers.length > 0) {
      topGainers.splice(0, topGainers.length, ...data.gainers.slice(0, 8));
    }

    if (data.losers && data.losers.length > 0) {
      topLosers.splice(0, topLosers.length, ...data.losers.slice(0, 8));
    }

    if (loading.value) {
      loading.value = false;
    }
  };

  eventSource.onerror = (error) => {
    console.error("EventSource failed:", error);
    eventSource.close();
  };
});

onUnmounted(() => {
  if (eventSource) {
    eventSource.close();
  }
});
</script>
