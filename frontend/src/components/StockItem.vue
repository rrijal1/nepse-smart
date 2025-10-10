<template>
  <div
    class="flex items-center justify-between p-3 bg-white rounded-lg shadow-sm transition-all duration-200 hover:shadow-md"
  >
    <div>
      <span class="font-semibold text-gray-800">{{ stock.symbol }}</span>
      <div class="text-sm text-gray-600">{{ formattedLtp }}</div>
    </div>
    <div class="text-right">
      <div
        :class="['font-semibold', isGainer ? 'text-green-600' : 'text-red-600']"
      >
        {{ formattedPercentageChange }}
      </div>
      <div class="text-sm text-gray-600">
        {{ formattedPointChange }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";

interface Stock {
  symbol: string;
  ltp: number;
  percentageChange: number;
  pointChange: number;
}

interface Props {
  stock: Stock;
  isGainer: boolean;
}

const props = defineProps<Props>();

// Computed properties for formatted values to avoid template calculations
const formattedLtp = computed(() => {
  return typeof props.stock.ltp === "number"
    ? props.stock.ltp.toFixed(2)
    : props.stock.ltp;
});

const formattedPercentageChange = computed(() => {
  const change = props.stock.percentageChange;
  const prefix = props.isGainer ? "+" : "";
  return `${prefix}${typeof change === "number" ? change.toFixed(2) : change}%`;
});

const formattedPointChange = computed(() => {
  const change = props.stock.pointChange;
  const prefix = props.isGainer ? "+" : "";
  return `${prefix}${typeof change === "number" ? change.toFixed(2) : change}`;
});
</script>
