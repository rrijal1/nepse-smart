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
      <div class="flex" style="height: calc(100% - 120px)">
        <!-- Main Analysis Area -->
        <div class="flex-1 p-6 overflow-y-auto">
          <StockAnalysisSection
            v-if="activeSection === 'analysis'"
            v-model:selected-symbol="selectedSymbol"
            :available-symbols="availableSymbols"
            :analysis-result="analysisResult"
            :is-loading="isAnalyzing"
            :error="analysisError"
            @analyze="handleAnalyze"
          />
          <TechnicalIndicatorsSection
            v-if="activeSection === 'technical'"
            :analysis-result="analysisResult"
            :is-loading="isAnalyzing"
          />
          <NewsAnalysisSection
            v-if="activeSection === 'news'"
            :analysis-result="analysisResult"
            :is-loading="isAnalyzing"
          />
          <PortfolioRecommendationsSection
            v-if="activeSection === 'portfolio'"
            :analysis-result="analysisResult"
            :is-loading="isAnalyzing"
          />
        </div>

        <!-- Right Panel - AI Chat -->
        <div class="w-96 border-l border-gray-200 bg-gray-50 p-4 flex flex-col">
          <AiChatSection class="flex-1 min-h-0" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import Sidebar from "../components/Sidebar.vue";
import StockAnalysisSection from "../components/agent/StockAnalysisSection.vue";
import TechnicalIndicatorsSection from "../components/agent/TechnicalIndicatorsSection.vue";
import NewsAnalysisSection from "../components/agent/NewsAnalysisSection.vue";
import PortfolioRecommendationsSection from "../components/agent/PortfolioRecommendationsSection.vue";
import AiChatSection from "../components/AiChatSection.vue";
import SparklesIcon from "../components/icons/SparklesIcon.vue";
import ChartIcon from "../components/icons/ChartIcon.vue";
import NewsIcon from "../components/icons/NewsIcon.vue";
import PortfolioIcon from "../components/icons/PortfolioIcon.vue";
import {
  analyzeAgentStock,
  type AgentAnalysisResponse,
} from "../services/agent";
import { fetchCompanyList } from "../services/marketData_enhanced";

const activeSection = ref("analysis");
const selectedSymbol = ref("NABIL");
const availableSymbols = ref<string[]>([]);

const analysisResult = ref<AgentAnalysisResponse | null>(null);
const isAnalyzing = ref(false);
const analysisError = ref<string | null>(null);

const handleAnalyze = async (symbol?: string) => {
  const targetSymbol = (symbol || selectedSymbol.value || "").toUpperCase();
  if (!targetSymbol) return;

  isAnalyzing.value = true;
  analysisError.value = null;

  try {
    const result = await analyzeAgentStock(targetSymbol);
    analysisResult.value = result;
    selectedSymbol.value = result.stock_symbol;
  } catch (error: any) {
    analysisError.value = error?.message || "Failed to analyze stock.";
  } finally {
    isAnalyzing.value = false;
  }
};

onMounted(async () => {
  const companies = await fetchCompanyList();
  const symbols: string[] = (companies || [])
    .map((c: any) => c?.symbol)
    .filter((s: any) => typeof s === "string" && s.length > 0);

  availableSymbols.value = Array.from(new Set(symbols)).sort();

  if (selectedSymbol.value) {
    if (!availableSymbols.value.includes(selectedSymbol.value)) {
      availableSymbols.value = [
        selectedSymbol.value,
        ...availableSymbols.value,
      ];
    }
  } else if (availableSymbols.value.length > 0) {
    selectedSymbol.value = availableSymbols.value[0];
  }
});

const sidebarItems = [
  { id: "analysis", label: "Stock Analysis", icon: ChartIcon },
  { id: "technical", label: "Technical Indicators", icon: SparklesIcon },
  { id: "news", label: "News & Sentiment", icon: NewsIcon },
  { id: "portfolio", label: "Portfolio Insights", icon: PortfolioIcon },
];
</script>
