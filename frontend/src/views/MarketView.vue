<template>
  <div class="flex h-[calc(100vh-120px)]">
    <!-- Left Sidebar -->
    <div class="w-80 bg-white shadow-lg rounded-lg mr-6 overflow-hidden">
      <div
        class="p-4 bg-gradient-to-r from-[rgb(var(--color-nepse-primary))] to-[rgb(var(--color-nepse-secondary))] text-white"
      >
        <h2 class="text-lg font-semibold">Market Overview</h2>
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
              class="ml-auto bg-red-500 text-white text-xs px-2 py-1 rounded-full"
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
            <span class="flex items-center gap-2 text-sm text-gray-600">
              <div
                class="w-2 h-2 bg-green-500 rounded-full animate-pulse"
              ></div>
              Live Data
            </span>
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
                  d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
                />
              </svg>
              Refresh
            </button>
          </div>
        </div>
      </div>

      <!-- Dynamic Content -->
      <div class="p-6 h-full overflow-y-auto">
        <!-- Indices Section -->
        <div v-if="activeSection === 'indices'" class="space-y-6">
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

        <!-- Trending Stocks Section -->
        <div v-if="activeSection === 'trending'" class="space-y-6">
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <!-- Top Gainers -->
            <div
              class="bg-gradient-to-br from-green-50 to-white p-6 rounded-xl shadow-sm border"
            >
              <h3
                class="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2"
              >
                <TrendingUpIcon class="w-5 h-5 text-green-600" />
                Top Gainers
              </h3>
              <div class="space-y-3">
                <div
                  v-for="stock in topGainers.slice(0, 8)"
                  :key="stock.symbol"
                  class="flex items-center justify-between p-3 bg-white rounded-lg shadow-sm"
                >
                  <div>
                    <span class="font-semibold text-gray-800">{{
                      stock.symbol
                    }}</span>
                    <div class="text-sm text-gray-600">{{ stock.ltp }}</div>
                  </div>
                  <div class="text-right">
                    <div class="text-green-600 font-semibold">
                      +{{ stock.percentageChange }}%
                    </div>
                    <div class="text-sm text-gray-600">
                      +{{ stock.pointChange }}
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Top Losers -->
            <div
              class="bg-gradient-to-br from-red-50 to-white p-6 rounded-xl shadow-sm border"
            >
              <h3
                class="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2"
              >
                <TrendingDownIcon class="w-5 h-5 text-red-600" />
                Top Losers
              </h3>
              <div class="space-y-3">
                <div
                  v-for="stock in topLosers.slice(0, 8)"
                  :key="stock.symbol"
                  class="flex items-center justify-between p-3 bg-white rounded-lg shadow-sm"
                >
                  <div>
                    <span class="font-semibold text-gray-800">{{
                      stock.symbol
                    }}</span>
                    <div class="text-sm text-gray-600">{{ stock.ltp }}</div>
                  </div>
                  <div class="text-right">
                    <div class="text-red-600 font-semibold">
                      {{ stock.percentageChange }}%
                    </div>
                    <div class="text-sm text-gray-600">
                      {{ stock.pointChange }}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- News & Updates Section -->
        <div v-if="activeSection === 'news'" class="space-y-6">
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div
              v-for="news in newsItems"
              :key="news.id"
              class="bg-white p-6 rounded-xl shadow-sm border hover:shadow-md transition-shadow cursor-pointer"
            >
              <div class="flex items-start gap-4">
                <div
                  class="w-2 h-2 bg-[rgb(var(--color-nepse-primary))] rounded-full mt-2 flex-shrink-0"
                ></div>
                <div class="flex-1">
                  <h3 class="font-semibold text-gray-800 mb-2">
                    {{ news.title }}
                  </h3>
                  <p class="text-gray-600 text-sm mb-3">{{ news.excerpt }}</p>
                  <div
                    class="flex items-center justify-between text-xs text-gray-500"
                  >
                    <span>{{ news.source }}</span>
                    <span>{{ news.time }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- IPOs Section -->
        <div v-if="activeSection === 'ipos'" class="space-y-6">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div
              v-for="ipo in ipoList"
              :key="ipo.company"
              class="bg-gradient-to-br from-blue-50 to-white p-6 rounded-xl shadow-sm border"
            >
              <div class="flex items-center justify-between mb-4">
                <h3 class="font-semibold text-gray-800">{{ ipo.company }}</h3>
                <span
                  :class="[
                    'px-3 py-1 rounded-full text-xs font-medium',
                    ipo.status === 'Open'
                      ? 'bg-green-100 text-green-800'
                      : ipo.status === 'Upcoming'
                      ? 'bg-blue-100 text-blue-800'
                      : 'bg-gray-100 text-gray-800',
                  ]"
                >
                  {{ ipo.status }}
                </span>
              </div>
              <div class="space-y-2 text-sm">
                <div class="flex justify-between">
                  <span class="text-gray-600">Issue Size:</span>
                  <span class="font-semibold">{{ ipo.issueSize }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-600">Price Range:</span>
                  <span class="font-semibold">{{ ipo.priceRange }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-600">Open Date:</span>
                  <span class="font-semibold">{{ ipo.openDate }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-600">Close Date:</span>
                  <span class="font-semibold">{{ ipo.closeDate }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- SME Zone Section -->
        <div v-if="activeSection === 'sme'" class="space-y-6">
          <div
            class="bg-gradient-to-r from-purple-50 to-blue-50 p-6 rounded-xl"
          >
            <h3 class="text-lg font-semibold text-gray-800 mb-4">
              SME Platform Overview
            </h3>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div class="text-center p-4 bg-white rounded-lg">
                <div class="text-2xl font-bold text-purple-600">
                  {{ smeStats.totalCompanies }}
                </div>
                <div class="text-sm text-gray-600">Listed Companies</div>
              </div>
              <div class="text-center p-4 bg-white rounded-lg">
                <div class="text-2xl font-bold text-blue-600">
                  {{ smeStats.totalVolume }}
                </div>
                <div class="text-sm text-gray-600">Total Volume</div>
              </div>
              <div class="text-center p-4 bg-white rounded-lg">
                <div class="text-2xl font-bold text-green-600">
                  {{ smeStats.totalTurnover }}
                </div>
                <div class="text-sm text-gray-600">Total Turnover</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Learn Section -->
        <div v-if="activeSection === 'learn'" class="space-y-6">
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div
              v-for="resource in learningResources"
              :key="resource.id"
              class="bg-white p-6 rounded-xl shadow-sm border hover:shadow-md transition-shadow cursor-pointer"
            >
              <div class="flex items-center gap-3 mb-4">
                <component
                  :is="resource.icon"
                  class="w-8 h-8 text-[rgb(var(--color-nepse-primary))]"
                />
                <h3 class="font-semibold text-gray-800">
                  {{ resource.title }}
                </h3>
              </div>
              <p class="text-gray-600 text-sm mb-4">
                {{ resource.description }}
              </p>
              <div class="flex items-center justify-between">
                <span class="text-xs text-gray-500">{{
                  resource.duration
                }}</span>
                <button
                  class="text-[rgb(var(--color-nepse-primary))] text-sm font-medium hover:underline"
                >
                  Start Learning →
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Chat Section -->
        <div v-if="activeSection === 'chat'" class="h-full flex flex-col">
          <div class="flex-1 bg-gray-50 rounded-lg p-4 mb-4 overflow-y-auto">
            <div class="space-y-4">
              <div
                v-for="message in chatMessages"
                :key="message.id"
                :class="[
                  'flex',
                  message.type === 'user' ? 'justify-end' : 'justify-start',
                ]"
              >
                <div
                  :class="[
                    'max-w-xs lg:max-w-md px-4 py-2 rounded-lg',
                    message.type === 'user'
                      ? 'bg-[rgb(var(--color-nepse-primary))] text-white'
                      : 'bg-white text-gray-800 shadow-sm',
                  ]"
                >
                  <div class="font-medium text-sm mb-1">
                    {{ message.sender }}
                  </div>
                  <div class="text-sm">{{ message.content }}</div>
                  <div class="text-xs opacity-70 mt-1">{{ message.time }}</div>
                </div>
              </div>
            </div>
          </div>
          <div class="flex gap-2">
            <input
              v-model="newMessage"
              @keyup.enter="sendMessage"
              type="text"
              placeholder="Share your market insights..."
              class="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[rgb(var(--color-nepse-primary))] focus:border-transparent"
            />
            <button
              @click="sendMessage"
              class="px-6 py-2 bg-[rgb(var(--color-nepse-primary))] text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              Send
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

// Comprehensive icon set for Market section navigation - Using Vue 3 render functions
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

const FireIcon = defineComponent({
  name: "FireIcon",
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
          d: "M17.657 18.657A8 8 0 016.343 7.343S7 9 9 10c0-2 .5-5 2.986-7C14 5 16.09 5.777 17.656 7.343A7.975 7.975 0 0120 13a7.975 7.975 0 01-2.343 5.657z",
        }),
        h("path", {
          "stroke-linecap": "round",
          "stroke-linejoin": "round",
          "stroke-width": "2",
          d: "M9.879 16.121A3 3 0 1012.015 11L11 14l4-4c-1.09 1.09-2.3 1.8-3.5 2.5a3 3 0 01-1.621-.379z",
        }),
      ]
    ),
});

