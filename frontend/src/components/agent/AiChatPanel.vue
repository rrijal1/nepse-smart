<template>
  <div class="flex h-full flex-col">
    <div class="flex-1 overflow-y-auto rounded-lg bg-white p-4 shadow-sm">
      <div class="space-y-4">
        <div
          v-for="message in messages"
          :key="message.id"
          :class="[
            'flex w-full',
            message.role === 'user' ? 'justify-end' : 'justify-start',
          ]"
        >
          <div
            :class="[
              'max-w-[85%] rounded-lg px-4 py-3 text-sm',
              message.role === 'user'
                ? 'bg-[rgb(var(--color-nepse-primary))] text-white'
                : 'bg-gray-50 text-gray-800 border border-gray-200 shadow-sm',
            ]"
          >
            <div
              class="flex items-center justify-between gap-3 text-xs text-gray-500"
            >
              <span class="uppercase tracking-wide font-semibold">{{
                message.role === "user" ? "You" : "Agent"
              }}</span>
              <span>{{ formatTimestamp(message.timestamp) }}</span>
            </div>
            <p class="mt-2 whitespace-pre-line">
              {{ message.content }}
            </p>

            <div v-if="message.structured" class="mt-4 space-y-3 text-xs">
              <div
                v-if="message.structured.quick_answer"
                class="rounded-md border border-blue-200 bg-blue-50 p-3 text-blue-800"
              >
                <h4 class="mb-1 font-semibold uppercase tracking-wide">
                  Quick Answer
                </h4>
                <p class="leading-relaxed">
                  {{ message.structured.quick_answer }}
                </p>
              </div>

              <div v-if="message.structured.key_insights?.length">
                <h4 class="font-semibold uppercase tracking-wide text-gray-600">
                  Key Insights
                </h4>
                <ul class="list-disc space-y-1 pl-4 text-gray-600">
                  <li
                    v-for="insight in message.structured.key_insights"
                    :key="insight"
                  >
                    {{ insight }}
                  </li>
                </ul>
              </div>

              <div v-if="message.structured.recommendation">
                <h4 class="font-semibold uppercase tracking-wide text-gray-600">
                  Recommendation
                </h4>
                <p class="text-gray-600">
                  {{ message.structured.recommendation }}
                </p>
              </div>

              <div v-if="message.structured.risk_factors">
                <h4 class="font-semibold uppercase tracking-wide text-gray-600">
                  Risk Factors
                </h4>
                <p class="text-gray-600">
                  {{ message.structured.risk_factors }}
                </p>
              </div>

              <div
                v-if="message.metadata"
                class="grid grid-cols-1 gap-2 rounded-md border border-gray-200 p-3 text-gray-600 sm:grid-cols-2"
              >
                <div v-if="message.metadata.confidence">
                  Confidence:
                  <span :class="confidenceColor(message.metadata.confidence)">
                    {{ message.metadata.confidence }}
                  </span>
                </div>
                <div v-if="message.metadata.processingTime">
                  Response Time: {{ message.metadata.processingTime }} ms
                </div>
                <div v-if="message.metadata.relatedStocks?.length">
                  Stocks: {{ message.metadata.relatedStocks.join(", ") }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div
      v-if="error"
      class="mt-3 rounded-md bg-red-50 p-3 text-xs text-red-600"
    >
      {{ error }}
    </div>

    <div class="mt-3 flex items-center gap-2">
      <input
        v-model="question"
        @keyup.enter="emitAsk"
        type="text"
        placeholder="Ask about NEPSE stocks, strategies, or comparisons..."
        class="flex-1 rounded-lg border border-gray-300 px-4 py-2 text-sm focus:border-transparent focus:ring-2 focus:ring-[rgb(var(--color-nepse-primary))]"
        :disabled="isLoading"
      />
      <button
        @click="emitAsk"
        :disabled="isLoading || !question.trim()"
        class="rounded-lg bg-gradient-to-r from-[rgb(var(--color-nepse-primary))] to-[rgb(var(--color-nepse-secondary))] px-4 py-2 text-sm font-semibold text-white transition hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-60"
      >
        <span v-if="!isLoading">Ask</span>
        <span v-else class="flex items-center gap-2">
          <span
            class="h-4 w-4 animate-spin rounded-full border-b-2 border-white"
          ></span>
          Thinking...
        </span>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from "vue";

interface ChatMessageMeta {
  confidence?: string;
  relatedStocks?: string[];
  processingTime?: number;
}

interface StructuredPayload {
  quick_answer?: string;
  key_insights?: string[];
  recommendation?: string;
  risk_factors?: string;
}

export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  structured?: StructuredPayload | null;
  metadata?: ChatMessageMeta;
  timestamp: string;
}

const props = defineProps<{
  messages: ChatMessage[];
  isLoading: boolean;
  error: string | null;
}>();

const emit = defineEmits<{
  (e: "ask", value: string): void;
}>();

const question = ref("");

const emitAsk = () => {
  if (!question.value.trim() || props.isLoading) return;
  emit("ask", question.value);
  question.value = "";
};

const formatTimestamp = (timestamp: string) => {
  try {
    return new Date(timestamp).toLocaleTimeString();
  } catch (error) {
    return timestamp;
  }
};

const confidenceColor = (confidence: string) => {
  switch (confidence) {
    case "High":
      return "text-green-600 font-semibold";
    case "Medium":
      return "text-yellow-600 font-semibold";
    case "Low":
      return "text-red-600 font-semibold";
    default:
      return "text-gray-600";
  }
};

const messages = computed(() => props.messages);
const isLoading = computed(() => props.isLoading);
const error = computed(() => props.error);
</script>
