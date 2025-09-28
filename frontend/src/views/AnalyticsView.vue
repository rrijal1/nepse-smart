<template>
  <div class="flex h-[calc(100vh-120px)]">
    <!-- Left Sidebar -->
    <div class="w-80 bg-white shadow-lg rounded-lg mr-6 overflow-hidden">
      <div
        class="p-4 bg-gradient-to-r from-[rgb(var(--color-nepse-primary))] to-[rgb(var(--color-nepse-secondary))] text-white"
      >
        <h2 class="text-lg font-semibold">Analytics Hub</h2>
      </div>

      <!-- Navigation Menu -->
      <nav class="p-2">
        <div class="space-y-1">
          <button
            v-for="item in sidebarItems"
            :key="item.id"
            @click="activeSection = item.id"
            :class="[
              'w-full flex items-center gap-3 px-4 py-3 text-left rounded-lg transition-all duration-200',
              activeSection === item.id
                ? 'bg-[rgb(var(--color-nepse-primary))]/10 text-[rgb(var(--color-nepse-primary))] font-semibold border-l-4 border-[rgb(var(--color-nepse-primary))]'
                : 'text-gray-700 hover:bg-gray-50 hover:text-[rgb(var(--color-nepse-primary))]',
            ]"
          >
            <component :is="item.icon" class="w-5 h-5" />
            <span>{{ item.label }}</span>
            <span
              v-if="item.badge"
              class="ml-auto bg-green-500 text-white text-xs px-2 py-1 rounded-full"
            >
              {{ item.badge }}
            </span>
          </button>
        </div>
      </nav>
    </div>

    <!-- Main Content Area -->
    <div class="flex-1 bg-white rounded-lg shadow-lg overflow-hidden">
      <!-- Content Header -->
      <div class="p-6 border-b border-gray-200 bg-gray-50">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-2xl font-bold text-gray-900">
              {{ getCurrentSectionTitle() }}
            </h1>
            <p class="text-gray-600 mt-1">
              {{ getCurrentSectionDescription() }}
            </p>
          </div>
          <div class="flex items-center gap-3">
            <button
              class="px-4 py-2 bg-[rgb(var(--color-nepse-primary))] text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              <svg
                class="w-4 h-4 inline mr-2"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"
                />
              </svg>
              Export Data
            </button>
          </div>
        </div>
      </div>

      <!-- Dynamic Content -->
      <div class="p-6 h-full overflow-y-auto">
        <!-- Charts Section with Technical Analysis -->
        <div v-if="activeSection === 'charts'" class="space-y-6">
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

        <!-- Trading Strategies Section -->
        <div v-if="activeSection === 'strategies'" class="space-y-6">
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

        <!-- Sector Rotation Section -->
        <div v-if="activeSection === 'sectors'" class="space-y-6">
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

        <!-- Distribution & Accumulation Section -->
        <div v-if="activeSection === 'distribution'" class="space-y-6">
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

        <!-- Expert Chat Section -->
        <div
          v-if="activeSection === 'expert-chat'"
          class="h-full flex flex-col"
        >
          <div class="flex-1 bg-gray-50 rounded-lg p-4 mb-4 overflow-y-auto">
            <div class="space-y-4">
              <div
                v-for="message in expertChatMessages"
                :key="message.id"
                class="flex items-start gap-3"
              >
                <div
                  class="w-8 h-8 rounded-full bg-[rgb(var(--color-nepse-primary))] text-white flex items-center justify-center text-sm font-semibold flex-shrink-0"
                >
                  {{ message.sender.charAt(0) }}
                </div>
                <div class="flex-1">
                  <div class="flex items-center gap-2 mb-1">
                    <span class="font-semibold text-gray-800">{{
                      message.sender
                    }}</span>
                    <span v-if="message.verified" class="text-blue-500">
                      <VerifiedIcon class="w-4 h-4" />
                    </span>
                    <span class="text-xs text-gray-500">{{
                      message.time
                    }}</span>
                  </div>
                  <div class="text-gray-700 text-sm">{{ message.content }}</div>
                  <div
                    v-if="message.analysis"
                    class="mt-2 p-3 bg-blue-50 rounded-lg border border-blue-200"
                  >
                    <div class="text-xs text-blue-800 font-semibold mb-1">
                      Market Analysis
                    </div>
                    <div class="text-sm text-blue-700">
                      {{ message.analysis }}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="flex gap-2">
            <input
              v-model="expertMessage"
              @keyup.enter="sendExpertMessage"
              type="text"
              placeholder="Ask the experts..."
              class="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[rgb(var(--color-nepse-primary))] focus:border-transparent"
            />
            <button
              @click="sendExpertMessage"
              class="px-6 py-2 bg-[rgb(var(--color-nepse-primary))] text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              Send
            </button>
          </div>
        </div>

        <!-- AI Chat Section -->
        <div v-if="activeSection === 'ai-chat'" class="h-full flex flex-col">
          <div class="flex-1 bg-gray-50 rounded-lg p-4 mb-4 overflow-y-auto">
            <div class="space-y-4">
              <div
                v-for="message in aiChatMessages"
                :key="message.id"
                :class="[
                  'flex',
                  message.type === 'user' ? 'justify-end' : 'justify-start',
                ]"
              >
                <div
                  :class="[
                    'max-w-md px-4 py-3 rounded-lg',
                    message.type === 'user'
                      ? 'bg-[rgb(var(--color-nepse-primary))] text-white'
                      : 'bg-white text-gray-800 shadow-sm border',
                  ]"
                >
                  <div
                    v-if="message.type === 'ai'"
                    class="flex items-center gap-2 mb-2"
                  >
                    <SparklesIcon
                      class="w-4 h-4 text-[rgb(var(--color-nepse-primary))]"
                    />
                    <span class="font-semibold text-sm"
                      >NEPSE AI Assistant</span
                    >
                  </div>
                  <div class="text-sm">{{ message.content }}</div>
                  <div
                    v-if="message.suggestion"
                    class="mt-2 p-2 bg-gray-50 rounded text-xs"
                  >
                    <strong>Suggestion:</strong> {{ message.suggestion }}
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="flex gap-2">
            <input
              v-model="aiMessage"
              @keyup.enter="sendAiMessage"
              type="text"
              placeholder="Ask me anything about the market in plain language..."
              class="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[rgb(var(--color-nepse-primary))] focus:border-transparent"
            />
            <button
              @click="sendAiMessage"
              class="px-6 py-2 bg-gradient-to-r from-[rgb(var(--color-nepse-primary))] to-[rgb(var(--color-nepse-secondary))] text-white rounded-lg hover:opacity-90 transition-opacity"
            >
              <SparklesIcon class="w-4 h-4 inline mr-2" />
              Ask AI
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from "vue";

