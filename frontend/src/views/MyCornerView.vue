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
        </div>
      </div>

      <!-- Dynamic Content -->
      <div class="p-6 overflow-y-auto" style="height: calc(100% - 100px)">
        <WatchlistSection v-if="activeSection === 'watchlist'" />
        <MyNewsSection v-if="activeSection === 'news'" />
        <FundamentalsSection v-if="activeSection === 'fundamentals'" />
        <TechnicalSection v-if="activeSection === 'technical'" />
        <PortfolioSection v-if="activeSection === 'portfolio'" />
        <PaperTradingSection v-if="activeSection === 'paper-trading'" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import Sidebar from "../components/Sidebar.vue";
import WatchlistSection from "../components/WatchlistSection.vue";
import MyNewsSection from "../components/MyNewsSection.vue";
import FundamentalsSection from "../components/FundamentalsSection.vue";
import TechnicalSection from "../components/TechnicalSection.vue";
import PortfolioSection from "../components/PortfolioSection.vue";
import PaperTradingSection from "../components/PaperTradingSection.vue";
import EyeIcon from "../components/icons/EyeIcon.vue";
import NewsIcon from "../components/icons/NewsIcon.vue";
import DocumentIcon from "../components/icons/DocumentIcon.vue";
import ChartIcon from "../components/icons/ChartIcon.vue";
import PortfolioIcon from "../components/icons/PortfolioIcon.vue";
import BriefcaseIcon from "../components/icons/BriefcaseIcon.vue";

const activeSection = ref("portfolio");

const sidebarItems = [
  { id: "portfolio", label: "Portfolio", icon: PortfolioIcon },
  { id: "paper-trading", label: "Paper Trading", icon: BriefcaseIcon },
  { id: "news", label: "News & Updates", icon: NewsIcon, badge: "12" },
  { id: "fundamentals", label: "Fundamentals", icon: DocumentIcon },
  { id: "technical", label: "Technical Analysis", icon: ChartIcon },
  { id: "watchlist", label: "My Watchlist", icon: EyeIcon },
];

const getCurrentSectionTitle = () => {
  const section = sidebarItems.find((item) => item.id === activeSection.value);
  return section ? section.label : "My Corner";
};

const getCurrentSectionDescription = () => {
  const descriptions: Record<string, string> = {
    watchlist: "Monitor your favorite stocks and portfolio performance",
    news: "Stay updated with news relevant to your investments",
    fundamentals: "Analyze stocks based on financial metrics and ratios",
    technical: "Technical analysis and trading signals for your stocks",
    portfolio: "Track your portfolio performance and holdings",
    "paper-trading": "Practice trading with a virtual portfolio",
  };
  return descriptions[activeSection.value] || "Your personalized trading hub";
};
</script>
