<template>
  <div class="space-y-6">
    <div
      v-if="isLoading"
      class="rounded-lg border border-purple-100 bg-purple-50 p-4 text-purple-700"
    >
      <div class="flex items-center gap-3">
        <span
          class="h-4 w-4 animate-spin rounded-full border-b-2 border-purple-500"
        ></span>
        Evaluating macro environment and news sentiment...
      </div>
    </div>

    <div
      v-else-if="!analysisResult"
      class="rounded-lg border border-dashed border-gray-300 bg-white p-6 text-center text-gray-500"
    >
      Run a stock analysis to view macro context, sentiment, and news takeaways.
    </div>

    <div v-else class="grid grid-cols-1 gap-6 lg:grid-cols-2">
      <div
        class="rounded-xl border border-purple-200 bg-purple-50 p-6 shadow-sm"
      >
        <h3
          class="mb-2 flex items-center gap-2 text-lg font-semibold text-purple-900"
        >
          <span>📰</span>
          News & Sentiment Summary
        </h3>
        <ul class="space-y-2 text-sm text-purple-800">
          <li v-for="line in keyThemes" :key="line">• {{ line }}</li>
        </ul>
      </div>

      <div class="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
        <h3 class="mb-3 text-lg font-semibold text-gray-900">
          Macro Takeaways
        </h3>
        <div class="space-y-3 text-sm text-gray-600">
          <div>
            <span class="font-semibold text-gray-800">Score</span>
            <div :class="['text-lg font-bold', scoreTint(macroDetail.score)]">
              {{ formatScore(macroDetail.score) }}
            </div>
          </div>
          <div>
            <span class="font-semibold text-gray-800">Overall Sentiment</span>
            <p class="mt-1">{{ overallSentiment }}</p>
          </div>
          <div>
            <span class="font-semibold text-gray-800"
              >Policy / Market Context</span
            >
            <p class="mt-1">{{ policyContext }}</p>
          </div>
          <div>
            <span class="font-semibold text-gray-800">Actionable Insight</span>
            <p class="mt-1">{{ actionableInsight }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import type { AgentAnalysisResponse } from "../../services/agent";

const props = defineProps<{
  analysisResult: AgentAnalysisResponse | null;
  isLoading: boolean;
}>();

const macroDetail = computed(
  () =>
    props.analysisResult?.agent_details.macro_news_analysis || {
      score: 0,
      summary: "",
    }
);

const keyThemes = computed(() =>
  macroDetail.value.summary
    .split(".")
    .map((sentence) => sentence.trim())
    .filter(Boolean)
    .slice(0, 4)
);

const scoreTint = (score: number) => {
  if (score > 0) return "text-green-600";
  if (score < 0) return "text-red-600";
  return "text-gray-500";
};

const formatScore = (score: number) => (score > 0 ? `+${score}` : `${score}`);

const overallSentiment = computed(() => {
  const summary = macroDetail.value.summary.toLowerCase();
  if (summary.includes("strongly positive")) return "Strongly Positive";
  if (summary.includes("positive")) return "Positive";
  if (summary.includes("strongly negative")) return "Strongly Negative";
  if (summary.includes("negative")) return "Negative";
  return "Neutral";
});

const policyContext = computed(() => {
  const summary = macroDetail.value.summary.toLowerCase();
  if (summary.includes("government"))
    return "Government policy developments may influence price action.";
  if (summary.includes("regulatory"))
    return "Regulatory oversight is in focus—monitor compliance headlines.";
  if (summary.includes("economic"))
    return "Macro-economic trends are shaping investor sentiment.";
  return "Monitor macro calendars and sector-specific news.";
});

const actionableInsight = computed(() => {
  const summary = macroDetail.value.summary.toLowerCase();
  if (summary.includes("impact"))
    return "Market-makers are reacting; expect sentiment-driven volatility.";
  if (summary.includes("sentiment"))
    return "Sentiment shift detected—consider aligning positions with tone.";
  if (summary.includes("score"))
    return "Score suggests recalibrating exposure based on macro outlook.";
  return "Keep an eye on upcoming news catalysts this week.";
});
</script>
