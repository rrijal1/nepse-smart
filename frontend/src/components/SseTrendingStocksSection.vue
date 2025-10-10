<template>
  <div v-if="loading" class="flex justify-center items-center h-64">
    <Spinner />
  </div>
  <div
    v-else-if="error"
    class="flex flex-col justify-center items-center h-64 text-red-600"
  >
    <div class="text-lg font-semibold mb-2">Connection Error</div>
    <div class="text-sm mb-4">{{ error }}</div>
    <button
      @click="reconnect"
      class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
    >
      Retry Connection
    </button>
  </div>
  <div v-else class="space-y-6">
    <!-- Connection Status Bar -->
    <div
      class="flex items-center justify-between p-3 bg-gray-50 rounded-lg border"
    >
      <div class="flex items-center gap-2">
        <div
          :class="[
            'w-3 h-3 rounded-full transition-colors',
            connectionStatus === 'connected'
              ? 'bg-green-500'
              : connectionStatus === 'connecting'
              ? 'bg-yellow-500 animate-pulse'
              : 'bg-red-500',
          ]"
        ></div>
        <span class="text-sm font-medium text-gray-700">
          {{ statusText }}
        </span>
      </div>
      <div v-if="lastUpdate" class="text-xs text-gray-500">
        Last update: {{ formatTime(lastUpdate) }}
      </div>
    </div>

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
          <StockItem
            v-for="stock in topGainers"
            :key="stock.symbol"
            :stock="stock"
            :is-gainer="true"
          />
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
          <StockItem
            v-for="stock in topLosers"
            :key="stock.symbol"
            :stock="stock"
            :is-gainer="false"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from "vue";
import TrendingUpIcon from "./icons/TrendingUpIcon.vue";
import TrendingDownIcon from "./icons/TrendingDownIcon.vue";
import Spinner from "./Spinner.vue";
import StockItem from "./StockItem.vue";

// Reactive state - using ref() instead of reactive() for better performance
const loading = ref(true);
const error = ref<string | null>(null);
const connectionStatus = ref<"connecting" | "connected" | "disconnected">(
  "connecting"
);
const lastUpdate = ref<Date | null>(null);
const topGainers = ref<any[]>([]);
const topLosers = ref<any[]>([]);

let eventSource: EventSource | null = null;
let retryCount = 0;
const MAX_RETRY_ATTEMPTS = 5;
const RETRY_DELAY = 2000; // 2 seconds

// Computed properties for better performance
const statusText = computed(() => {
  switch (connectionStatus.value) {
    case "connected":
      return "Live Data Stream";
    case "connecting":
      return "Connecting...";
    case "disconnected":
      return "Connection Lost";
    default:
      return "Unknown Status";
  }
});

// Utility functions
const formatTime = (date: Date) => {
  return date.toLocaleTimeString("en-NP", {
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
  });
};

// Performance optimization: check if data has actually changed
const hasDataChanged = (newData: any[], currentData: any[]) => {
  if (newData.length !== currentData.length) return true;

  return newData.some((newStock, index) => {
    const currentStock = currentData[index];
    return (
      !currentStock ||
      newStock.symbol !== currentStock.symbol ||
      newStock.ltp !== currentStock.ltp ||
      newStock.percentageChange !== currentStock.percentageChange ||
      newStock.pointChange !== currentStock.pointChange
    );
  });
};

const connectSSE = () => {
  if (eventSource && eventSource.readyState === EventSource.OPEN) {
    return;
  }

  // Clean up existing connection
  if (eventSource) {
    eventSource.close();
  }

  error.value = null;
  connectionStatus.value = "connecting";

  try {
    eventSource = new EventSource("/api/trending-stocks-sse");

    eventSource.onopen = () => {
      console.log("SSE connection established");
      connectionStatus.value = "connected";
      error.value = null;
      retryCount = 0; // Reset retry count on successful connection
    };

    eventSource.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);

        if (data.error) {
          console.error("SSE Error:", data.error);
          error.value = `Server error: ${data.error}`;
          return;
        }

        // Optimized data updates - only update if data has actually changed
        if (data.gainers && data.gainers.length > 0) {
          const newGainers = data.gainers.slice(0, 8);
          if (hasDataChanged(newGainers, topGainers.value)) {
            topGainers.value = newGainers;
          }
        }

        if (data.losers && data.losers.length > 0) {
          const newLosers = data.losers.slice(0, 8);
          if (hasDataChanged(newLosers, topLosers.value)) {
            topLosers.value = newLosers;
          }
        }

        lastUpdate.value = new Date();

        if (loading.value) {
          loading.value = false;
        }
      } catch (err) {
        console.error("Error parsing SSE message:", err);
        error.value = "Error parsing server response";
      }
    };

    eventSource.onerror = (err) => {
      console.error("EventSource failed:", err);
      connectionStatus.value = "disconnected";

      if (eventSource) {
        eventSource.close();
      }

      // Implement exponential backoff retry
      if (retryCount < MAX_RETRY_ATTEMPTS) {
        retryCount++;
        const delay = RETRY_DELAY * Math.pow(2, retryCount - 1); // Exponential backoff
        error.value = `Connection lost. Retrying in ${Math.ceil(
          delay / 1000
        )}s... (${retryCount}/${MAX_RETRY_ATTEMPTS})`;

        setTimeout(() => {
          if (connectionStatus.value === "disconnected") {
            connectSSE();
          }
        }, delay);
      } else {
        error.value = `Connection failed after ${MAX_RETRY_ATTEMPTS} attempts. Please check your internet connection.`;
      }
    };
  } catch (err) {
    console.error("Failed to create EventSource:", err);
    error.value = "Failed to establish connection";
    connectionStatus.value = "disconnected";
  }
};

const reconnect = () => {
  retryCount = 0;
  loading.value = true;
  connectSSE();
};

// Lifecycle hooks
onMounted(() => {
  connectSSE();
});

onUnmounted(() => {
  if (eventSource) {
    eventSource.close();
    eventSource = null;
  }
});
</script>
