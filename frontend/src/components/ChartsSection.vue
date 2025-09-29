<template>
  <div class="space-y-6">
    <!-- Chart Controls -->
    <div class="flex items-center justify-between mb-6">
      <div class="flex items-center gap-4">
        <select
          v-model="selectedStock"
          class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[rgb(var(--color-nepse-primary))] focus:border-transparent"
        >
          <option value="NABIL">NABIL</option>
          <option value="SCBL">SCBL</option>
          <option value="HBL">HBL</option>
          <option value="EBL">EBL</option>
        </select>
        <div class="flex items-center gap-2">
          <button
            v-for="timeframe in timeframes"
            :key="timeframe"
            @click="selectedTimeframe = timeframe"
            :class="[
              'px-3 py-1 rounded-md text-sm font-medium transition-colors',
              selectedTimeframe === timeframe
                ? 'bg-[rgb(var(--color-nepse-primary))] text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200',
            ]"
          >
            {{ timeframe }}
          </button>
        </div>
      </div>
      <div class="flex items-center gap-2">
        <button
          v-for="indicator in technicalIndicators"
          :key="indicator.id"
          @click="toggleIndicator(indicator.id)"
          :class="[
            'px-3 py-1 rounded-md text-sm font-medium transition-colors',
            indicator.active
              ? 'bg-green-100 text-green-800'
              : 'bg-gray-100 text-gray-700 hover:bg-gray-200',
          ]"
        >
          {{ indicator.name }}
        </button>
      </div>
    </div>

    <!-- Main Chart Area -->
    <div class="bg-gray-50 rounded-xl p-6 h-96 relative">
      <div class="flex items-center justify-center h-full">
        <div class="text-center">
          <ChartIcon class="w-16 h-16 text-gray-400 mx-auto mb-4" />
          <h3 class="text-lg font-semibold text-gray-600 mb-2">
            Advanced Trading Chart
          </h3>
          <p class="text-gray-500">
            {{ selectedStock }} - {{ selectedTimeframe }} with Technical
            Analysis
          </p>
          <div class="mt-4 text-sm text-gray-600">
            <div class="flex items-center justify-center gap-6">
              <div class="flex items-center gap-2">
                <div class="w-3 h-0.5 bg-red-500"></div>
                <span>Resistance Lines</span>
              </div>
              <div class="flex items-center gap-2">
                <div class="w-3 h-0.5 bg-green-500"></div>
                <span>Support Lines</span>
              </div>
              <div class="flex items-center gap-2">
                <div class="w-3 h-0.5 bg-blue-500"></div>
                <span>Liquidity Zones</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Chart Overlay Information -->
      <div
        class="absolute top-4 left-4 bg-white rounded-lg shadow-sm p-3 text-sm"
      >
        <div class="space-y-1">
          <div class="flex justify-between gap-8">
            <span class="text-gray-600">Current Price:</span>
            <span class="font-semibold">Rs. 1,235</span>
          </div>
          <div class="flex justify-between gap-8">
            <span class="text-gray-600">Stop Loss:</span>
            <span class="text-red-600 font-semibold">Rs. 1,180</span>
          </div>
          <div class="flex justify-between gap-8">
            <span class="text-gray-600">Take Profit:</span>
            <span class="text-green-600 font-semibold">Rs. 1,320</span>
          </div>
          <div class="flex justify-between gap-8">
            <span class="text-gray-600">R:R Ratio:</span>
            <span class="font-semibold">1:1.55</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Key Levels Panel -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="bg-red-50 p-4 rounded-lg border border-red-200">
        <h4
          class="font-semibold text-red-800 mb-3 flex items-center gap-2"
        >
          <TrendingDownIcon class="w-4 h-4" />
          Resistance Levels
        </h4>
        <div class="space-y-2 text-sm">
          <div class="flex justify-between">
            <span>Strong:</span>
            <span class="font-mono font-semibold">1,350</span>
          </div>
          <div class="flex justify-between">
            <span>Medium:</span>
            <span class="font-mono">1,280</span>
          </div>
          <div class="flex justify-between">
            <span>Weak:</span>
            <span class="font-mono">1,250</span>
          </div>
        </div>
      </div>

      <div class="bg-green-50 p-4 rounded-lg border border-green-200">
        <h4
          class="font-semibold text-green-800 mb-3 flex items-center gap-2"
        >
          <TrendingUpIcon class="w-4 h-4" />
          Support Levels
        </h4>
        <div class="space-y-2 text-sm">
          <div class="flex justify-between">
            <span>Strong:</span>
            <span class="font-mono font-semibold">1,150</span>
          </div>
          <div class="flex justify-between">
            <span>Medium:</span>
            <span class="font-mono">1,200</span>
          </div>
          <div class="flex justify-between">
            <span>Weak:</span>
            <span class="font-mono">1,220</span>
          </div>
        </div>
      </div>

      <div class="bg-blue-50 p-4 rounded-lg border border-blue-200">
        <h4
          class="font-semibold text-blue-800 mb-3 flex items-center gap-2"
        >
          <WaveIcon class="w-4 h-4" />
          Liquidity Zones
        </h4>
        <div class="space-y-2 text-sm">
          <div class="flex justify-between">
            <span>High Volume:</span>
            <span class="font-mono font-semibold">1,180-1,200</span>
          </div>
          <div class="flex justify-between">
            <span>Medium Volume:</span>
            <span class="font-mono">1,280-1,300</span>
          </div>
          <div class="flex justify-between">
            <span>Low Volume:</span>
            <span class="font-mono">1,320-1,340</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from "vue";
import ChartIcon from "./icons/ChartIcon.vue";
import TrendingUpIcon from "./icons/TrendingUpIcon.vue";
import TrendingDownIcon from "./icons/TrendingDownIcon.vue";
import WaveIcon from "./icons/WaveIcon.vue";

const selectedStock = ref("NABIL");
const selectedTimeframe = ref("1D");

const timeframes = ["5M", "15M", "1H", "4H", "1D", "1W", "1M"];
const technicalIndicators = reactive([
  { id: "ma", name: "MA", active: true },
  { id: "rsi", name: "RSI", active: false },
  { id: "macd", name: "MACD", active: true },
  { id: "bb", name: "BB", active: false },
]);

const toggleIndicator = (id: string) => {
  const indicator = technicalIndicators.find((i) => i.id === id);
  if (indicator) {
    indicator.active = !indicator.active;
  }
};
</script>
