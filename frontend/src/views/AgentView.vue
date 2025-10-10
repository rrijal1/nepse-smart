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
      <div
        class="p-6 border-b border-gray-200 bg-gradient-to-r from-blue-50 to-indigo-50"
      >
        <div class="flex items-center justify-between">
          <div>
            <h1
              class="text-2xl font-bold text-gray-900 flex items-center gap-3"
            >
              <SparklesIcon class="w-8 h-8 text-blue-600" />
              NEPSE Trading Agent
            </h1>
            <p class="text-gray-600 mt-1">
              AI-powered trading analysis for Nepal Stock Exchange
            </p>
          </div>
          <div class="flex items-center gap-3">
            <div
              class="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-medium"
            >
              ● Live Analysis
            </div>
          </div>
        </div>
      </div>

      <!-- Dynamic Content -->
      <div class="flex h-full">
        <!-- Main Analysis Area -->
        <div class="flex-1 p-6 overflow-y-auto">
          <StockAnalysisSection v-if="activeSection === 'analysis'" />
          <TechnicalIndicatorsSection v-if="activeSection === 'technical'" />
          <NewsAnalysisSection v-if="activeSection === 'news'" />
          <PortfolioRecommendationsSection
            v-if="activeSection === 'portfolio'"
          />
        </div>

        <!-- Right Panel - AI Chat -->
        <div class="w-96 border-l border-gray-200 bg-gray-50">
          <AiChatPanel />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import Sidebar from "../components/Sidebar.vue";
import StockAnalysisSection from "../components/agent/StockAnalysisSection.vue";
import TechnicalIndicatorsSection from "../components/agent/TechnicalIndicatorsSection.vue";
import NewsAnalysisSection from "../components/agent/NewsAnalysisSection.vue";
import PortfolioRecommendationsSection from "../components/agent/PortfolioRecommendationsSection.vue";
import AiChatPanel from "../components/agent/AiChatPanel.vue";
import SparklesIcon from "../components/icons/SparklesIcon.vue";
import ChartIcon from "../components/icons/ChartIcon.vue";
import NewsIcon from "../components/icons/NewsIcon.vue";
import PortfolioIcon from "../components/icons/PortfolioIcon.vue";

const activeSection = ref("analysis");

const sidebarItems = [
  { id: "analysis", label: "Stock Analysis", icon: ChartIcon },
  { id: "technical", label: "Technical Indicators", icon: SparklesIcon },
  { id: "news", label: "News & Sentiment", icon: NewsIcon },
  { id: "portfolio", label: "Portfolio Insights", icon: PortfolioIcon },
];
</script>
