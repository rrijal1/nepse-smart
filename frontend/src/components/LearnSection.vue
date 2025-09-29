<template>
  <div class="space-y-6">
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div
        v-for="resource in learningResources"
        :key="resource.id"
        class="bg-white p-6 rounded-xl shadow-sm border hover:shadow-md transition-shadow cursor-pointer"
      >
        <div class="flex items-center gap-3 mb-4">
          <component
            :is="resource.icon"
            class="w-8 h-8 text-[rgb(var(--color-nepse-primary))]"
          />
          <h3 class="font-semibold text-gray-800">
            {{ resource.title }}
          </h3>
        </div>
        <p class="text-gray-600 text-sm mb-4">
          {{ resource.description }}
        </p>
        <div class="flex items-center justify-between">
          <span class="text-xs text-gray-500">{{
            resource.duration
          }}</span>
          <button
            class="text-[rgb(var(--color-nepse-primary))] text-sm font-medium hover:underline"
          >
            Start Learning →
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive } from "vue";
import BookIcon from "./icons/BookIcon.vue";
import ChartIcon from "./icons/ChartIcon.vue";
import VideoIcon from "./icons/VideoIcon.vue";

const learningResources = reactive([
  {
    id: 1,
    title: "Stock Market Basics",
    description: "Learn fundamental concepts of stock market investing",
    duration: "45 min",
    icon: BookIcon,
  },
  {
    id: 2,
    title: "Technical Analysis",
    description: "Master chart patterns and technical indicators",
    duration: "1.5 hours",
    icon: ChartIcon,
  },
  {
    id: 3,
    title: "Video Tutorial Series",
    description: "Comprehensive video course on NEPSE trading",
    duration: "3 hours",
    icon: VideoIcon,
  },
  {
    id: 4,
    title: "Risk Management",
    description: "Essential strategies for managing investment risks",
    duration: "30 min",
    icon: BookIcon,
  },
]);
</script>