const BellIcon = defineComponent({
  name: "BellIcon",
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
          d: "M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9",
        }),
      ]
    ),
});

const StarIcon = defineComponent({
  name: "StarIcon",
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
          d: "M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z",
        }),
      ]
    ),
});

const BuildingIcon = defineComponent({
  name: "BuildingIcon",
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
          d: "M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4",
        }),
      ]
    ),
});

const AcademicCapIcon = defineComponent({
  name: "AcademicCapIcon",
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
          d: "M12 14l9-5-9-5-9 5 9 5z",
        }),
        h("path", {
          "stroke-linecap": "round",
          "stroke-linejoin": "round",
          "stroke-width": "2",
          d: "M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z",
        }),
      ]
    ),
});

const ChatIcon = defineComponent({
  name: "ChatIcon",
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
          d: "M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z",
        }),
      ]
    ),
});

// Additional icons used in content sections
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

const BookIcon = defineComponent({
  name: "BookIcon",
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
          d: "M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253",
        }),
      ]
    ),
});

const VideoIcon = defineComponent({
  name: "VideoIcon",
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
          d: "M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z",
        }),
      ]
    ),
});

// Reactive data
const activeSection = ref("indices");
const newMessage = ref("");

// Enhanced sidebar items with better visual icons
const sidebarItems = [
  { id: "indices", label: "Indices", icon: ChartIcon },
  { id: "trending", label: "Trending Stocks", icon: FireIcon },
  { id: "news", label: "News & Updates", icon: BellIcon, badge: "5" },
  { id: "ipos", label: "IPOs", icon: StarIcon },
  { id: "sme", label: "SME Zone", icon: BuildingIcon },
  { id: "learn", label: "Learn", icon: AcademicCapIcon },
  { id: "chat", label: "Chat", icon: ChatIcon },
];

