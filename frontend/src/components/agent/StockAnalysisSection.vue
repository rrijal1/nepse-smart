<template>
  <div class="space-y-6">
    <div
      class="bg-white border border-gray-200 rounded-xl p-6 shadow-sm space-y-4"
    >
      <div class="flex flex-col md:flex-row md:items-end gap-4">
        <div class="flex-1">
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Stock Symbol
          </label>
          <div class="relative">
            <input
              v-model="symbolModel"
              @input="handleInput"
              @focus="showDropdown = filteredSymbols.length > 0"
              @keyup.enter="emitAnalyze"
              placeholder="e.g., NABIL, ADBL"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[rgb(var(--color-nepse-primary))] focus:border-transparent uppercase"
            />
            <div
              v-if="showDropdown && filteredSymbols.length > 0"
              class="absolute z-20 mt-2 w-full bg-white border border-gray-200 rounded-lg shadow-lg max-h-52 overflow-y-auto"
            >
              <button
                v-for="option in filteredSymbols"
                :key="option"
                @click.prevent="selectSymbol(option)"
                class="w-full text-left px-4 py-2 text-sm hover:bg-gray-100"
              >
                {{ option }}
              </button>
            </div>
          </div>
        </div>

        <div class="flex items-center gap-3">
          <button
            @click="emitAnalyze"
            :disabled="isLoading"
            class="px-6 py-3 bg-[rgb(var(--color-nepse-primary))] text-white rounded-lg hover:bg-opacity-90 transition disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="!isLoading">Run Analysis</span>
            <span v-else class="flex items-center gap-2">
              <span
                class="animate-spin rounded-full h-4 w-4 border-b-2 border-white"
              ></span>
              Analyzing...
            </span>
          </button>
        </div>
      </div>

      <p class="text-sm text-gray-500">
        Powered by LangChain multi-agent pipeline (technical, fundamental,
        macro/news).
      </p>

      <div v-if="error" class="rounded-lg bg-red-50 border border-red-200 p-3">
        <p class="text-sm text-red-700">{{ error }}</p>
      </div>
    </div>

    <div v-if="analysisResult" class="space-y-6">
      <div
        class="bg-gradient-to-r from-blue-50 via-violet-50 to-purple-50 rounded-xl p-6 flex flex-col md:flex-row md:items-center md:justify-between gap-6"
      >
        <div>
          <h2 class="text-2xl font-bold text-gray-900">
            {{ analysisResult.stock_symbol }} Overview
          </h2>
          <p class="text-sm text-gray-600">
            Completed in {{ analysisResult.processing_time_ms }} ms • Updated
            {{ formatTimestamp(analysisResult.timestamp) }}
          </p>
        </div>
        <div class="flex gap-6">
          <div class="text-center">
            <div
              class="text-4xl font-bold"
              :class="scoreColor(analysisResult.overall_score)"
            >
              {{ formatScore(analysisResult.overall_score) }}
            </div>
            <div class="text-xs text-gray-500 tracking-wide uppercase mt-1">
              Overall Score
            </div>
          </div>
          <div class="text-center">
            <div
              class="px-4 py-2 rounded-full text-sm font-semibold"
              :class="recommendationBadge(overallRecommendation)"
            >
              {{ overallRecommendation }}
            </div>
            <div class="text-xs text-gray-500 tracking-wide uppercase mt-1">
              Recommendation
            </div>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div
          v-for="card in detailCards"
          :key="card.title"
          :class="[
            'rounded-xl border shadow-sm p-5',
            themeClasses[card.theme] || 'border-gray-200 bg-gray-50',
          ]"
        >
          <div class="flex items-center justify-between mb-3">
            <div
              class="flex items-center gap-2 text-sm font-semibold text-gray-800"
            >
              <span>{{ card.icon }}</span>
              <span>{{ card.title }}</span>
            </div>
            <span :class="['text-xl font-bold', scoreTint(card.detail.score)]">
              {{ formatScore(card.detail.score) }}
            </span>
          </div>
          <ul class="space-y-1 text-sm text-gray-700">
            <li
              v-for="line in extractHighlights(card.detail.summary)"
              :key="line"
            >
              • {{ line }}
            </li>
          </ul>
        </div>
      </div>

      <div class="bg-white border border-gray-200 rounded-xl shadow-sm p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-3">Analyst Notes</h3>
        <pre
          class="whitespace-pre-wrap text-sm leading-relaxed text-gray-700"
          >{{ analysisResult.analysis }}</pre
        >
      </div>
    </div>

    <div
      v-else-if="!isLoading"
      class="bg-white border border-dashed border-gray-300 rounded-xl p-6 text-center text-gray-500"
    >
      Run an analysis to view detailed multi-agent insights.
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch } from "vue";
import type { AgentAnalysisResponse, AgentDetail } from "../../services/agent";

