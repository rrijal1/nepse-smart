<template>
  <div class="h-full flex flex-col">
    <div class="flex-1 bg-gray-50 rounded-lg p-4 mb-4 overflow-y-auto">
      <div class="space-y-4">
        <div
          v-for="message in chatMessages"
          :key="message.id"
          :class="[
            'flex',
            message.type === 'user' ? 'justify-end' : 'justify-start',
          ]"
        >
          <div
            :class="[
              'max-w-xs lg:max-w-md px-4 py-2 rounded-lg',
              message.type === 'user'
                ? 'bg-[rgb(var(--color-nepse-primary))] text-white'
                : 'bg-white text-gray-800 shadow-sm',
            ]"
          >
            <div class="font-medium text-sm mb-1">
              {{ message.sender }}
            </div>
            <div class="text-sm">{{ message.content }}</div>
            <div class="text-xs opacity-70 mt-1">{{ message.time }}</div>
          </div>
        </div>
      </div>
    </div>
    <div class="flex gap-2">
      <input
        v-model="newMessage"
        @keyup.enter="sendMessage"
        type="text"
        placeholder="Share your market insights..."
        class="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[rgb(var(--color-nepse-primary))] focus:border-transparent"
      />
      <button
        @click="sendMessage"
        class="px-6 py-2 bg-[rgb(var(--color-nepse-primary))] text-white rounded-lg hover:bg-blue-700 transition-colors"
      >
        Send
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from "vue";

const newMessage = ref("");

const chatMessages = reactive([
  {
    id: 1,
    type: "other",
    sender: "TraderPro",
    content: "Anyone watching NABIL today? Strong volume!",
    time: "10:30 AM",
  },
  {
    id: 2,
    type: "user",
    sender: "You",
    content: "Yes, looks like it might break resistance at 1250",
    time: "10:32 AM",
  },
  {
    id: 3,
    type: "other",
    sender: "MarketGuru",
    content: "Banking sector overall looking bullish this week",
    time: "10:35 AM",
  },
]);

const sendMessage = () => {
  if (newMessage.value.trim()) {
    chatMessages.push({
      id: Date.now(),
      type: "user",
      sender: "You",
      content: newMessage.value,
      time: new Date().toLocaleTimeString("en-US", {
        hour: "2-digit",
        minute: "2-digit",
      }),
    });
    newMessage.value = "";
  }
};
</script>
