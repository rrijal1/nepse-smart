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
      class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
    >
      Retry Connection
    </button>
  </div>
  <div v-else class="space-y-6">
    <!-- Connection Status -->
    <div
      class="flex items-center justify-between mb-4 p-3 bg-gray-50 rounded-lg"
    >
      <div class="flex items-center gap-2">
        <div
          :class="[
            'w-3 h-3 rounded-full',
            connectionStatus === 'connected'
              ? 'bg-green-500'
              : connectionStatus === 'connecting'
              ? 'bg-yellow-500'
              : 'bg-red-500',
          ]"
        ></div>
        <span class="text-sm font-medium">
          {{
            connectionStatus === "connected"
              ? "Live Data"
              : connectionStatus === "connecting"
              ? "Connecting..."
              : "Disconnected"
          }}
        </span>
      </div>
      <div v-if="lastUpdate" class="text-xs text-gray-600">
        Last updated: {{ formatTime(lastUpdate) }}
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
          Top Gainers (WebSocket)
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
              <div class="text-sm text-gray-600">+{{ stock.pointChange }}</div>
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
          Top Losers (WebSocket)
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
import { ref, onMounted, onUnmounted } from "vue";
import TrendingUpIcon from "./icons/TrendingUpIcon.vue";
import TrendingDownIcon from "./icons/TrendingDownIcon.vue";
import Spinner from "./Spinner.vue";

const loading = ref(true);
const error = ref<string | null>(null);
const connectionStatus = ref<"connecting" | "connected" | "disconnected">(
  "connecting"
);
const lastUpdate = ref<Date | null>(null);
const topGainers = ref<any[]>([]);
const topLosers = ref<any[]>([]);

let socket: WebSocket | null = null;
// let reconnectTimeout: NodeJS.Timeout | null = null;

const formatTime = (date: Date) => {
  return date.toLocaleTimeString("en-NP", {
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
  });
};

const connectWebSocket = () => {
  if (socket && socket.readyState === WebSocket.OPEN) {
    return;
  }

  error.value = null;
  connectionStatus.value = "connecting";

  // Use relative path for WebSocket which will be proxied by Vite
  const socketUrl = `ws://${window.location.host}/ws/trending-stocks`;
  socket = new WebSocket(socketUrl);

  socket.onopen = () => {
    console.log("WebSocket connection established");
    connectionStatus.value = "connected";
    error.value = null;
  };

  socket.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);
      if (data.error) {
        console.error("WebSocket Error:", data.error);
        error.value = `Server error: ${data.error}`;
        return;
      }

      if (data.gainers && data.gainers.length > 0) {
        topGainers.value = data.gainers.slice(0, 8);
      }

      if (data.losers && data.losers.length > 0) {
        topLosers.value = data.losers.slice(0, 8);
      }

      lastUpdate.value = new Date();

      if (loading.value) {
        loading.value = false;
      }
    } catch (err) {
      console.error("Error parsing WebSocket message:", err);
      error.value = "Error parsing server response";
    }
  };

  socket.onerror = (err) => {
    console.error("WebSocket failed:", err);
    error.value = "Failed to connect to server";
    connectionStatus.value = "disconnected";
  };

  socket.onclose = (event) => {
    console.log("WebSocket connection closed", event.code, event.reason);
    connectionStatus.value = "disconnected";

    // Auto-reconnect after 5 seconds if connection was established before
    if (!error.value && event.code !== 1000) {
      error.value = "Connection lost. Attempting to reconnect...";
      setTimeout(() => {
        if (connectionStatus.value === "disconnected") {
          connectWebSocket();
        }
      }, 5000);
    }
  };
};

const reconnect = () => {
  if (socket) {
    socket.close();
  }
  loading.value = true;
  connectWebSocket();
};

onMounted(() => {
  connectWebSocket();
});

onUnmounted(() => {
  if (socket) {
    socket.close();
  }
});
</script>
