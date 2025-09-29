<template>
  <div class="space-y-6">
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div
        v-for="strategy in tradingStrategies"
        :key="strategy.id"
        class="bg-gradient-to-br from-white to-gray-50 p-6 rounded-xl shadow-sm border hover:shadow-md transition-shadow"
      >
        <div class="flex items-center justify-between mb-4">
          <h3 class="font-semibold text-gray-800">{{ strategy.name }}</h3>
          <span
            :class="[
              'px-2 py-1 rounded-full text-xs font-medium',
              strategy.performance >= 0
                ? 'bg-green-100 text-green-800'
                : 'bg-red-100 text-red-800',
            ]"
          >
            {{ strategy.performance >= 0 ? "+" : ""
            }}{{ strategy.performance }}%
          </span>
        </div>
        <p class="text-gray-600 text-sm mb-4">
          {{ strategy.description }}
        </p>
        <div class="space-y-2 text-sm">
          <div class="flex justify-between">
            <span class="text-gray-600">Risk Level:</span>
            <span
              :class="[
                'font-semibold',
                strategy.risk === 'Low'
                  ? 'text-green-600'
                  : strategy.risk === 'Medium'
                  ? 'text-yellow-600'
                  : 'text-red-600',
              ]"
              >{{ strategy.risk }}</span
            >
          </div>
          <div class="flex justify-between">
            <span class="text-gray-600">Time Frame:</span>
            <span class="font-semibold">{{ strategy.timeframe }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-gray-600">Success Rate:</span>
            <span class="font-semibold">{{ strategy.successRate }}%</span>
          </div>
        </div>
        <button
          class="w-full mt-4 px-4 py-2 bg-[rgb(var(--color-nepse-primary))] text-white rounded-lg hover:bg-blue-700 transition-colors text-sm font-medium"
        >
          Apply Strategy
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive } from "vue";

const tradingStrategies = reactive([
  {
    id: 1,
    name: "Momentum Breakout",
    description: "Identifies stocks breaking above resistance with high volume",
    performance: 15.8,
    risk: "Medium",
    timeframe: "1-3 days",
    successRate: 72,
  },
  {
    id: 2,
    name: "Support Bounce",
    description: "Trades stocks bouncing off strong support levels",
    performance: 12.3,
    risk: "Low",
    timeframe: "2-5 days",
    successRate: 68,
  },
  {
    id: 3,
    name: "Mean Reversion",
    description: "Capitalizes on oversold conditions in quality stocks",
    performance: -2.1,
    risk: "Low",
    timeframe: "1-2 weeks",
    successRate: 58,
  },
  {
    id: 4,
    name: "Trend Following",
    description: "Rides established trends with proper risk management",
    performance: 18.7,
    risk: "High",
    timeframe: "1-4 weeks",
    successRate: 65,
  },
]);
</script>