const props = defineProps<{
  selectedSymbol: string;
  availableSymbols: string[];
  analysisResult: AgentAnalysisResponse | null;
  isLoading: boolean;
  error: string | null;
}>();

const emit = defineEmits<{
  (e: "update:selectedSymbol", value: string): void;
  (e: "analyze", value: string): void;
}>();

const symbolModel = computed({
  get: () => props.selectedSymbol,
  set: (value: string) => emit("update:selectedSymbol", value.toUpperCase()),
});

const showDropdown = ref(false);

const filteredSymbols = computed(() => {
  const query = symbolModel.value.trim().toUpperCase();
  if (!query) return props.availableSymbols.slice(0, 8);
  return props.availableSymbols
    .filter((symbol) => symbol.toUpperCase().includes(query))
    .slice(0, 8);
});

watch(
  () => props.availableSymbols,
  () => {
    if (filteredSymbols.value.length === 0) {
      showDropdown.value = false;
    }
  },
  { immediate: true }
);

const overallRecommendation = computed(() =>
  getRecommendationFromScore(props.analysisResult?.overall_score ?? 0)
);

const handleInput = () => {
  showDropdown.value = filteredSymbols.value.length > 0;
};

const selectSymbol = (value: string) => {
  symbolModel.value = value;
  showDropdown.value = false;
  emitAnalyze();
};

const emitAnalyze = () => {
  const symbol = symbolModel.value.trim();
  if (!symbol) return;
  emit("analyze", symbol.toUpperCase());
};

const scoreColor = (score: number) => {
  if (score > 0) return "text-green-600";
  if (score < 0) return "text-red-600";
  return "text-gray-600";
};

const recommendationBadge = (recommendation: string) => {
  switch (recommendation) {
    case "BUY":
      return "bg-green-100 text-green-800";
    case "HOLD":
      return "bg-yellow-100 text-yellow-800";
    case "NEUTRAL":
      return "bg-blue-100 text-blue-800";
    case "SELL":
      return "bg-red-100 text-red-800";
    default:
      return "bg-gray-100 text-gray-800";
  }
};

const formatScore = (score: number) => (score > 0 ? `+${score}` : `${score}`);

const formatTimestamp = (timestamp: string) => {
  try {
    return new Date(timestamp).toLocaleString();
  } catch (error) {
    return timestamp;
  }
};

const getRecommendationFromScore = (score: number) => {
  if (score >= 5) return "BUY";
  if (score >= 2) return "HOLD";
  if (score >= -2) return "NEUTRAL";
  return "SELL";
};

const extractHighlights = (summary: string) =>
  summary
    .split(".")
    .map((sentence) => sentence.trim())
    .filter(Boolean)
    .slice(0, 3);

const themeClasses: Record<string, string> = {
  blue: "border-blue-200 bg-blue-50",
  green: "border-green-200 bg-green-50",
  purple: "border-purple-200 bg-purple-50",
};

const scoreTint = (score: number) => {
  if (score > 0) return "text-green-600";
  if (score < 0) return "text-red-600";
  return "text-gray-500";
};

const detailCards = computed(() => {
  if (!props.analysisResult)
    return [] as Array<{
      title: string;
      icon: string;
      theme: keyof typeof themeClasses;
      detail: AgentDetail;
    }>;

  return [
    {
      title: "Technical Signals",
      icon: "📈",
      theme: "blue" as const,
      detail: props.analysisResult.agent_details.technical_analysis,
    },
    {
      title: "Fundamental Health",
      icon: "🏦",
      theme: "green" as const,
      detail: props.analysisResult.agent_details.fundamental_analysis,
    },
    {
      title: "Macro & News",
      icon: "📰",
      theme: "purple" as const,
      detail: props.analysisResult.agent_details.macro_news_analysis,
    },
  ];
});
</script>
