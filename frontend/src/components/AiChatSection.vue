<template>
  <div class="h-full min-h-0 flex flex-col">
    <div class="flex-1 bg-gray-50 rounded-lg p-4 mb-4 overflow-y-auto">
      <div class="space-y-4">
        <div
          v-for="message in aiChatMessages"
          :key="message.id"
          :class="[
            'flex',
            message.type === 'user' ? 'justify-end' : 'justify-start',
          ]"
        >
          <div
            :class="[
              'w-full max-w-xl px-4 py-3 rounded-lg',
              message.type === 'user'
                ? 'bg-[rgb(var(--color-nepse-primary))] text-white'
                : 'bg-white text-gray-800 shadow-sm border',
            ]"
          >
            <div
              v-if="message.type === 'ai'"
              class="flex items-center gap-2 mb-2"
            >
              <SparklesIcon
                class="w-4 h-4 text-[rgb(var(--color-nepse-primary))]"
              />
              <span class="font-semibold text-sm">NEPSE AI Assistant</span>
              <span
                v-if="message.confidence"
                class="ml-auto text-xs text-gray-500"
              >
                Confidence: {{ message.confidence }}
              </span>
            </div>
            <div v-if="message.isLoading" class="text-sm italic text-gray-500">
              Analyzing latest market context...
            </div>
            <div v-else class="text-sm whitespace-pre-line">
              {{ message.content }}
            </div>
            <div
              v-if="!message.isLoading && message.details?.keyInsights?.length"
              class="mt-3 text-xs"
            >
              <h4 class="font-semibold text-gray-700 mb-1">Key Insights</h4>
              <ul class="space-y-1">
                <li
                  v-for="(insight, index) in message.details.keyInsights"
                  :key="index"
                  class="flex items-start gap-2"
                >
                  <span
                    class="mt-1 h-1.5 w-1.5 rounded-full bg-[rgb(var(--color-nepse-primary))]"
                  ></span>
                  <span>{{ insight }}</span>
                </li>
              </ul>
            </div>
            <div
              v-if="!message.isLoading && message.details?.recommendation"
              class="mt-3 p-3 bg-gray-50 rounded text-xs"
            >
              <strong class="text-gray-700">Recommendation:</strong>
              <span class="ml-1">{{ message.details.recommendation }}</span>
            </div>
            <div
              v-if="!message.isLoading && message.details?.riskFactors"
              class="mt-3 text-xs text-gray-600"
            >
              <strong>Risk Factors:</strong>
              <span class="ml-1">{{ message.details.riskFactors }}</span>
            </div>
            <div
              v-if="
                !message.isLoading &&
                message.details?.stockMetrics &&
                Object.keys(message.details.stockMetrics).length
              "
              class="mt-3 text-xs"
            >
              <h4 class="font-semibold text-gray-700 mb-1">Stock Breakdown</h4>
              <div
                v-for="(metrics, symbol) in message.details.stockMetrics"
                :key="symbol"
                class="mb-2 last:mb-0"
              >
                <div class="font-semibold text-gray-800">{{ symbol }}</div>
                <div class="grid grid-cols-2 gap-2 mt-1">
                  <div class="bg-gray-50 rounded p-2">
                    <div class="text-[10px] text-gray-500 uppercase">
                      Overall
                    </div>
                    <div class="font-semibold">{{ metrics.overall_score }}</div>
                  </div>
                  <div class="bg-gray-50 rounded p-2">
                    <div class="text-[10px] text-gray-500 uppercase">
                      Recommendation
                    </div>
                    <div class="font-semibold">
                      {{ metrics.recommendation }}
                    </div>
                  </div>
                  <div class="bg-gray-50 rounded p-2">
                    <div class="text-[10px] text-gray-500 uppercase">
                      Technical
                    </div>
                    <div class="font-semibold">
                      {{ metrics.technical_score }}
                    </div>
                  </div>
                  <div class="bg-gray-50 rounded p-2">
                    <div class="text-[10px] text-gray-500 uppercase">
                      Fundamental
                    </div>
                    <div class="font-semibold">
                      {{ metrics.fundamental_score }}
                    </div>
                  </div>
                  <div class="bg-gray-50 rounded p-2 col-span-2">
                    <div class="text-[10px] text-gray-500 uppercase">Macro</div>
                    <div class="font-semibold">{{ metrics.macro_score }}</div>
                  </div>
                </div>
              </div>
            </div>
            <div
              v-if="message.suggestion && !message.isLoading"
              class="mt-2 p-2 bg-gray-50 rounded text-xs"
            >
              <strong>Suggestion:</strong> {{ message.suggestion }}
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="flex gap-2">
      <input
        v-model="aiMessage"
        @keyup.enter="sendAiMessage"
        :disabled="isSubmitting"
        type="text"
        placeholder="Ask me anything about the market in plain language..."
        class="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[rgb(var(--color-nepse-primary))] focus:border-transparent disabled:bg-gray-100 disabled:cursor-not-allowed"
      />
      <button
        @click="sendAiMessage"
        :disabled="isSubmitting || !aiMessage.trim()"
        class="px-6 py-2 bg-gradient-to-r from-[rgb(var(--color-nepse-primary))] to-[rgb(var(--color-nepse-secondary))] text-white rounded-lg hover:opacity-90 transition-opacity disabled:opacity-60 disabled:cursor-not-allowed"
      >
        <SparklesIcon class="w-4 h-4 inline mr-2" />
        <span v-if="!isSubmitting">Ask AI</span>
        <span v-else>Thinking…</span>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import SparklesIcon from "./icons/SparklesIcon.vue";
