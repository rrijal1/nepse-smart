<template>
  <div class="flex h-[calc(100vh-120px)]">
    <!-- Left Sidebar -->
    <Sidebar
      v-model:activeSection="activeSection"
      :sidebarItems="sidebarItems"
    />

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
        <ChartsSection v-if="activeSection === 'charts'" />
        <TradingStrategiesSection v-if="activeSection === 'strategies'" />
        <SectorRotationSection v-if="activeSection === 'sectors'" />
        <DistributionAccumulationSection
          v-if="activeSection === 'distribution'"
        />
        <ExpertChatSection v-if="activeSection === 'expert-chat'" />
        <AiChatSection v-if="activeSection === 'ai-chat'" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import Sidebar from "../components/Sidebar.vue";
import ChartsSection from "../components/ChartsSection.vue";
import TradingStrategiesSection from "../components/TradingStrategiesSection.vue";
import SectorRotationSection from "../components/SectorRotationSection.vue";
import DistributionAccumulationSection from "../components/DistributionAccumulationSection.vue";
import ExpertChatSection from "../components/ExpertChatSection.vue";
import AiChatSection from "../components/AiChatSection.vue";
import ChartIcon from "../components/icons/ChartIcon.vue";
import CogIcon from "../components/icons/CogIcon.vue";
import PieChartIcon from "../components/icons/PieChartIcon.vue";
import TrendingUpIcon from "../components/icons/TrendingUpIcon.vue";
import UsersIcon from "../components/icons/UsersIcon.vue";
import SparklesIcon from "../components/icons/SparklesIcon.vue";

const activeSection = ref("charts");

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
</script>
