<template>
  <div class="space-y-6">
    <!-- Portfolio Summary Cards -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-6">
      <div
        class="bg-gradient-to-br from-green-50 to-green-100 p-6 rounded-xl border border-green-200"
      >
        <div class="flex items-center justify-between mb-4">
          <h3 class="font-semibold text-green-800">Total Portfolio</h3>
          <TrendingUpIcon class="w-5 h-5 text-green-600" />
        </div>
        <div class="text-2xl font-bold text-green-700">Rs. 12,45,000</div>
        <div class="text-sm text-green-600 mt-1">+Rs. 45,000 (3.75%)</div>
      </div>

      <div
        class="bg-gradient-to-br from-blue-50 to-blue-100 p-6 rounded-xl border border-blue-200"
      >
        <div class="flex items-center justify-between mb-4">
          <h3 class="font-semibold text-blue-800">Day's P&L</h3>
          <ChartIcon class="w-5 h-5 text-blue-600" />
        </div>
        <div class="text-2xl font-bold text-blue-700">+Rs. 8,500</div>
        <div class="text-sm text-blue-600 mt-1">+0.68% today</div>
      </div>

      <div
        class="bg-gradient-to-br from-purple-50 to-purple-100 p-6 rounded-xl border border-purple-200"
      >
        <div class="flex items-center justify-between mb-4">
          <h3 class="font-semibold text-purple-800">Holdings</h3>
          <PortfolioIcon class="w-5 h-5 text-purple-600" />
        </div>
        <div class="text-2xl font-bold text-purple-700">15</div>
        <div class="text-sm text-purple-600 mt-1">
          Stocks in portfolio
        </div>
      </div>

      <div
        class="bg-gradient-to-br from-yellow-50 to-yellow-100 p-6 rounded-xl border border-yellow-200"
      >
        <div class="flex items-center justify-between mb-4">
          <h3 class="font-semibold text-yellow-800">Cash Available</h3>
          <WalletIcon class="w-5 h-5 text-yellow-600" />
        </div>
        <div class="text-2xl font-bold text-yellow-700">Rs. 2,50,000</div>
        <div class="text-sm text-yellow-600 mt-1">Ready to invest</div>
      </div>
    </div>

    <!-- Watchlist Table -->
    <div
      class="bg-white border border-gray-200 rounded-xl overflow-hidden"
    >
      <div class="px-6 py-4 border-b border-gray-200 bg-gray-50">
        <h3 class="text-lg font-semibold text-gray-800">My Watchlist</h3>
      </div>
      <div class="overflow-x-auto">
        <table class="min-w-full">
          <thead class="bg-gray-50 border-b border-gray-200">
            <tr>
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Symbol
              </th>
              <th
                class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                LTP
              </th>
              <th
                class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Change
              </th>
              <th
                class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                % Change
              </th>
              <th
                class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Volume
              </th>
              <th
                class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Holdings
              </th>
              <th
                class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Action
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr
              v-for="stock in watchlistStocks"
              :key="stock.symbol"
              class="hover:bg-gray-50"
            >
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                  <div class="font-semibold text-gray-900">
                    {{ stock.symbol }}
                  </div>
                  <StarIcon
                    :class="[
                      'w-4 h-4 ml-2 cursor-pointer',
                      stock.favorite
                        ? 'text-yellow-500 fill-current'
                        : 'text-gray-300',
                    ]"
                    @click="toggleFavorite(stock.symbol)"
                  />
                </div>
              </td>
              <td
                class="px-6 py-4 whitespace-nowrap text-right font-mono font-semibold"
              >
                Rs. {{ stock.ltp.toLocaleString() }}
              </td>
              <td
                class="px-6 py-4 whitespace-nowrap text-right font-mono font-semibold"
                :class="
                  stock.change >= 0 ? 'text-green-600' : 'text-red-600'
                "
              >
                {{ stock.change >= 0 ? "+" : "" }}{{ stock.change }}
              </td>
              <td
                class="px-6 py-4 whitespace-nowrap text-right font-mono font-semibold"
                :class="
                  stock.changePercent >= 0
                    ? 'text-green-600'
                    : 'text-red-600'
                "
              >
                {{ stock.changePercent >= 0 ? "+" : ""
                }}{{ stock.changePercent }}%
              </td>
              <td
                class="px-6 py-4 whitespace-nowrap text-right font-mono text-sm text-gray-600"
              >
                {{ stock.volume }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right">
                <div v-if="stock.holdings > 0" class="text-sm">
                  <div class="font-semibold text-gray-900">
                    {{ stock.holdings }} shares
                  </div>
                  <div class="text-gray-600">
                    Avg: Rs. {{ stock.avgPrice }}
                  </div>
                </div>
                <div v-else class="text-gray-400 text-sm">
                  Not holding
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-center">
                <button
                  class="text-[rgb(var(--color-nepse-primary))] hover:text-blue-700 text-sm font-medium"
                >
                  Trade
                </button>
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
import TrendingUpIcon from "./icons/TrendingUpIcon.vue";
import ChartIcon from "./icons/ChartIcon.vue";
import PortfolioIcon from "./icons/PortfolioIcon.vue";
import WalletIcon from "./icons/WalletIcon.vue";
import StarIcon from "./icons/StarIcon.vue";

const watchlistStocks = reactive([
  {
    symbol: "NABIL",
    ltp: 1235,
    change: 45,
    changePercent: 3.78,
    volume: "2.3M",
    holdings: 100,
    avgPrice: 1180,
    favorite: true,
  },
  {
    symbol: "SCBL",
    ltp: 567,
    change: -12,
    changePercent: -2.07,
    volume: "1.8M",
    holdings: 0,
    avgPrice: 0,
    favorite: false,
  },
  {
    symbol: "HBL",
    ltp: 689,
    change: 28,
    changePercent: 4.24,
    volume: "1.5M",
    holdings: 50,
    avgPrice: 650,
    favorite: true,
  },
  {
    symbol: "EBL",
    ltp: 890,
    change: 35,
    changePercent: 4.09,
    volume: "1.2M",
    holdings: 75,
    avgPrice: 820,
    favorite: false,
  },
  {
    symbol: "UPPER",
    ltp: 456,
    change: -23,
    changePercent: -4.79,
    volume: "3.2M",
    holdings: 200,
    avgPrice: 480,
    favorite: true,
  },
]);

const toggleFavorite = (symbol: string) => {
  const stock = watchlistStocks.find((s) => s.symbol === symbol);
  if (stock) {
    stock.favorite = !stock.favorite;
  }
};
</script>
