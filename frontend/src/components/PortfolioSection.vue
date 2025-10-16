<template>
  <div class="space-y-6">
    <!-- Loading State -->
    <div v-if="loading" class="text-center py-8">
      <div
        class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"
      ></div>
      <p class="mt-2 text-gray-600">Loading...</p>
    </div>

    <!-- Error State -->
    <div
      v-if="error"
      class="bg-red-50 border border-red-200 rounded-lg p-4 mb-6"
    >
      <p class="text-red-700">{{ error }}</p>
      <button
        @click="loadData"
        class="mt-2 text-sm text-red-600 hover:text-red-800 underline"
      >
        Retry
      </button>
    </div>

    <!-- Portfolio Summary Cards -->
    <div
      v-if="portfolioSummary && !loading"
      class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 mb-6"
    >
      <div
        class="bg-gradient-to-br from-green-50 to-green-100 p-6 rounded-xl border border-green-200"
      >
        <div class="flex items-center justify-between mb-4">
          <h3 class="font-semibold text-green-800">Total Portfolio</h3>
          <TrendingUpIcon class="w-5 h-5 text-green-600" />
        </div>
        <div class="text-2xl font-bold text-green-700">
          {{ formatCurrency(portfolioSummary.current_value) }}
        </div>
        <div
          class="text-sm mt-1"
          :class="
            portfolioSummary.total_pnl >= 0 ? 'text-green-600' : 'text-red-600'
          "
        >
          {{ formatCurrency(portfolioSummary.total_pnl) }} ({{
            formatPercent(portfolioSummary.total_pnl_percent)
          }})
        </div>
      </div>

      <div
        class="bg-gradient-to-br from-blue-50 to-blue-100 p-6 rounded-xl border border-blue-200"
      >
        <div class="flex items-center justify-between mb-4">
          <h3 class="font-semibold text-blue-800">Day's P&L</h3>
          <ChartIcon class="w-5 h-5 text-blue-600" />
        </div>
        <div
          class="text-2xl font-bold"
          :class="
            portfolioSummary.day_pnl >= 0 ? 'text-blue-700' : 'text-red-700'
          "
        >
          {{ formatCurrency(portfolioSummary.day_pnl) }}
        </div>
        <div
          class="text-sm mt-1"
          :class="
            portfolioSummary.day_pnl_percent >= 0
              ? 'text-blue-600'
              : 'text-red-600'
          "
        >
          {{ formatPercent(portfolioSummary.day_pnl_percent) }} today
        </div>
      </div>

      <div
        class="bg-gradient-to-br from-purple-50 to-purple-100 p-6 rounded-xl border border-purple-200"
      >
        <div class="flex items-center justify-between mb-4">
          <h3 class="font-semibold text-purple-800">Total Invested</h3>
          <WalletIcon class="w-5 h-5 text-purple-600" />
        </div>
        <div class="text-2xl font-bold text-purple-700">
          {{ formatCurrency(portfolioSummary.total_invested) }}
        </div>
        <div class="text-sm text-purple-600 mt-1">Total investment</div>
      </div>
    </div>

    <!-- Holdings Table -->
    <div class="bg-white border border-gray-200 rounded-xl overflow-hidden">
      <div class="px-6 py-4 border-b border-gray-200 bg-gray-50">
        <h3 class="text-lg font-semibold text-gray-800">Current Holdings</h3>
      </div>
      <div class="overflow-x-auto">
        <table class="min-w-full">
          <thead class="bg-gray-50 border-b border-gray-200">
            <tr>
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Stock
              </th>
              <th
                class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Quantity
              </th>
              <th
                class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Avg Price
              </th>
              <th
                class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Current Price
              </th>
              <th
                class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                P&L
              </th>
              <th
                class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                % Change
              </th>
              <th
                class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Actions
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr
              v-for="holding in portfolioHoldings"
              :key="holding.symbol"
              class="hover:bg-gray-50"
            >
              <td
                class="px-6 py-4 whitespace-nowrap font-semibold text-gray-900"
              >
                {{ holding.symbol }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right font-mono">
                {{ holding.quantity }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right font-mono">
                Rs. {{ (holding.avg_price || 0).toLocaleString() }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right font-mono">
                Rs. {{ (holding.current_price || 0).toLocaleString() }}
              </td>
              <td
                class="px-6 py-4 whitespace-nowrap text-right font-mono font-semibold"
                :class="
                  (holding.pnl || 0) >= 0 ? 'text-green-600' : 'text-red-600'
                "
              >
                {{ (holding.pnl || 0) >= 0 ? "+" : "" }}Rs.
                {{ Math.abs(holding.pnl || 0).toLocaleString() }}
              </td>
              <td
                class="px-6 py-4 whitespace-nowrap text-right font-mono font-semibold"
                :class="
                  (holding.pnl_percent || 0) >= 0
                    ? 'text-green-600'
                    : 'text-red-600'
                "
              >
                {{ (holding.pnl_percent || 0) >= 0 ? "+" : ""
                }}{{ (holding.pnl_percent || 0).toFixed(2) }}%
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-center space-x-2">
                <button
                  @click="openEditModal(holding)"
                  class="text-blue-600 hover:text-blue-800 text-sm font-medium"
                  title="Edit Holding"
                >
                  Edit
                </button>
                <button
                  @click="deleteHolding(holding.id)"
                  class="text-red-600 hover:text-red-800 text-sm font-medium"
                  title="Delete Holding"
                >
                  Delete
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Edit Holding Modal -->
    <div
      v-if="showEditModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
      @click.self="closeEditModal"
    >
      <div class="bg-white rounded-lg p-6 max-w-md w-full mx-4">
        <h3 class="text-lg font-semibold mb-4">
          Edit {{ editForm.symbol }} Holding
        </h3>

        <form @submit.prevent="submitEdit" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1"
              >Symbol</label
            >
            <input
              v-model="editForm.symbol"
              type="text"
              readonly
              class="w-full px-3 py-2 border border-gray-300 rounded-lg bg-gray-50"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1"
              >Quantity
              <span class="text-xs text-gray-500"
                >(Set to 0 to remove)</span
              ></label
            >
            <input
              v-model.number="editForm.quantity"
              type="number"
              min="0"
              required
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1"
              >Average Price (Rs.)</label
            >
            <input
              v-model.number="editForm.avg_price"
              type="number"
              step="0.01"
              min="0"
              required
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1"
              >Buy Date</label
            >
            <input
              v-model="editForm.buy_date"
              type="date"
              required
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1"
              >Notes (Optional)</label
            >
            <textarea
              v-model="editForm.notes"
              rows="2"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            ></textarea>
          </div>

          <div class="flex space-x-3 pt-4">
            <button
              type="submit"
              class="flex-1 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
            >
              Update Holding
            </button>
            <button
              type="button"
              @click="closeEditModal"
              class="flex-1 bg-gray-200 text-gray-800 px-4 py-2 rounded-lg hover:bg-gray-300"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import TrendingUpIcon from "./icons/TrendingUpIcon.vue";
import ChartIcon from "./icons/ChartIcon.vue";
import WalletIcon from "./icons/WalletIcon.vue";
import {
  fetchPortfolio,
  fetchPortfolioSummary,
  updatePortfolioHolding,
  removeFromPortfolio,
  type PortfolioHolding,
  type PortfolioSummary,
} from "../services/portfolio";

const portfolioHoldings = ref<PortfolioHolding[]>([]);
const portfolioSummary = ref<PortfolioSummary | null>(null);
const loading = ref(false);
const error = ref<string | null>(null);
const showEditModal = ref(false);
const editForm = ref({
  id: 0,
  symbol: "",
  quantity: 0,
  avg_price: 0,
  buy_date: "",
  notes: "",
});

onMounted(async () => {
  await loadData();
});

const loadData = async () => {
  loading.value = true;
  error.value = null;
  try {
    const [holdings, summary] = await Promise.all([
      fetchPortfolio(),
      fetchPortfolioSummary(),
    ]);
    portfolioHoldings.value = holdings;
    portfolioSummary.value = summary;
  } catch (err: any) {
    error.value = err.message || "Failed to load portfolio data";
    console.error("Error loading portfolio data:", err);
  } finally {
    loading.value = false;
  }
};

// Smart currency formatter - abbreviates large numbers to prevent overflow
const formatCurrency = (value: number | null | undefined): string => {
  if (value === null || value === undefined) return "N/A";

  const absValue = Math.abs(value);
  const sign = value < 0 ? "-" : "";

  // Format in Crores (Cr) for values >= 1 crore (10 million)
  if (absValue >= 10000000) {
    return `${sign}Rs. ${(absValue / 10000000).toFixed(2)}Cr`;
  }
  // Format in Lakhs (L) for values >= 1 lakh (100,000)
  else if (absValue >= 100000) {
    return `${sign}Rs. ${(absValue / 100000).toFixed(2)}L`;
  }
  // Format in thousands (K) for values >= 10,000
  else if (absValue >= 10000) {
    return `${sign}Rs. ${(absValue / 1000).toFixed(1)}K`;
  }
  // Normal formatting for smaller values
  else {
    return `${sign}Rs. ${absValue.toLocaleString("en-IN", {
      maximumFractionDigits: 2,
    })}`;
  }
};

const formatPercent = (value: number | null | undefined): string => {
  if (value === null || value === undefined) return "N/A";
  const sign = value >= 0 ? "+" : "";
  return `${sign}${value.toFixed(2)}%`;
};

// Edit Modal Functions
const openEditModal = (holding: PortfolioHolding) => {
  editForm.value = {
    id: holding.id,
    symbol: holding.symbol,
    quantity: holding.quantity,
    avg_price: holding.avg_price,
    buy_date: holding.buy_date,
    notes: holding.notes || "",
  };
  showEditModal.value = true;
};

const closeEditModal = () => {
  showEditModal.value = false;
  editForm.value = {
    id: 0,
    symbol: "",
    quantity: 0,
    avg_price: 0,
    buy_date: "",
    notes: "",
  };
};

const submitEdit = async () => {
  try {
    // If quantity is 0, delete the holding
    if (editForm.value.quantity === 0) {
      await removeFromPortfolio(editForm.value.id);
    } else {
      // Update the holding
      await updatePortfolioHolding(editForm.value.id, {
        quantity: editForm.value.quantity,
        avg_price: editForm.value.avg_price,
        buy_date: editForm.value.buy_date,
        notes: editForm.value.notes,
      });
    }
    closeEditModal();
    await loadData();
  } catch (err: any) {
    error.value = err.message || "Failed to update holding";
    console.error("Error updating holding:", err);
  }
};

const deleteHolding = async (id: number) => {
  if (!confirm("Are you sure you want to delete this holding?")) return;

  try {
    await removeFromPortfolio(id);
    await loadData();
  } catch (err: any) {
    error.value = err.message || "Failed to delete holding";
    console.error("Error deleting holding:", err);
  }
};
</script>
