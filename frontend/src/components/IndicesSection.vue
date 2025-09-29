<template>
  <div class="space-y-6">
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div
        v-for="index in nepseIndices"
        :key="index.name"
        class="bg-gradient-to-br from-white to-gray-50 p-6 rounded-xl shadow-sm border"
      >
        <div class="flex items-center justify-between mb-4">
          <h3 class="font-semibold text-gray-800">{{ index.name }}</h3>
          <span
            :class="[
              'px-2 py-1 rounded-full text-xs font-medium',
              index.change >= 0
                ? 'bg-green-100 text-green-800'
                : 'bg-red-100 text-red-800',
            ]"
          >
            {{ index.change >= 0 ? "+" : "" }}{{ index.change }}%
          </span>
        </div>
        <div class="space-y-2">
          <div class="flex justify-between">
            <span class="text-gray-600">Current:</span>
            <span class="font-mono font-semibold">{{
              index.current.toLocaleString()
            }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-gray-600">Previous:</span>
            <span class="font-mono">{{
              index.previous.toLocaleString()
            }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive } from "vue";

const nepseIndices = reactive([
  { name: "NEPSE Index", current: 2145.67, previous: 2139.23, change: 0.3 },
  { name: "Banking", current: 1876.45, previous: 1889.12, change: -0.67 },
  {
    name: "Hotels & Tourism",
    current: 2834.21,
    previous: 2798.67,
    change: 1.27,
  },
  { name: "Hydropower", current: 2156.78, previous: 2134.56, change: 1.04 },
  { name: "Finance", current: 1654.32, previous: 1667.89, change: -0.81 },
  { name: "Insurance", current: 8976.45, previous: 8934.21, change: 0.47 },
]);
</script>
