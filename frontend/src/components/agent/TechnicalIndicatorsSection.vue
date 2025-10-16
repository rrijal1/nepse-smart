<template>
  <div class="space-y-6">
    <div
      v-if="isLoading"
      class="rounded-lg border border-blue-100 bg-blue-50 p-4 text-blue-700"
    >
      <div class="flex items-center gap-3">
        <span
          class="h-4 w-4 animate-spin rounded-full border-b-2 border-blue-500"
        ></span>
        Running technical analysis... hang tight.
      </div>
    </div>

    <div
      v-else-if="!analysisResult"
      class="rounded-lg border border-dashed border-gray-300 bg-white p-6 text-center text-gray-500"
    >
      Run a stock analysis first to view detailed technical indicators and
      signals.
    </div>

    <div v-else class="grid grid-cols-1 gap-6 lg:grid-cols-2">
      <div class="rounded-xl border border-blue-200 bg-blue-50 p-6 shadow-sm">
        <h3
          class="mb-2 flex items-center gap-2 text-lg font-semibold text-blue-900"
        >
          <span>📊</span>
          Core Technical View
        </h3>
        <ul class="space-y-2 text-sm text-blue-800">
          <li v-for="line in highlights" :key="line">• {{ line }}</li>
        </ul>
      </div>

      <div class="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
        <h3 class="mb-3 text-lg font-semibold text-gray-900">
          Indicator Snapshot
        </h3>
        <div class="grid grid-cols-2 gap-4 text-sm text-gray-600">
          <div>
            <span class="font-semibold text-gray-800">Score</span>
            <div
              :class="['text-xl font-bold', scoreTint(technicalDetail.score)]"
            >
              {{ formatScore(technicalDetail.score) }}
            </div>
            <p class="text-xs text-gray-500">Aggregated signal strength</p>
          </div>
          <div>
            <span class="font-semibold text-gray-800">Trend Bias</span>
            <div class="text-base font-semibold text-gray-700">
              {{ trendBias }}
            </div>
            <p class="text-xs text-gray-500">Based on moving averages</p>
          </div>
          <div>
            <span class="font-semibold text-gray-800">Momentum</span>
            <p class="mt-1 text-sm text-gray-600">{{ momentumNote }}</p>
          </div>
          <div>
            <span class="font-semibold text-gray-800"
              >Support / Resistance</span
            >
            <p class="mt-1 text-sm text-gray-600">{{ supportResistance }}</p>
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

const technicalDetail = computed(
  () =>
    props.analysisResult?.agent_details.technical_analysis || {
      score: 0,
      summary: "",
    }
);

const highlights = computed(() =>
  technicalDetail.value.summary
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

const trendBias = computed(() => {
  const summary = technicalDetail.value.summary.toLowerCase();
  if (summary.includes("uptrend")) return "Bullish";
  if (summary.includes("downtrend")) return "Bearish";
  return "Neutral";
});

const momentumNote = computed(() => {
  const summary = technicalDetail.value.summary.toLowerCase();
  if (summary.includes("overbought")) return "Overbought conditions detected";
  if (summary.includes("oversold"))
    return "Oversold reading suggests bounce potential";
  if (summary.includes("neutral momentum")) return "Momentum is balanced";
  return "Momentum within normal bounds";
});

const supportResistance = computed(() => {
  const summary = technicalDetail.value.summary.toLowerCase();
  if (summary.includes("resistance")) return "Approaching resistance zone";
  if (summary.includes("support")) return "Holding above key support";
  return "Monitor key price levels";
});
</script>
