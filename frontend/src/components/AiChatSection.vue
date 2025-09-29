<template>
  <div class="h-full flex flex-col">
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
              'max-w-md px-4 py-3 rounded-lg',
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
              <span class="font-semibold text-sm"
                >NEPSE AI Assistant</span
              >
            </div>
            <div class="text-sm">{{ message.content }}</div>
            <div
              v-if="message.suggestion"
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
        type="text"
        placeholder="Ask me anything about the market in plain language..."
        class="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[rgb(var(--color-nepse-primary))] focus:border-transparent"
      />
      <button
        @click="sendAiMessage"
        class="px-6 py-2 bg-gradient-to-r from-[rgb(var(--color-nepse-primary))] to-[rgb(var(--color-nepse-secondary))] text-white rounded-lg hover:opacity-90 transition-opacity"
      >
        <SparklesIcon class="w-4 h-4 inline mr-2" />
        Ask AI
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from "vue";
import SparklesIcon from "./icons/SparklesIcon.vue";

const aiMessage = ref("");

const aiChatMessages = reactive([
  {
    id: 1,
    type: "ai",
    content:
      "Hello! I'm your NEPSE AI assistant. I can help you analyze market data, explain technical indicators, and provide investment insights. What would you like to know?",
    suggestion:
      'Try asking "What stocks are showing bullish signals today?" or "Explain RSI indicator"',
  },
]);

const sendAiMessage = () => {
  if (aiMessage.value.trim()) {
    aiChatMessages.push({
      id: Date.now(),
      type: "user",
      content: aiMessage.value,
      suggestion: "",
    });

    // Simulate AI response
    setTimeout(() => {
      aiChatMessages.push({
        id: Date.now() + 1,
        type: "ai",
        content:
          "Based on current market data, I can provide insights on that topic. Let me analyze the latest information for you.",
        suggestion:
          "Would you like me to analyze specific stocks or market sectors?",
      });
    }, 1000);

    aiMessage.value = "";
  }
};
</script>