// API integration
import { onMounted } from "vue";
import axios from "axios";

// Sample data (will be replaced with API data)
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

const topGainers = reactive([
  { symbol: "NABIL", ltp: 1235, pointChange: 45, percentageChange: 3.78 },
  { symbol: "SCBL", ltp: 567, pointChange: 23, percentageChange: 4.23 },
  { symbol: "HBL", ltp: 689, pointChange: 28, percentageChange: 4.24 },
  { symbol: "EBL", ltp: 890, pointChange: 35, percentageChange: 4.09 },
  { symbol: "BOKL", ltp: 345, pointChange: 15, percentageChange: 4.55 },
  { symbol: "MBL", ltp: 456, pointChange: 18, percentageChange: 4.11 },
  { symbol: "CBL", ltp: 278, pointChange: 11, percentageChange: 4.12 },
  { symbol: "PRVU", ltp: 567, pointChange: 22, percentageChange: 4.04 },
]);

const topLosers = reactive([
  { symbol: "UPPER", ltp: 456, pointChange: -23, percentageChange: -4.79 },
  { symbol: "CHCL", ltp: 567, pointChange: -28, percentageChange: -4.7 },
  { symbol: "AKPL", ltp: 234, pointChange: -12, percentageChange: -4.88 },
  { symbol: "UMHL", ltp: 345, pointChange: -17, percentageChange: -4.69 },
  { symbol: "NYADI", ltp: 789, pointChange: -38, percentageChange: -4.59 },
  { symbol: "KKHC", ltp: 123, pointChange: -6, percentageChange: -4.65 },
  { symbol: "RHPL", ltp: 456, pointChange: -22, percentageChange: -4.61 },
  { symbol: "SHEL", ltp: 234, pointChange: -11, percentageChange: -4.49 },
]);

// Fetch real data from backend
const fetchMarketData = async () => {
  try {
    // Try to fetch from backend API
    const [gainersRes, losersRes] = await Promise.all([
      axios.get("/api/top-gainers"),
      axios.get("/api/top-losers"),
    ]);

    // Update with real data
    topGainers.splice(0, topGainers.length, ...gainersRes.data.slice(0, 8));
    topLosers.splice(0, topLosers.length, ...losersRes.data.slice(0, 8));
  } catch (error) {
    console.log("Using sample data - API not available:", error);
    // Keep using sample data if API is not available
  }
};

