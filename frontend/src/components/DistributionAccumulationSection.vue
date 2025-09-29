<template>
  <div class="space-y-6">
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <!-- Accumulation Phase Stocks -->
      <div class="bg-green-50 p-6 rounded-xl border border-green-200">
        <h3
          class="text-lg font-semibold text-green-800 mb-4 flex items-center gap-2"
        >
          <TrendingUpIcon class="w-5 h-5" />
          Accumulation Phase
        </h3>
        <div class="space-y-3">
          <div
            v-for="stock in accumulationStocks"
            :key="stock.symbol"
            class="flex items-center justify-between p-3 bg-white rounded-lg shadow-sm"
          >
            <div>
              <span class="font-semibold text-gray-800">{{
                stock.symbol
              }}</span>
              <div class="text-sm text-gray-600">
                Volume: {{ stock.volume }}
              </div>
            </div>
            <div class="text-right">
              <div class="text-green-600 font-semibold">
                {{ stock.strength }}%
              </div>
              <div class="text-xs text-gray-600">Strength</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Distribution Phase Stocks -->
      <div class="bg-red-50 p-6 rounded-xl border border-red-200">
        <h3
          class="text-lg font-semibold text-red-800 mb-4 flex items-center gap-2"
        >
          <TrendingDownIcon class="w-5 h-5" />
          Distribution Phase
        </h3>
        <div class="space-y-3">
          <div
            v-for="stock in distributionStocks"
            :key="stock.symbol"
            class="flex items-center justify-between p-3 bg-white rounded-lg shadow-sm"
          >
            <div>
              <span class="font-semibold text-gray-800">{{
                stock.symbol
              }}</span>
              <div class="text-sm text-gray-600">
                Volume: {{ stock.volume }}
              </div>
            </div>
            <div class="text-right">
              <div class="text-red-600 font-semibold">
                {{ stock.strength }}%
              </div>
              <div class="text-xs text-gray-600">Weakness</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive } from "vue";
import TrendingUpIcon from "./icons/TrendingUpIcon.vue";
import TrendingDownIcon from "./icons/TrendingDownIcon.vue";

const accumulationStocks = reactive([
  { symbol: "NABIL", volume: "2.3M", strength: 85 },
  { symbol: "SCBL", volume: "1.8M", strength: 78 },
  { symbol: "HBL", volume: "1.5M", strength: 72 },
  { symbol: "EBL", volume: "1.2M", strength: 68 },
]);

const distributionStocks = reactive([
  { symbol: "UPPER", volume: "3.2M", strength: 82 },
  { symbol: "CHCL", volume: "2.1M", strength: 75 },
  { symbol: "AKPL", volume: "1.9M", strength: 70 },
  { symbol: "UMHL", volume: "1.6M", strength: 65 },
]);
</script>