import { defineComponent, h } from "vue";

// Analytics section icons - Using Vue 3 render functions
const ChartIcon = defineComponent({
  name: "ChartIcon",
  render: () =>
    h(
      "svg",
      {
        fill: "none",
        stroke: "currentColor",
        viewBox: "0 0 24 24",
        xmlns: "http://www.w3.org/2000/svg",
      },
      [
        h("path", {
          "stroke-linecap": "round",
          "stroke-linejoin": "round",
          "stroke-width": "2",
          d: "M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z",
        }),
      ]
    ),
});

const TrendingUpIcon = defineComponent({
  name: "TrendingUpIcon",
  render: () =>
    h(
      "svg",
      {
        fill: "none",
        stroke: "currentColor",
        viewBox: "0 0 24 24",
        xmlns: "http://www.w3.org/2000/svg",
      },
      [
        h("path", {
          "stroke-linecap": "round",
          "stroke-linejoin": "round",
          "stroke-width": "2",
          d: "M13 7h8m0 0v8m0-8l-8 8-4-4-6 6",
        }),
      ]
    ),
});

const TrendingDownIcon = defineComponent({
  name: "TrendingDownIcon",
  render: () =>
    h(
      "svg",
      {
        fill: "none",
        stroke: "currentColor",
        viewBox: "0 0 24 24",
        xmlns: "http://www.w3.org/2000/svg",
      },
      [
        h("path", {
          "stroke-linecap": "round",
          "stroke-linejoin": "round",
          "stroke-width": "2",
          d: "M13 17h8m0 0V9m0 8l-8-8-4 4-6-6",
        }),
      ]
    ),
});

const CogIcon = defineComponent({
  name: "CogIcon",
  render: () =>
    h(
      "svg",
      {
        fill: "none",
        stroke: "currentColor",
        viewBox: "0 0 24 24",
        xmlns: "http://www.w3.org/2000/svg",
      },
      [
        h("path", {
          "stroke-linecap": "round",
          "stroke-linejoin": "round",
          "stroke-width": "2",
          d: "M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z",
        }),
        h("path", {
          "stroke-linecap": "round",
          "stroke-linejoin": "round",
          "stroke-width": "2",
          d: "M15 12a3 3 0 11-6 0 3 3 0 016 0z",
        }),
      ]
    ),
});

const PieChartIcon = defineComponent({
  name: "PieChartIcon",
  render: () =>
    h(
      "svg",
      {
        fill: "none",
        stroke: "currentColor",
        viewBox: "0 0 24 24",
        xmlns: "http://www.w3.org/2000/svg",
      },
      [
        h("path", {
          "stroke-linecap": "round",
          "stroke-linejoin": "round",
          "stroke-width": "2",
          d: "M11 3.055A9.001 9.001 0 1020.945 13H11V3.055z",
        }),
        h("path", {
          "stroke-linecap": "round",
          "stroke-linejoin": "round",
          "stroke-width": "2",
          d: "M20.488 9H15V3.512A9.025 9.025 0 0120.488 9z",
        }),
      ]
    ),
});

