<template>
  <div class="space-y-6">
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div
        v-for="ipo in ipoList"
        :key="ipo.company"
        class="bg-gradient-to-br from-blue-50 to-white p-6 rounded-xl shadow-sm border"
      >
        <div class="flex items-center justify-between mb-4">
          <h3 class="font-semibold text-gray-800">{{ ipo.company }}</h3>
          <span
            :class="[
              'px-3 py-1 rounded-full text-xs font-medium',
              ipo.status === 'Open'
                ? 'bg-green-100 text-green-800'
                : ipo.status === 'Upcoming'
                ? 'bg-blue-100 text-blue-800'
                : 'bg-gray-100 text-gray-800',
            ]"
          >
            {{ ipo.status }}
          </span>
        </div>
        <div class="space-y-2 text-sm">
          <div class="flex justify-between">
            <span class="text-gray-600">Issue Size:</span>
            <span class="font-semibold">{{ ipo.issueSize }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-gray-600">Price Range:</span>
            <span class="font-semibold">{{ ipo.priceRange }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-gray-600">Open Date:</span>
            <span class="font-semibold">{{ ipo.openDate }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-gray-600">Close Date:</span>
            <span class="font-semibold">{{ ipo.closeDate }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive } from "vue";

const ipoList = reactive([
  {
    company: "ABC Banking Ltd.",
    status: "Open",
    issueSize: "1,00,000 shares",
    priceRange: "Rs. 100-120",
    openDate: "2025-09-25",
    closeDate: "2025-10-05",
  },
  {
    company: "XYZ Insurance Co.",
    status: "Upcoming",
    issueSize: "75,000 shares",
    priceRange: "Rs. 200-250",
    openDate: "2025-10-10",
    closeDate: "2025-10-20",
  },
  {
    company: "Nepal Hydro Power",
    status: "Closed",
    issueSize: "2,00,000 shares",
    priceRange: "Rs. 80-100",
    openDate: "2025-09-10",
    closeDate: "2025-09-20",
  },
]);
</script>
