<template>
  <div class="space-y-6">
    <div
      class="bg-gradient-to-r from-purple-50 to-blue-50 p-6 rounded-xl"
    >
      <h3 class="text-lg font-semibold text-gray-800 mb-4">
        SME Platform Overview
      </h3>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div class="text-center p-4 bg-white rounded-lg">
          <div class="text-2xl font-bold text-purple-600">
            {{ smeStats.totalCompanies }}
          </div>
          <div class="text-sm text-gray-600">Listed Companies</div>
        </div>
        <div class="text-center p-4 bg-white rounded-lg">
          <div class="text-2xl font-bold text-blue-600">
            {{ smeStats.totalVolume }}
          </div>
          <div class="text-sm text-gray-600">Total Volume</div>
        </div>
        <div class="text-center p-4 bg-white rounded-lg">
          <div class="text-2xl font-bold text-green-600">
            {{ smeStats.totalTurnover }}
          </div>
          <div class="text-sm text-gray-600">Total Turnover</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive } from "vue";

const smeStats = reactive({
  totalCompanies: 45,
  totalVolume: "2.5M",
  totalTurnover: "Rs. 850M",
});
</script>
