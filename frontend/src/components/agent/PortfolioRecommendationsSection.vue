<template>
  <div class="space-y-6">
    <div
      v-if="isLoading"
      class="rounded-lg border border-green-100 bg-green-50 p-4 text-green-700"
    >
      <div class="flex items-center gap-3">
        <span
          class="h-4 w-4 animate-spin rounded-full border-b-2 border-green-500"
        ></span>
        Building portfolio-focused recommendation...
      </div>
    </div>

    <div
      v-else-if="!analysisResult"
      class="rounded-lg border border-dashed border-gray-300 bg-white p-6 text-center text-gray-500"
    >
      Run a stock analysis to receive portfolio positioning guidance.
    </div>

    <div v-else class="space-y-6">
      <div class="rounded-xl border border-green-200 bg-green-50 p-6 shadow-sm">
        <h3
          class="mb-3 flex items-center gap-2 text-lg font-semibold text-green-900"
        >
          <span>📈</span>
          Portfolio Recommendation
        </h3>
        <div
          class="flex flex-col gap-4 md:flex-row md:items-center md:justify-between"
        >
          <div>
            <div class="text-sm uppercase tracking-wide text-gray-600">
              Overall Score
            </div>
            <div
              :class="[
                'text-3xl font-bold',
                scoreTint(analysisResult.overall_score),
              ]"
            >
              {{ formatScore(analysisResult.overall_score) }}
            </div>
          </div>
          <div>
            <div class="text-sm uppercase tracking-wide text-gray-600">
              Stance
            </div>
            <div
              :class="[
                'mt-1 inline-flex items-center rounded-full px-4 py-1 text-sm font-semibold',
                recommendationBadge(recommendation),
              ]"
            >
              {{ recommendation }}
            </div>
          </div>
          <div class="text-sm text-gray-600">
            <div class="font-semibold text-gray-800">Time Horizon</div>
            <p>{{ horizonNote }}</p>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <div class="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
          <h4 class="mb-2 text-lg font-semibold text-gray-900">
            Fundamental Highlights
          </h4>
          <ul class="space-y-2 text-sm text-gray-700">
            <li v-for="line in fundamentalHighlights" :key="line">
              • {{ line }}
            </li>
          </ul>
        </div>
        <div class="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
          <h4 class="mb-2 text-lg font-semibold text-gray-900">
            Risk Checklist
          </h4>
          <ul class="space-y-2 text-sm text-gray-700">
            <li v-for="risk in riskChecklist" :key="risk">• {{ risk }}</li>
          </ul>
        </div>
      </div>

      <div
        class="rounded-xl border border-yellow-100 bg-yellow-50 p-4 text-sm text-yellow-800"
      >
        Disclaimer: This AI-generated insight is educational and not financial
        advice. Validate with your own research.
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

const recommendation = computed(() => {
  const score = props.analysisResult?.overall_score ?? 0;
  if (score >= 5) return "BUY";
  if (score >= 2) return "HOLD";
  if (score >= -2) return "NEUTRAL";
  return "SELL";
});

const fundamentalDetail = computed(
  () =>
    props.analysisResult?.agent_details.fundamental_analysis || {
      score: 0,
      summary: "",
    }
);

const fundamentalHighlights = computed(() =>
  fundamentalDetail.value.summary
    .split(".")
    .map((sentence) => sentence.trim())
    .filter(Boolean)
    .slice(0, 4)
);

const riskChecklist = computed(() => {
  const analysis = props.analysisResult?.analysis || "";
  return analysis
    .split("\n")
    .filter((line) => /risk|concern|watch/i.test(line))
    .map((line) => line.replace(/[-•]/g, "").trim())
    .slice(0, 4);
});

const horizonNote = computed(() => {
  const analysis = props.analysisResult?.analysis.toLowerCase() || "";
  if (analysis.includes("long-term"))
    return "Best suited for long-term accumulation.";
  if (analysis.includes("short-term"))
    return "Consider tactical positioning for short-term swings.";
  if (analysis.includes("medium-term"))
    return "Align with a medium-term investment horizon.";
  return "Review allocation against your investment timeframe.";
});

const scoreTint = (score: number) => {
  if (score > 0) return "text-green-600";
  if (score < 0) return "text-red-600";
  return "text-gray-500";
};

const formatScore = (score: number) => (score > 0 ? `+${score}` : `${score}`);

const recommendationBadge = (value: string) => {
  switch (value) {
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
</script>