// Initialize data on component mount
onMounted(() => {
  fetchMarketData();
});

const newsItems = reactive([
  {
    id: 1,
    title: "NEPSE Index Crosses 2,150 Mark",
    excerpt: "The benchmark index gained 0.30% in today's trading session...",
    source: "Market Report",
    time: "2 hours ago",
  },
  {
    id: 2,
    title: "Banking Sector Shows Mixed Performance",
    excerpt:
      "While some banks posted gains, overall sector declined by 0.67%...",
    source: "Sector Analysis",
    time: "3 hours ago",
  },
  {
    id: 3,
    title: "Hydropower Stocks Rally Continues",
    excerpt:
      "Hydropower sector gained 1.04% led by strong performance in major stocks...",
    source: "Energy News",
    time: "4 hours ago",
  },
  {
    id: 4,
    title: "New IPO Announcement Expected",
    excerpt:
      "Sources suggest a major company may announce IPO plans next week...",
    source: "IPO Updates",
    time: "5 hours ago",
  },
]);

const ipoList = reactive([
  {
    company: "ABC Banking Ltd.",
    status: "Open",
    issueSize: "1,00,000 shares",
    priceRange: "Rs. 100-120",
    openDate: "2025-09-25",
    closeDate: "2025-10-05",
  },
  {
    company: "XYZ Insurance Co.",
    status: "Upcoming",
    issueSize: "75,000 shares",
    priceRange: "Rs. 200-250",
    openDate: "2025-10-10",
    closeDate: "2025-10-20",
  },
  {
    company: "Nepal Hydro Power",
    status: "Closed",
    issueSize: "2,00,000 shares",
    priceRange: "Rs. 80-100",
    openDate: "2025-09-10",
    closeDate: "2025-09-20",
  },
]);

const smeStats = reactive({
  totalCompanies: 45,
  totalVolume: "2.5M",
  totalTurnover: "Rs. 850M",
});

const learningResources = reactive([
  {
    id: 1,
    title: "Stock Market Basics",
    description: "Learn fundamental concepts of stock market investing",
    duration: "45 min",
    icon: BookIcon,
  },
  {
    id: 2,
    title: "Technical Analysis",
    description: "Master chart patterns and technical indicators",
    duration: "1.5 hours",
    icon: ChartIcon,
  },
  {
    id: 3,
    title: "Video Tutorial Series",
    description: "Comprehensive video course on NEPSE trading",
    duration: "3 hours",
    icon: VideoIcon,
  },
  {
    id: 4,
    title: "Risk Management",
    description: "Essential strategies for managing investment risks",
    duration: "30 min",
    icon: BookIcon,
  },
]);

const chatMessages = reactive([
  {
    id: 1,
    type: "other",
    sender: "TraderPro",
    content: "Anyone watching NABIL today? Strong volume!",
    time: "10:30 AM",
  },
  {
    id: 2,
    type: "user",
    sender: "You",
    content: "Yes, looks like it might break resistance at 1250",
    time: "10:32 AM",
  },
  {
    id: 3,
    type: "other",
    sender: "MarketGuru",
    content: "Banking sector overall looking bullish this week",
    time: "10:35 AM",
  },
]);

// Methods
const getCurrentSectionTitle = () => {
  const section = sidebarItems.find((item) => item.id === activeSection.value);
  return section ? section.label : "Market Overview";
};

const getCurrentSectionDescription = () => {
  const descriptions: Record<string, string> = {
    indices: "Track NEPSE indices and sector performance",
    trending: "Discover top performing stocks in real-time",
    news: "Stay updated with latest market news and updates",
    ipos: "Explore upcoming and ongoing IPO opportunities",
    sme: "Monitor SME platform performance and listings",
    learn: "Enhance your trading knowledge and skills",
    chat: "Connect with fellow traders and market experts",
  };
  return descriptions[activeSection.value] || "Market overview and insights";
};

const sendMessage = () => {
  if (newMessage.value.trim()) {
    chatMessages.push({
      id: Date.now(),
      type: "user",
      sender: "You",
      content: newMessage.value,
      time: new Date().toLocaleTimeString("en-US", {
        hour: "2-digit",
        minute: "2-digit",
      }),
    });
    newMessage.value = "";
  }
};
</script>
