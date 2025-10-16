<template>
  <div class="flex h-[calc(100vh-120px)]">
    <!-- Left Sidebar -->
    <Sidebar v-model:activeSection="activeSection" :sidebarItems="sidebarItems" />

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
      <div class="p-6 overflow-y-auto" style="height: calc(100% - 100px);">
        <IndicesSection v-if="activeSection === 'indices'" />
        <TrendingStocksSection v-if="activeSection === 'trending'" />
        <NewsSection v-if="activeSection === 'news'" />
        <IposSection v-if="activeSection === 'ipos'" />
        <SmeZoneSection v-if="activeSection === 'sme'" />
        <LearnSection v-if="activeSection === 'learn'" />
        <ChatSection v-if="activeSection === 'chat'" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import Sidebar from "../components/Sidebar.vue";
import IndicesSection from "../components/IndicesSection.vue";
import TrendingStocksSection from "../components/TrendingStocksSection.vue";
import NewsSection from "../components/NewsSection.vue";
import IposSection from "../components/IposSection.vue";
import SmeZoneSection from "../components/SmeZoneSection.vue";
import LearnSection from "../components/LearnSection.vue";
import ChatSection from "../components/ChatSection.vue";
import ChartIcon from "../components/icons/ChartIcon.vue";
import FireIcon from "../components/icons/FireIcon.vue";
import BellIcon from "../components/icons/BellIcon.vue";
import StarIcon from "../components/icons/StarIcon.vue";
import BuildingIcon from "../components/icons/BuildingIcon.vue";
import AcademicCapIcon from "../components/icons/AcademicCapIcon.vue";
import ChatIcon from "../components/icons/ChatIcon.vue";

const activeSection = ref("indices");

const sidebarItems = [
  { id: "indices", label: "Indices", icon: ChartIcon },
  { id: "trending", label: "Trending Stocks", icon: FireIcon },
  { id: "news", label: "News & Updates", icon: BellIcon, badge: "5" },
  { id: "ipos", label: "IPOs", icon: StarIcon },
  { id: "sme", label: "SME Zone", icon: BuildingIcon },
  { id: "learn", label: "Learn", icon: AcademicCapIcon },
  { id: "chat", label: "Chat", icon: ChatIcon },
];

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
</script>