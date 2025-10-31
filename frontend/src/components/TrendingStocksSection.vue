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
          Top Gainers
        </h3>
        <div class="space-y-3">
          <div
            v-for="stock in topGainers.slice(0, 8)"
            :key="stock.symbol"
            class="flex items-center justify-between p-3 bg-white rounded-lg shadow-sm"
          >
            <div>
              <span class="font-semibold text-gray-800">{{
                stock.symbol
              }}</span>
              <div class="text-sm text-gray-600">
                {{ formatNumber(stock.close) }}
              </div>
            </div>
            <div class="text-right">
              <div class="text-green-600 font-semibold">
                {{ formatPercentage(stock.change_percent) }}
              </div>
              <div class="text-sm text-gray-600">
                +{{ formatNumber(stock.change) }}
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
          Top Losers
        </h3>
        <div class="space-y-3">
          <div
            v-for="stock in topLosers.slice(0, 8)"
            :key="stock.symbol"
            class="flex items-center justify-between p-3 bg-white rounded-lg shadow-sm"
          >
            <div>
              <span class="font-semibold text-gray-800">{{
                stock.symbol
              }}</span>
              <div class="text-sm text-gray-600">
                {{ formatNumber(stock.close) }}
              </div>
            </div>
            <div class="text-right">
              <div class="text-red-600 font-semibold">
                {{ formatPercentage(stock.change_percent) }}
              </div>
              <div class="text-sm text-gray-600">
                {{ formatNumber(stock.change) }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from "vue";
import {
  fetchTopGainers,
  fetchTopLosers,
} from "../services/marketData_enhanced";
import TrendingUpIcon from "./icons/TrendingUpIcon.vue";
import TrendingDownIcon from "./icons/TrendingDownIcon.vue";
import Spinner from "./Spinner.vue";

const loading = ref(true);
const topGainers = reactive<any[]>([]);
const topLosers = reactive<any[]>([]);

// Fetch real data from backend
const fetchMarketData = async () => {
  loading.value = true;
  const gainers = await fetchTopGainers();
  const losers = await fetchTopLosers();

  if (gainers.length > 0) {
    topGainers.splice(0, topGainers.length, ...gainers.slice(0, 8));
  } else {
    // Keep using sample data if API is not available
    topGainers.splice(
      0,
      topGainers.length,
      ...[
        { symbol: "NABIL", close: 1235, change: 45, change_percent: 3.78 },
        { symbol: "SCBL", close: 567, change: 23, change_percent: 4.23 },
        { symbol: "HBL", close: 689, change: 28, change_percent: 4.24 },
        { symbol: "EBL", close: 890, change: 35, change_percent: 4.09 },
        { symbol: "BOKL", close: 345, change: 15, change_percent: 4.55 },
        { symbol: "MBL", close: 456, change: 18, change_percent: 4.11 },
        { symbol: "CBL", close: 278, change: 11, change_percent: 4.12 },
        { symbol: "PRVU", close: 567, change: 22, change_percent: 4.04 },
      ]
    );
  }

  if (losers.length > 0) {
    topLosers.splice(0, topLosers.length, ...losers.slice(0, 8));
  } else {
    // Keep using sample data if API is not available
    topLosers.splice(
      0,
      topLosers.length,
      ...[
        { symbol: "UPPER", close: 456, change: -23, change_percent: -4.79 },
        { symbol: "CHCL", close: 567, change: -28, change_percent: -4.7 },
        { symbol: "AKPL", close: 234, change: -12, change_percent: -4.88 },
        { symbol: "UMHL", close: 345, change: -17, change_percent: -4.69 },
        { symbol: "NYADI", close: 789, change: -38, change_percent: -4.59 },
        { symbol: "KKHC", close: 123, change: -6, change_percent: -4.65 },
        { symbol: "RHPL", close: 456, change: -22, change_percent: -4.61 },
        { symbol: "SHEL", close: 234, change: -11, change_percent: -4.49 },
      ]
    );
  }
  loading.value = false;
};

// Initialize data on component mount
onMounted(() => {
  fetchMarketData();
});

// Format percentage to 2 decimal places
const formatPercentage = (value: number) => {
  if (value === null || value === undefined) return "0.00%";
  const sign = value >= 0 ? "+" : "";
  return `${sign}${value.toFixed(2)}%`;
};

// Format number to 2 decimal places
const formatNumber = (value: number) => {
  if (value === null || value === undefined) return "0.00";
  return value.toFixed(2);
};
</script>
