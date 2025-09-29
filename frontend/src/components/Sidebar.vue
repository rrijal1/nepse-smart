<template>
  <div class="w-80 bg-white shadow-lg rounded-lg mr-6 overflow-hidden">
    <div
      class="p-4 bg-gradient-to-r from-[rgb(var(--color-nepse-primary))] to-[rgb(var(--color-nepse-secondary))] text-white"
    >
      <h2 class="text-lg font-semibold">Market Overview</h2>
    </div>

    <!-- Navigation Menu -->
    <nav class="p-2">
      <div class="space-y-1">
        <button
          v-for="item in sidebarItems"
          :key="item.id"
          @click="$emit('update:activeSection', item.id)"
          :class="[
            'w-full flex items-center gap-3 px-4 py-3 text-left rounded-lg transition-all duration-200',
            activeSection === item.id
              ? 'bg-[rgb(var(--color-nepse-primary))]/10 text-[rgb(var(--color-nepse-primary))] font-semibold border-l-4 border-[rgb(var(--color-nepse-primary))]'
              : 'text-gray-700 hover:bg-gray-50 hover:text-[rgb(var(--color-nepse-primary))]',
          ]"
        >
          <component :is="item.icon" class="w-5 h-5" />
          <span>{{ item.label }}</span>
          <span
            v-if="item.badge"
            class="ml-auto bg-red-500 text-white text-xs px-2 py-1 rounded-full"
          >
            {{ item.badge }}
          </span>
        </button>
      </div>
    </nav>
  </div>
</template>

<script setup lang="ts">
import { defineProps, defineEmits } from 'vue';

defineProps<{ activeSection: string, sidebarItems: any[] }>();
defineEmits(['update:activeSection']);

</script>
