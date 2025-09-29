<template>
  <div class="space-y-6">
    <!-- Technical Screener -->
    <div class="bg-gray-50 p-6 rounded-xl">
      <h3 class="text-lg font-semibold text-gray-800 mb-4">
        Technical Screener
      </h3>
      <div class="grid grid-cols-1 md:grid-cols-5 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2"
            >RSI</label
          >
          <select
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[rgb(var(--color-nepse-primary))] focus:border-transparent"
          >
            <option>Any</option>
            <option>Overbought (>70)</option>
            <option>Oversold (<30)</option>
            <option>Neutral (30-70)</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2"
            >MACD</label
          >
          <select
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[rgb(var(--color-nepse-primary))] focus:border-transparent"
          >
            <option>Any</option>
            <option>Bullish Crossover</option>
            <option>Bearish Crossover</option>
            <option>Above Signal</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2"
            >Moving Average</label
          >
          <select
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[rgb(var(--color-nepse-primary))] focus:border-transparent"
          >
            <option>Any</option>
            <option>Above 50 SMA</option>
            <option>Below 50 SMA</option>
            <option>Golden Cross</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2"
            >Volume</label
          >
          <select
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[rgb(var(--color-nepse-primary))] focus:border-transparent"
          >
            <option>Any</option>
            <option>Above Average</option>
            <option>High Volume</option>
            <option>Low Volume</option>
          </select>
        </div>
        <div class="flex items-end">
          <button
            class="w-full px-4 py-2 bg-[rgb(var(--color-nepse-primary))] text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            Scan
          </button>
        </div>
      </div>
    </div>

    <!-- Technical Analysis Results -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <div
        v-for="stock in technicalStocks"
        :key="stock.symbol"
        class="bg-white border border-gray-200 rounded-xl p-6"
      >
        <div class="flex items-center justify-between mb-4">
          <h3 class="font-semibold text-gray-800">{{ stock.symbol }}</h3>
          <span
            :class="[
              'px-2 py-1 rounded-full text-xs font-medium',
              stock.signal === 'Strong Buy'
                ? 'bg-green-100 text-green-800'
                : stock.signal === 'Buy'
                ? 'bg-blue-100 text-blue-800'
                : stock.signal === 'Hold'
                ? 'bg-yellow-100 text-yellow-800'
                : 'bg-red-100 text-red-800',
            ]"
          >
            {{ stock.signal }}
          </span>
        </div>
        <div class="space-y-3 text-sm">
          <div class="flex items-center justify-between">
            <span class="text-gray-600">RSI (14):</span>
            <span
              :class="[
                'font-semibold',
                stock.rsi > 70
                  ? 'text-red-600'
                  : stock.rsi < 30
                  ? 'text-green-600'
                  : 'text-gray-800',
              ]"
              >{{ stock.rsi }}</span
            >
          </div>
          <div class="flex items-center justify-between">
            <span class="text-gray-600">MACD:</span>
            <span
              :class="[
                'font-semibold',
                stock.macd === 'Bullish'
                  ? 'text-green-600'
                  : stock.macd === 'Bearish'
                  ? 'text-red-600'
                  : 'text-gray-800',
              ]"
              >{{ stock.macd }}</span
            >
          </div>
          <div class="flex items-center justify-between">
            <span class="text-gray-600">Support:</span>
            <span class="font-mono font-semibold"
              >Rs. {{ stock.support }}</span
            >
          </div>
          <div class="flex items-center justify-between">
            <span class="text-gray-600">Resistance:</span>
            <span class="font-mono font-semibold"
              >Rs. {{ stock.resistance }}</span
            >
          </div>
          <div class="flex items-center justify-between">
            <span class="text-gray-600">Volume Trend:</span>
            <span
              :class="[
                'font-semibold',
                stock.volumeTrend === 'High'
                  ? 'text-green-600'
                  : stock.volumeTrend === 'Low'
                  ? 'text-red-600'
                  : 'text-gray-800',
              ]"
              >{{ stock.volumeTrend }}</span
            >
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive } from "vue";

const technicalStocks = reactive([
  {
    symbol: "NABIL",
    signal: "Strong Buy",
    rsi: 45,
    macd: "Bullish",
    support: 1180,
    resistance: 1280,
    volumeTrend: "High",
  },
  {
    symbol: "SCBL",
    signal: "Sell",
    rsi: 75,
    macd: "Bearish",
    support: 520,
    resistance: 580,
    volumeTrend: "Low",
  },
  {
    symbol: "HBL",
    signal: "Buy",
    rsi: 55,
    macd: "Bullish",
    support: 650,
    resistance: 720,
    volumeTrend: "Medium",
  },
  {
    symbol: "EBL",
    signal: "Hold",
    rsi: 60,
    macd: "Neutral",
    support: 850,
    resistance: 920,
    volumeTrend: "Medium",
  },
  {
    symbol: "UPPER",
    signal: "Strong Sell",
    rsi: 25,
    macd: "Bearish",
    support: 420,
    resistance: 480,
    volumeTrend: "High",
  },
  {
    symbol: "CHCL",
    signal: "Buy",
    rsi: 35,
    macd: "Bullish",
    support: 480,
    resistance: 550,
    volumeTrend: "High",
  },
]);
</script>