import { askAgentQuestion } from "@/services/agent";

type MessageType = "user" | "ai" | "system";

interface ChatMessage {
  id: number;
  type: MessageType;
  content: string;
  confidence?: string;
  suggestion?: string;
  isLoading?: boolean;
  details?: {
    keyInsights?: string[];
    recommendation?: string;
    riskFactors?: string;
    stockMetrics?: Record<
      string,
      {
        overall_score: number;
        technical_score: number;
        fundamental_score: number;
        macro_score: number;
        recommendation: string;
      }
    >;
  };
}

const aiMessage = ref("");
const isSubmitting = ref(false);
const aiChatMessages = ref<ChatMessage[]>([
  {
    id: 1,
    type: "ai",
    content:
      "Hello! I'm your NEPSE AI assistant. I can help you analyze market data, explain technical indicators, and provide investment insights. What would you like to know?",
    suggestion:
      'Try asking "What stocks are showing bullish signals today?" or "Explain RSI indicator"',
  },
]);

const sendAiMessage = async () => {
  const trimmedMessage = aiMessage.value.trim();
  if (!trimmedMessage || isSubmitting.value) {
    return;
  }

  const userMessage: ChatMessage = {
    id: Date.now(),
    type: "user",
    content: trimmedMessage,
  };

  aiChatMessages.value.push(userMessage);
  aiMessage.value = "";

  const loadingMessage: ChatMessage = {
    id: Date.now() + 1,
    type: "ai",
    content: "",
    isLoading: true,
  };

  aiChatMessages.value.push(loadingMessage);
  isSubmitting.value = true;

  try {
    const response = await askAgentQuestion(trimmedMessage);
    const structured = response.structured_response;

    loadingMessage.content = structured?.quick_answer || response.answer;
    loadingMessage.confidence = response.confidence;
    loadingMessage.details = structured
      ? {
          keyInsights: structured.key_insights,
          recommendation: structured.recommendation,
          riskFactors: structured.risk_factors,
          stockMetrics: structured.stock_metrics,
        }
      : undefined;
    loadingMessage.suggestion =
      response.related_stocks.length && structured?.recommendation
        ? `Related stocks: ${response.related_stocks.join(", ")}`
        : undefined;
  } catch (error: unknown) {
    const message =
      error instanceof Error
        ? error.message
        : "Sorry, I couldn't process that request. Please try again.";
    loadingMessage.type = "system";
    loadingMessage.content = message;
    loadingMessage.suggestion =
      "Check the question phrasing or try again shortly.";
  } finally {
    loadingMessage.isLoading = false;
    isSubmitting.value = false;
  }
};
</script>
