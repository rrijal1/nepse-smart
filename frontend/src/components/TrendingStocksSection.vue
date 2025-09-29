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
import { ref, reactive, onMounted } from "vue";
import { fetchTopGainers, fetchTopLosers } from "../services/marketData";
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

  console.log("Gainers:", gainers);
  console.log("Losers:", losers);

  if (gainers.length > 0) {
    topGainers.splice(0, topGainers.length, ...gainers.slice(0, 8));
  }
  else {
    // Keep using sample data if API is not available
    topGainers.splice(0, topGainers.length, 
        ...[{ symbol: "NABIL", ltp: 1235, pointChange: 45, percentageChange: 3.78 }, { symbol: "SCBL", ltp: 567, pointChange: 23, percentageChange: 4.23 }, { symbol: "HBL", ltp: 689, pointChange: 28, percentageChange: 4.24 }, { symbol: "EBL", ltp: 890, pointChange: 35, percentageChange: 4.09 }, { symbol: "BOKL", ltp: 345, pointChange: 15, percentageChange: 4.55 }, { symbol: "MBL", ltp: 456, pointChange: 18, percentageChange: 4.11 }, { symbol: "CBL", ltp: 278, pointChange: 11, percentageChange: 4.12 }, { symbol: "PRVU", ltp: 567, pointChange: 22, percentageChange: 4.04 }]
    );
  }

  if (losers.length > 0) {
    topLosers.splice(0, topLosers.length, ...losers.slice(0, 8));
  }
  else {
    // Keep using sample data if API is not available
    topLosers.splice(0, topLosers.length, 
        ...[{ symbol: "UPPER", ltp: 456, pointChange: -23, percentageChange: -4.79 }, { symbol: "CHCL", ltp: 567, pointChange: -28, percentageChange: -4.7 }, { symbol: "AKPL", ltp: 234, pointChange: -12, percentageChange: -4.88 }, { symbol: "UMHL", ltp: 345, pointChange: -17, percentageChange: -4.69 }, { symbol: "NYADI", ltp: 789, pointChange: -38, percentageChange: -4.59 }, { symbol: "KKHC", ltp: 123, pointChange: -6, percentageChange: -4.65 }, { symbol: "RHPL", ltp: 456, pointChange: -22, percentageChange: -4.61 }, { symbol: "SHEL", ltp: 234, pointChange: -11, percentageChange: -4.49 }]
    );
  }
  loading.value = false;
};

// Initialize data on component mount
onMounted(() => {
  fetchMarketData();
});
</script>
