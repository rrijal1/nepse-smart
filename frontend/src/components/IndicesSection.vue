<template>
  <div class="space-y-6">
    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center items-center h-64">
      <div class="text-center">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-[rgb(var(--color-nepse-primary))] mx-auto mb-4"></div>
        <p class="text-gray-600">Loading indices data...</p>
      </div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="flex flex-col justify-center items-center h-64 text-red-600">
      <div class="text-lg font-semibold mb-2">Error Loading Data</div>
      <div class="text-sm mb-4">{{ error }}</div>
      <button
        @click="fetchIndicesData"
        class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
      >
        Retry
      </button>
    </div>

    <!-- Data Display -->
    <div v-else>
      <!-- NEPSE Main Indices -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
        <div
          v-for="index in mainIndices"
          :key="index.index_name"
          class="bg-white p-6 rounded-xl shadow-sm border hover:shadow-md transition-shadow"
        >
          <div class="flex items-center justify-between mb-4">
            <h3 class="font-semibold text-gray-800">{{ index.index_name }}</h3>
            <span
              :class="[
                'px-2 py-1 rounded-full text-xs font-medium',
                index.change >= 0
                  ? 'bg-green-100 text-green-800'
                  : 'bg-red-100 text-red-800',
              ]"
            >
              {{ index.change >= 0 ? "+" : "" }}{{ index.change_percent }}%
            </span>
          </div>
          <div class="space-y-2 text-sm">
            <div class="flex justify-between">
              <span class="text-gray-600">Current:</span>
              <span class="font-mono font-semibold">{{ index.current_value.toLocaleString() }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">Change:</span>
              <span
                :class="[
                  'font-mono font-semibold',
                  index.change >= 0 ? 'text-green-600' : 'text-red-600',
                ]"
              >
                {{ index.change >= 0 ? "+" : "" }}{{ index.change }}
              </span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">High:</span>
              <span class="font-mono">{{ index.high.toLocaleString() }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">Low:</span>
              <span class="font-mono">{{ index.low.toLocaleString() }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">Turnover:</span>
              <span class="font-mono text-xs">{{ (index.turnover / 10000000).toFixed(1) }} Cr</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Sector Indices -->
      <div class="bg-white p-6 rounded-xl shadow-sm border">
        <h3 class="text-lg font-semibold text-gray-800 mb-4">Sector Indices</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div
            v-for="sector in sectorIndices"
            :key="sector.index_name"
            class="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
          >
            <div class="flex items-center justify-between mb-2">
              <span class="font-medium text-gray-800 text-sm">{{ sector.index_name }}</span>
              <span
                :class="[
                  'px-2 py-1 rounded-full text-xs font-medium',
                  sector.change >= 0
                    ? 'bg-green-100 text-green-800'
                    : 'bg-red-100 text-red-800',
                ]"
              >
                {{ sector.change >= 0 ? "+" : "" }}{{ sector.change_percent }}%
              </span>
            </div>
            <div class="space-y-1 text-xs">
              <div class="flex justify-between">
                <span class="text-gray-600">Current:</span>
                <span class="font-mono font-semibold">{{ sector.current_value.toLocaleString() }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600">Change:</span>
                <span
                  :class="[
                    'font-mono font-semibold',
                    sector.change >= 0 ? 'text-green-600' : 'text-red-600',
                  ]"
                >
                  {{ sector.change >= 0 ? "+" : "" }}{{ sector.change }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { fetchNepseIndex, fetchSubIndices } from "../services/marketData_enhanced";

const mainIndices = ref<any[]>([]);
const sectorIndices = ref<any[]>([]);
const loading = ref(true);
const error = ref<string | null>(null);

const fetchIndicesData = async () => {
  try {
    loading.value = true;
    error.value = null;

    // Fetch main NEPSE indices
    const nepseData = await fetchNepseIndex();
    mainIndices.value = [
      nepseData.nepse_index,
      nepseData.sensitive_index,
      nepseData.float_index,
    ];

    // Fetch sector indices
    sectorIndices.value = await fetchSubIndices();

  } catch (err) {
    console.error("Error fetching indices data:", err);
    error.value = "Failed to load indices data";
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchIndicesData();
});
</script>
