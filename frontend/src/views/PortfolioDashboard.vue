<template>
  <div class="space-y-6">
    <!-- Portfolio Overview -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
      <div class="bg-white rounded-lg shadow p-6 text-center">
        <h3 class="text-sm font-medium text-gray-500">Total Value</h3>
        <p class="text-2xl font-bold text-gray-900">NPR 1,250,000</p>
        <p class="text-sm text-green-600 mt-1">+2.5% today</p>
      </div>
      <div class="bg-white rounded-lg shadow p-6 text-center">
        <h3 class="text-sm font-medium text-gray-500">Day's Gain/Loss</h3>
        <p class="text-2xl font-bold text-green-600">+NPR 30,500</p>
        <p class="text-sm text-gray-500 mt-1">+2.5%</p>
      </div>
      <div class="bg-white rounded-lg shadow p-6 text-center">
        <h3 class="text-sm font-medium text-gray-500">Total Holdings</h3>
        <p class="text-2xl font-bold text-gray-900">12</p>
        <p class="text-sm text-gray-500 mt-1">stocks</p>
      </div>
      <div class="bg-white rounded-lg shadow p-6 text-center">
        <h3 class="text-sm font-medium text-gray-500">Cash Balance</h3>
        <p class="text-2xl font-bold text-gray-900">NPR 85,000</p>
        <p class="text-sm text-gray-500 mt-1">Available</p>
      </div>
    </div>

    <!-- Holdings Table -->
    <div class="bg-white rounded-lg shadow">
      <div class="px-6 py-4 border-b border-gray-200">
        <h2 class="text-xl font-bold text-gray-800">Your Holdings</h2>
      </div>
      <div class="overflow-x-auto">
        <table class="min-w-full">
          <thead class="bg-gray-50">
            <tr>
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase"
              >
                Symbol
              </th>
              <th
                class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase"
              >
                Quantity
              </th>
              <th
                class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase"
              >
                Avg Cost
              </th>
              <th
                class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase"
              >
                Current Price
              </th>
              <th
                class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase"
              >
                Market Value
              </th>
              <th
                class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase"
              >
                Gain/Loss
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <!-- Sample holdings data -->
            <tr>
              <td
                class="px-6 py-4 whitespace-nowrap font-semibold text-gray-900"
              >
                NABIL
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right text-gray-900">
                100
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right text-gray-900">
                1,200
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right text-gray-900">
                1,350
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right text-gray-900">
                135,000
              </td>
              <td
                class="px-6 py-4 whitespace-nowrap text-right font-semibold text-green-600"
              >
                +15,000 (+12.5%)
              </td>
            </tr>
            <tr>
              <td
                class="px-6 py-4 whitespace-nowrap font-semibold text-gray-900"
              >
                NEPSE
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right text-gray-900">
                50
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right text-gray-900">
                2,800
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right text-gray-900">
                2,650
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right text-gray-900">
                132,500
              </td>
              <td
                class="px-6 py-4 whitespace-nowrap text-right font-semibold text-red-600"
              >
                -7,500 (-5.4%)
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Portfolio Allocation Chart -->
    <div class="bg-white rounded-lg shadow p-6">
      <h2 class="text-xl font-bold text-gray-800 mb-4">Portfolio Allocation</h2>
      <div class="text-center py-20 text-gray-500">
        Portfolio Pie Chart Component
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// Portfolio dashboard logic
</script>
