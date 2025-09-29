<template>
  <div class="h-full flex flex-col">
    <div class="flex-1 bg-gray-50 rounded-lg p-4 mb-4 overflow-y-auto">
      <div class="space-y-4">
        <div
          v-for="message in expertChatMessages"
          :key="message.id"
          class="flex items-start gap-3"
        >
          <div
            class="w-8 h-8 rounded-full bg-[rgb(var(--color-nepse-primary))] text-white flex items-center justify-center text-sm font-semibold flex-shrink-0"
          >
            {{ message.sender.charAt(0) }}
          </div>
          <div class="flex-1">
            <div class="flex items-center gap-2 mb-1">
              <span class="font-semibold text-gray-800">{{
                message.sender
              }}</span>
              <span v-if="message.verified" class="text-blue-500">
                <VerifiedIcon class="w-4 h-4" />
              </span>
              <span class="text-xs text-gray-500">{{
                message.time
              }}</span>
            </div>
            <div class="text-gray-700 text-sm">{{ message.content }}</div>
            <div
              v-if="message.analysis"
              class="mt-2 p-3 bg-blue-50 rounded-lg border border-blue-200"
            >
              <div class="text-xs text-blue-800 font-semibold mb-1">
                Market Analysis
              </div>
              <div class="text-sm text-blue-700">
                {{ message.analysis }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="flex gap-2">
      <input
        v-model="expertMessage"
        @keyup.enter="sendExpertMessage"
        type="text"
        placeholder="Ask the experts..."
        class="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[rgb(var(--color-nepse-primary))] focus:border-transparent"
      />
      <button
        @click="sendExpertMessage"
        class="px-6 py-2 bg-[rgb(var(--color-nepse-primary))] text-white rounded-lg hover:bg-blue-700 transition-colors"
      >
        Send
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from "vue";
import VerifiedIcon from "./icons/VerifiedIcon.vue";

const expertMessage = ref("");

const expertChatMessages = reactive([
  {
    id: 1,
    sender: "Dr. Sharma",
    verified: true,
    content:
      "Banking sector showing strong accumulation patterns. Volume analysis suggests institutional buying.",
    analysis:
      "Key resistance at 1,250 for NABIL. Break above this level could trigger momentum rally to 1,350.",
    time: "2 hours ago",
  },
  {
    id: 2,
    sender: "TradeGuru",
    verified: true,
    content:
      "Hydropower stocks are forming a sector rotation play. Watch for breakouts in UPPER and CHCL.",
    time: "1 hour ago",
  },
]);

const sendExpertMessage = () => {
  if (expertMessage.value.trim()) {
    expertChatMessages.push({
      id: Date.now(),
      sender: "You",
      verified: false,
      content: expertMessage.value,
      time: "now",
    });
    expertMessage.value = "";
  }
};
</script>
