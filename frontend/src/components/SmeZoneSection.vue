<template>
  <div class="space-y-6">
    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center items-center h-64">
      <div class="text-center">
        <div
          class="animate-spin rounded-full h-12 w-12 border-b-2 border-[rgb(var(--color-nepse-primary))] mx-auto mb-4"
        ></div>
        <p class="text-gray-600">Loading SME data...</p>
      </div>
    </div>

    <!-- Error State -->
    <div
      v-else-if="error"
      class="flex flex-col justify-center items-center h-64 text-red-600"
    >
      <div class="text-lg font-semibold mb-2">Error Loading Data</div>
      <div class="text-sm mb-4">{{ error }}</div>
      <button
        @click="fetchSmeData"
        class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
      >
        Retry
      </button>
    </div>

    <!-- Data Display -->
    <div
      v-else
      class="bg-gradient-to-r from-purple-50 to-blue-50 p-6 rounded-xl"
    >
      <h3 class="text-lg font-semibold text-gray-800 mb-4">
        SME Platform Overview
      </h3>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div class="text-center p-4 bg-white rounded-lg">
          <div class="text-2xl font-bold text-purple-600">
            {{ smeStats.totalCompanies }}
          </div>
          <div class="text-sm text-gray-600">Listed Companies</div>
        </div>
        <div class="text-center p-4 bg-white rounded-lg">
          <div class="text-2xl font-bold text-blue-600">
            {{ smeStats.totalVolume }}
          </div>
          <div class="text-sm text-gray-600">Total Volume</div>
        </div>
        <div class="text-center p-4 bg-white rounded-lg">
          <div class="text-2xl font-bold text-green-600">
            {{ smeStats.totalTurnover }}
          </div>
          <div class="text-sm text-gray-600">Total Turnover</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { fetchPriceVolume } from "../services/marketData_enhanced";

const smeStats = ref({
  totalCompanies: 0,
  totalVolume: "0",
  totalTurnover: "Rs. 0",
});
const loading = ref(true);
const error = ref<string | null>(null);

// SME threshold - stocks with turnover below this are considered SME
const SME_TURNOVER_THRESHOLD = 5000000; // 5 million NPR

const fetchSmeData = async () => {
  try {
    loading.value = true;
    error.value = null;

    const allStocks = await fetchPriceVolume();

    // Filter stocks that could be considered SME (lower turnover)
    const smeStocks = allStocks.filter(
      (stock: any) => stock.turnover < SME_TURNOVER_THRESHOLD
    );

    // Calculate aggregated statistics
    const totalCompanies = smeStocks.length;
    const totalVolume = smeStocks.reduce(
      (sum: number, stock: any) => sum + (stock.quantity || 0),
      0
    );
    const totalTurnover = smeStocks.reduce(
      (sum: number, stock: any) => sum + stock.turnover,
      0
    );

    smeStats.value = {
      totalCompanies,
      totalVolume: formatNumber(totalVolume),
      totalTurnover: formatCurrency(totalTurnover),
    };
  } catch (err) {
    console.error("Error fetching SME data:", err);
    error.value = "Failed to load SME data";
  } finally {
    loading.value = false;
  }
};

const formatNumber = (value: number) => {
  if (value >= 1000000) {
    return (value / 1000000).toFixed(1) + "M";
  } else if (value >= 1000) {
    return (value / 1000).toFixed(1) + "K";
  }
  return value.toString();
};

const formatCurrency = (value: number) => {
  if (value >= 10000000) {
    // 1 crore
    return "Rs. " + (value / 10000000).toFixed(1) + "Cr";
  } else if (value >= 100000) {
    // 1 lakh
    return "Rs. " + (value / 100000).toFixed(1) + "L";
  } else {
    return "Rs. " + value.toLocaleString();
  }
};

onMounted(() => {
  fetchSmeData();
});
</script>
