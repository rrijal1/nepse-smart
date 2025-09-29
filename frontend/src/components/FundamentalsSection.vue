<template>
  <div class="space-y-6">
    <!-- Stock Screener -->
    <div class="bg-gray-50 p-6 rounded-xl">
      <h3 class="text-lg font-semibold text-gray-800 mb-4">
        Stock Screener
      </h3>
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2"
            >Market Cap</label
          >
          <select
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[rgb(var(--color-nepse-primary))] focus:border-transparent"
          >
            <option>Any</option>
            <option>Large Cap</option>
            <option>Mid Cap</option>
            <option>Small Cap</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2"
            >P/E Ratio</label
          >
          <select
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[rgb(var(--color-nepse-primary))] focus:border-transparent"
          >
            <option>Any</option>
            <option>< 15</option>
            <option>15-25</option>
            <option>> 25</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2"
            >ROE</label
          >
          <select
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[rgb(var(--color-nepse-primary))] focus:border-transparent"
          >
            <option>Any</option>
            <option>> 15%</option>
            <option>10-15%</option>
            <option>< 10%</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2"
            >Debt/Equity</label
          >
          <select
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[rgb(var(--color-nepse-primary))] focus:border-transparent"
          >
            <option>Any</option>
            <option>< 0.5</option>
            <option>0.5-1.0</option>
            <option>> 1.0</option>
          </select>
        </div>
      </div>
      <button
        class="mt-4 px-6 py-2 bg-[rgb(var(--color-nepse-primary))] text-white rounded-lg hover:bg-blue-700 transition-colors"
      >
        Apply Filters
      </button>
    </div>

    <!-- Fundamental Analysis Results -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div
        v-for="stock in fundamentalStocks"
        :key="stock.symbol"
        class="bg-white border border-gray-200 rounded-xl p-6"
      >
        <div class="flex items-center justify-between mb-4">
          <h3 class="font-semibold text-gray-800">{{ stock.symbol }}</h3>
          <span
            :class="[
              'px-2 py-1 rounded-full text-xs font-medium',
              stock.rating === 'Strong Buy'
                ? 'bg-green-100 text-green-800'
                : stock.rating === 'Buy'
                ? 'bg-blue-100 text-blue-800'
                : stock.rating === 'Hold'
                ? 'bg-yellow-100 text-yellow-800'
                : 'bg-red-100 text-red-800',
            ]"
          >
            {{ stock.rating }}
          </span>
        </div>
        <div class="grid grid-cols-2 gap-4 text-sm">
          <div class="space-y-2">
            <div class="flex justify-between">
              <span class="text-gray-600">P/E Ratio:</span>
              <span class="font-semibold">{{ stock.pe }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">ROE:</span>
              <span class="font-semibold">{{ stock.roe }}%</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">ROA:</span>
              <span class="font-semibold">{{ stock.roa }}%</span>
            </div>
          </div>
          <div class="space-y-2">
            <div class="flex justify-between">
              <span class="text-gray-600">Book Value:</span>
              <span class="font-semibold">Rs. {{ stock.bookValue }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">EPS:</span>
              <span class="font-semibold">Rs. {{ stock.eps }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">Debt/Equity:</span>
              <span class="font-semibold">{{ stock.debtEquity }}</span>
            </div>
          </div>
        </div>
        <button
          class="w-full mt-4 px-4 py-2 border border-[rgb(var(--color-nepse-primary))] text-[rgb(var(--color-nepse-primary))] rounded-lg hover:bg-[rgb(var(--color-nepse-primary))]/10 transition-colors text-sm font-medium"
        >
          View Details
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive } from "vue";

const fundamentalStocks = reactive([
  {
    symbol: "NABIL",
    rating: "Strong Buy",
    pe: 12.5,
    roe: 18.2,
    roa: 2.1,
    bookValue: 890,
    eps: 98.7,
    debtEquity: 0.3,
  },
  {
    symbol: "SCBL",
    rating: "Buy",
    pe: 15.2,
    roe: 16.8,
    roa: 1.9,
    bookValue: 456,
    eps: 37.3,
    debtEquity: 0.4,
  },
  {
    symbol: "HBL",
    rating: "Hold",
    pe: 18.7,
    roe: 14.5,
    roa: 1.7,
    bookValue: 523,
    eps: 36.8,
    debtEquity: 0.5,
  },
  {
    symbol: "EBL",
    rating: "Buy",
    pe: 14.1,
    roe: 17.3,
    roa: 2.0,
    bookValue: 678,
    eps: 63.1,
    debtEquity: 0.35,
  },
]);
</script>
