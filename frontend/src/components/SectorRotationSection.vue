<template>
  <div class="space-y-6">
    <div
      class="bg-gradient-to-r from-purple-50 to-blue-50 p-6 rounded-xl"
    >
      <h3 class="text-lg font-semibold text-gray-800 mb-4">
        Sector Performance Matrix
      </h3>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div
          v-for="sector in sectorPerformance"
          :key="sector.name"
          :class="[
            'p-4 rounded-lg text-center cursor-pointer transition-all duration-200 hover:scale-105',
            sector.trend === 'bullish'
              ? 'bg-green-100 border border-green-300'
              : sector.trend === 'bearish'
              ? 'bg-red-100 border border-red-300'
              : 'bg-gray-100 border border-gray-300',
          ]"
        >
          <div
            class="text-lg font-bold mb-1"
            :class="[
              sector.trend === 'bullish'
                ? 'text-green-700'
                : sector.trend === 'bearish'
                ? 'text-red-700'
                : 'text-gray-700',
            ]"
          >
            {{ sector.change }}%
          </div>
          <div class="text-sm font-medium text-gray-800">
            {{ sector.name }}
          </div>
          <div class="text-xs text-gray-600 mt-1">
            {{ sector.volume }}
          </div>
        </div>
      </div>
    </div>

    <!-- Rotation Analysis -->
    <div class="bg-white p-6 rounded-xl shadow-sm border">
      <h3 class="text-lg font-semibold text-gray-800 mb-4">
        Smart Money Flow Analysis
      </h3>
      <div class="space-y-4">
        <div
          v-for="flow in moneyFlow"
          :key="flow.sector"
          class="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
        >
          <div class="flex items-center gap-3">
            <div
              :class="[
                'w-3 h-3 rounded-full',
                flow.direction === 'inflow'
                  ? 'bg-green-500'
                  : 'bg-red-500',
              ]"
            ></div>
            <span class="font-medium">{{ flow.sector }}</span>
          </div>
          <div class="text-right">
            <div
              :class="[
                'font-semibold',
                flow.direction === 'inflow'
                  ? 'text-green-600'
                  : 'text-red-600',
              ]"
            >
              {{ flow.direction === "inflow" ? "+" : "-" }}Rs.
              {{ flow.amount }}
            </div>
            <div class="text-xs text-gray-600">
              {{ flow.confidence }}% confidence
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive } from "vue";

const sectorPerformance = reactive([
  { name: "Banking", change: 2.3, trend: "bullish", volume: "45.2M" },
  { name: "Insurance", change: -1.2, trend: "bearish", volume: "12.8M" },
  { name: "Hydropower", change: 3.8, trend: "bullish", volume: "28.5M" },
  { name: "Finance", change: 1.5, trend: "bullish", volume: "18.2M" },
  { name: "Hotels", change: -0.8, trend: "bearish", volume: "5.3M" },
  { name: "Manufacturing", change: 0.2, trend: "neutral", volume: "8.7M" },
  { name: "Trading", change: -2.1, trend: "bearish", volume: "15.4M" },
  { name: "Microfinance", change: 1.8, trend: "bullish", volume: "22.1M" },
]);

const moneyFlow = reactive([
  { sector: "Banking", direction: "inflow", amount: "2.5M", confidence: 85 },
  { sector: "Hydropower", direction: "inflow", amount: "1.8M", confidence: 78 },
  { sector: "Insurance", direction: "outflow", amount: "900K", confidence: 72 },
  { sector: "Trading", direction: "outflow", amount: "1.2M", confidence: 80 },
]);
</script>
