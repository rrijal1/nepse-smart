<template>
  <div class="space-y-6">
    <!-- Portfolio Performance Chart -->
    <div class="bg-white border border-gray-200 rounded-xl p-6">
      <h3 class="text-lg font-semibold text-gray-800 mb-4">
        Portfolio Performance
      </h3>
      <div class="h-64 bg-gray-50 rounded-lg flex items-center justify-center">
        <div class="text-center">
          <ChartIcon class="w-12 h-12 text-gray-400 mx-auto mb-2" />
          <p class="text-gray-600">Portfolio performance chart</p>
          <p class="text-sm text-gray-500">+15.8% overall return</p>
        </div>
      </div>
    </div>

    <!-- Holdings Table -->
    <div class="bg-white border border-gray-200 rounded-xl overflow-hidden">
      <div class="px-6 py-4 border-b border-gray-200 bg-gray-50">
        <h3 class="text-lg font-semibold text-gray-800">Current Holdings</h3>
      </div>
      <div class="overflow-x-auto">
        <table class="min-w-full">
          <thead class="bg-gray-50 border-b border-gray-200">
            <tr>
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Stock
              </th>
              <th
                class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Quantity
              </th>
              <th
                class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Avg Price
              </th>
              <th
                class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Current Price
              </th>
              <th
                class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                P&L
              </th>
              <th
                class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                % Change
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr
              v-for="holding in portfolioHoldings"
              :key="holding.symbol"
              class="hover:bg-gray-50"
            >
              <td
                class="px-6 py-4 whitespace-nowrap font-semibold text-gray-900"
              >
                {{ holding.symbol }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right font-mono">
                {{ holding.quantity }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right font-mono">
                Rs. {{ holding.avgPrice.toLocaleString() }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right font-mono">
                Rs. {{ holding.currentPrice.toLocaleString() }}
              </td>
              <td
                class="px-6 py-4 whitespace-nowrap text-right font-mono font-semibold"
                :class="holding.pnl >= 0 ? 'text-green-600' : 'text-red-600'"
              >
                {{ holding.pnl >= 0 ? "+" : "" }}Rs.
                {{ Math.abs(holding.pnl).toLocaleString() }}
              </td>
              <td
                class="px-6 py-4 whitespace-nowrap text-right font-mono font-semibold"
                :class="
                  holding.pnlPercent >= 0 ? 'text-green-600' : 'text-red-600'
                "
              >
                {{ holding.pnlPercent >= 0 ? "+" : ""
                }}{{ holding.pnlPercent }}%
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive } from "vue";
import ChartIcon from "./icons/ChartIcon.vue";

const portfolioHoldings = reactive([
  {
    symbol: "NABIL",
    quantity: 100,
    avgPrice: 1180,
    currentPrice: 1235,
    pnl: 5500,
    pnlPercent: 4.66,
  },
  {
    symbol: "HBL",
    quantity: 50,
    avgPrice: 650,
    currentPrice: 689,
    pnl: 1950,
    pnlPercent: 6.0,
  },
  {
    symbol: "EBL",
    quantity: 75,
    avgPrice: 820,
    currentPrice: 890,
    pnl: 5250,
    pnlPercent: 8.54,
  },
  {
    symbol: "UPPER",
    quantity: 200,
    avgPrice: 480,
    currentPrice: 456,
    pnl: -4800,
    pnlPercent: -5.0,
  },
  {
    symbol: "BOKL",
    quantity: 150,
    avgPrice: 320,
    currentPrice: 345,
    pnl: 3750,
    pnlPercent: 7.81,
  },
]);
</script>
