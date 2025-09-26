<template>
  <div class="space-y-6">
    <div class="bg-white rounded-lg shadow p-6">
      <h2 class="text-2xl font-bold text-gray-800 mb-4">Market Summary</h2>
      <div v-if="loading" class="text-center py-4">
        <div
          class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-nepse-primary"
        ></div>
        <p class="mt-2 text-gray-600">Loading market data...</p>
      </div>
      <div v-else-if="error" class="text-center py-4 text-bear-red">
        <p>Error loading data: {{ error }}</p>
        <button
          @click="fetchData"
          class="mt-2 px-4 py-2 bg-nepse-primary text-white rounded hover:bg-blue-700"
        >
          Retry
        </button>
      </div>
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div
          v-for="item in marketSummary"
          :key="item.detail"
          class="text-center p-4 bg-gray-50 rounded"
        >
          <h3 class="font-semibold text-gray-700">{{ item.detail }}</h3>
          <p
            class="text-2xl font-bold mt-2"
            :class="getValueColor(item.detail, item.value)"
          >
            {{ formatValue(item.detail, item.value) }}
          </p>
        </div>
      </div>
    </div>

    <div class="bg-white rounded-lg shadow p-6">
      <h2 class="text-2xl font-bold text-gray-800 mb-4">Top Gainers</h2>
      <div v-if="topGainers.length > 0" class="overflow-x-auto">
        <table class="min-w-full">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-4 py-2 text-left">Symbol</th>
              <th class="px-4 py-2 text-right">LTP</th>
              <th class="px-4 py-2 text-right">Change</th>
              <th class="px-4 py-2 text-right">% Change</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="stock in topGainers.slice(0, 10)"
              :key="stock.symbol"
              class="border-t"
            >
              <td class="px-4 py-2 font-semibold">{{ stock.symbol }}</td>
              <td class="px-4 py-2 text-right font-mono">{{ stock.ltp }}</td>
              <td class="px-4 py-2 text-right font-mono text-bull-green">
                +{{ stock.pointChange }}
              </td>
              <td class="px-4 py-2 text-right font-mono text-bull-green">
                +{{ stock.percentageChange }}%
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="bg-white rounded-lg shadow p-6">
      <h2 class="text-2xl font-bold text-gray-800 mb-4">Top Losers</h2>
      <div v-if="topLosers.length > 0" class="overflow-x-auto">
        <table class="min-w-full">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-4 py-2 text-left">Symbol</th>
              <th class="px-4 py-2 text-right">LTP</th>
              <th class="px-4 py-2 text-right">Change</th>
              <th class="px-4 py-2 text-right">% Change</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="stock in topLosers.slice(0, 10)"
              :key="stock.symbol"
              class="border-t"
            >
              <td class="px-4 py-2 font-semibold">{{ stock.symbol }}</td>
              <td class="px-4 py-2 text-right font-mono">{{ stock.ltp }}</td>
              <td class="px-4 py-2 text-right font-mono text-bear-red">
                {{ stock.pointChange }}
              </td>
              <td class="px-4 py-2 text-right font-mono text-bear-red">
                {{ stock.percentageChange }}%
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import axios from "axios";

// Types
interface MarketSummaryItem {
  detail: string;
  value: string | number;
}

interface Stock {
  symbol: string;
  ltp: number;
  pointChange: number;
  percentageChange: number;
}

// Reactive data
const loading = ref(true);
const error = ref("");
const marketSummary = ref<MarketSummaryItem[]>([]);
const topGainers = ref<Stock[]>([]);
const topLosers = ref<Stock[]>([]);

// Methods
const fetchData = async () => {
  loading.value = true;
  error.value = "";

  try {
    // Fetch data from our FastAPI backend
    const [summaryRes, gainersRes, losersRes] = await Promise.all([
      axios.get("/api/summary"),
      axios.get("/api/top-gainers"),
      axios.get("/api/top-losers"),
    ]);

    marketSummary.value = summaryRes.data;
    topGainers.value = gainersRes.data;
    topLosers.value = losersRes.data;
  } catch (err: any) {
    error.value = err.message || "Failed to fetch data";
    console.error("Error fetching data:", err);
  } finally {
    loading.value = false;
  }
};

const getValueColor = (detail: string, value: string | number): string => {
  const detailLower = detail.toLowerCase();
  if (detailLower.includes("change") || detailLower.includes("difference")) {
    const numValue = typeof value === "string" ? parseFloat(value) : value;
    if (numValue > 0) return "text-bull-green";
    if (numValue < 0) return "text-bear-red";
  }
  return "text-gray-800";
};

const formatValue = (detail: string, value: string | number): string => {
  if (typeof value === "number") {
    if (
      detail.toLowerCase().includes("change") ||
      detail.toLowerCase().includes("difference")
    ) {
      return value > 0 ? `+${value}` : value.toString();
    }
    return value.toLocaleString();
  }
  return value;
};

// Lifecycle
onMounted(() => {
  fetchData();
});
</script>