const UsersIcon = defineComponent({
  name: "UsersIcon",
  render: () =>
    h(
      "svg",
      {
        fill: "none",
        stroke: "currentColor",
        viewBox: "0 0 24 24",
        xmlns: "http://www.w3.org/2000/svg",
      },
      [
        h("path", {
          "stroke-linecap": "round",
          "stroke-linejoin": "round",
          "stroke-width": "2",
          d: "M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a4 4 0 11-8 0 4 4 0 018 0z",
        }),
      ]
    ),
});

const SparklesIcon = defineComponent({
  name: "SparklesIcon",
  render: () =>
    h(
      "svg",
      {
        fill: "none",
        stroke: "currentColor",
        viewBox: "0 0 24 24",
        xmlns: "http://www.w3.org/2000/svg",
      },
      [
        h("path", {
          "stroke-linecap": "round",
          "stroke-linejoin": "round",
          "stroke-width": "2",
          d: "M5 3a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2V5a2 2 0 00-2-2H5zM5 17a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2v-2a2 2 0 00-2-2H5zM19 3a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2V5a2 2 0 00-2-2h-2zM19 17a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2v-2a2 2 0 00-2-2h-2z",
        }),
      ]
    ),
});

// Reactive data
const activeSection = ref("charts");
const selectedStock = ref("NABIL");
const selectedTimeframe = ref("1D");
const expertMessage = ref("");
const aiMessage = ref("");

// Sidebar items
const sidebarItems = [
  { id: "charts", label: "Charts", icon: ChartIcon },
  { id: "strategies", label: "Trading Strategies", icon: CogIcon },
  { id: "sectors", label: "Sector Rotation", icon: PieChartIcon },
  {
    id: "distribution",
    label: "Distribution & Accumulation",
    icon: TrendingUpIcon,
  },
  { id: "expert-chat", label: "Expert Chat", icon: UsersIcon, badge: "Live" },
  { id: "ai-chat", label: "AI Assistant", icon: SparklesIcon },
];

// Chart data
const timeframes = ["5M", "15M", "1H", "4H", "1D", "1W", "1M"];
const technicalIndicators = reactive([
  { id: "ma", name: "MA", active: true },
  { id: "rsi", name: "RSI", active: false },
  { id: "macd", name: "MACD", active: true },
  { id: "bb", name: "BB", active: false },
]);

// Trading strategies data
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

// Sector performance data
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

// Distribution & Accumulation data
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

// Chat messages
const expertChatMessages = reactive([
  {
    id: 1,
    sender: "Dr. Sharma",
    verified: true,
    content:
      "Banking sector showing strong accumulation patterns. Volume analysis suggests institutional buying.",
    analysis:
      "Key resistance at 1,250 for NABIL. Break above this level could trigger momentum rally to 1,350.",
    time: "2 hours ago",
  },
  {
    id: 2,
    sender: "TradeGuru",
    verified: true,
    content:
      "Hydropower stocks are forming a sector rotation play. Watch for breakouts in UPPER and CHCL.",
    time: "1 hour ago",
  },
]);

const aiChatMessages = reactive([
  {
    id: 1,
    type: "ai",
    content:
      "Hello! I'm your NEPSE AI assistant. I can help you analyze market data, explain technical indicators, and provide investment insights. What would you like to know?",
    suggestion:
      'Try asking "What stocks are showing bullish signals today?" or "Explain RSI indicator"',
  },
]);

// Methods
const getCurrentSectionTitle = () => {
  const section = sidebarItems.find((item) => item.id === activeSection.value);
  return section ? section.label : "Analytics Hub";
};

const getCurrentSectionDescription = () => {
  const descriptions: Record<string, string> = {
    charts:
      "Advanced technical analysis with support/resistance levels and liquidity zones",
    strategies:
      "Proven trading strategies with performance metrics and risk analysis",
    sectors: "Smart money flow analysis and sector rotation patterns",
    distribution: "Identify accumulation and distribution phases in real-time",
    "expert-chat": "Live chat with verified market experts and analysts",
    "ai-chat": "AI-powered market analysis and investment guidance",
  };
  return descriptions[activeSection.value] || "Advanced analytics and insights";
};

const toggleIndicator = (id: string) => {
  const indicator = technicalIndicators.find((i) => i.id === id);
  if (indicator) {
    indicator.active = !indicator.active;
  }
};

const sendExpertMessage = () => {
  if (expertMessage.value.trim()) {
    expertChatMessages.push({
      id: Date.now(),
      sender: "You",
      verified: false,
      content: expertMessage.value,
      time: "now",
    });
    expertMessage.value = "";
  }
};

const sendAiMessage = () => {
  if (aiMessage.value.trim()) {
    aiChatMessages.push({
      id: Date.now(),
      type: "user",
      content: aiMessage.value,
      suggestion: "",
    });

    // Simulate AI response
    setTimeout(() => {
      aiChatMessages.push({
        id: Date.now() + 1,
        type: "ai",
        content:
          "Based on current market data, I can provide insights on that topic. Let me analyze the latest information for you.",
        suggestion:
          "Would you like me to analyze specific stocks or market sectors?",
      });
    }, 1000);

    aiMessage.value = "";
  }
};
</script>
