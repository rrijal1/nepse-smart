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

    <!-- Watchlist Table -->
    <div
      v-if="!loading"
      class="bg-white border border-gray-200 rounded-xl overflow-hidden"
    >
      <div
        class="px-6 py-4 border-b border-gray-200 bg-gray-50 flex justify-between items-center"
      >
        <h3 class="text-lg font-semibold text-gray-800">My Watchlist</h3>
        <button
          @click="openAddWatchlistModal"
          class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 text-sm font-medium"
        >
          + Add to Watchlist
        </button>
      </div>

      <!-- Empty State -->
      <div v-if="watchlistStocks.length === 0" class="p-12 text-center">
        <p class="text-gray-500 mb-4">No stocks in watchlist</p>
        <button
          @click="openAddWatchlistModal"
          class="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700"
        >
          Add Stock
        </button>
      </div>

      <!-- Watchlist Table -->
      <div v-else class="overflow-x-auto">
        <table class="min-w-full">
          <thead class="bg-gray-50 border-b border-gray-200">
            <tr>
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Symbol
              </th>
              <th
                class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                LTP
              </th>
              <th
                class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Change
              </th>
              <th
                class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                % Change
              </th>
              <th
                class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Holdings
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
              v-for="stock in watchlistStocks"
              :key="stock.id"
              class="hover:bg-gray-50"
            >
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                  <div class="font-semibold text-gray-900">
                    {{ stock.symbol }}
                  </div>
                  <StarIcon
                    :class="[
                      'w-4 h-4 ml-2 cursor-pointer transition-colors',
                      stock.favorite
                        ? 'text-yellow-500 fill-current'
                        : 'text-gray-300 hover:text-gray-400',
                    ]"
                    @click="toggleFavorite(stock)"
                  />
                </div>
              </td>
              <td
                class="px-6 py-4 whitespace-nowrap text-right font-mono font-semibold"
              >
                Rs. {{ (stock.ltp || 0).toLocaleString() }}
              </td>
              <td
                class="px-6 py-4 whitespace-nowrap text-right font-mono font-semibold"
                :class="
                  (stock.change || 0) >= 0 ? 'text-green-600' : 'text-red-600'
                "
              >
                {{ (stock.change || 0) >= 0 ? "+" : "" }}{{ stock.change || 0 }}
              </td>
              <td
                class="px-6 py-4 whitespace-nowrap text-right font-mono font-semibold"
                :class="
                  (stock.change_percent || 0) >= 0
                    ? 'text-green-600'
                    : 'text-red-600'
                "
              >
                {{ (stock.change_percent || 0) >= 0 ? "+" : ""
                }}{{ (stock.change_percent || 0).toFixed(2) }}%
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right">
                <div v-if="(stock.holdings || 0) > 0" class="text-sm">
                  <div class="font-semibold text-gray-900">
                    {{ stock.holdings }} shares
                  </div>
                  <div class="text-gray-600">
                    Avg: Rs.
                    {{ (stock.avg_holding_price || 0).toLocaleString() }}
                  </div>
                </div>
                <div v-else class="text-gray-400 text-sm">Not holding</div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-center space-x-2">
                <button
                  @click="openAddPortfolioModal(stock)"
                  class="text-blue-600 hover:text-blue-800 text-sm font-medium"
                  title="Add to Portfolio"
                >
                  Add Portfolio
                </button>
                <button
                  @click="removeStock(stock.id)"
                  class="text-red-600 hover:text-red-800 text-sm font-medium"
                  title="Remove from Watchlist"
                >
                  Remove
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Add to Portfolio Modal -->
    <div
      v-if="showAddPortfolioModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
      @click.self="closeAddPortfolioModal"
    >
      <div class="bg-white rounded-lg p-6 max-w-md w-full mx-4">
        <h3 class="text-lg font-semibold mb-4">
          Add {{ selectedStock?.symbol }} to Portfolio
        </h3>

        <form @submit.prevent="submitAddToPortfolio" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1"
              >Symbol</label
            >
            <input
              v-model="addPortfolioForm.symbol"
              type="text"
              readonly
              class="w-full px-3 py-2 border border-gray-300 rounded-lg bg-gray-50"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1"
              >Quantity</label
            >
            <input
              v-model.number="addPortfolioForm.quantity"
              type="number"
              min="1"
              required
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1"
              >Average Price (Rs.)</label
            >
            <input
              v-model.number="addPortfolioForm.avgPrice"
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
              v-model="addPortfolioForm.buyDate"
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
              v-model="addPortfolioForm.notes"
              rows="2"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            ></textarea>
          </div>

          <div class="flex space-x-3 pt-4">
            <button
              type="submit"
              class="flex-1 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
            >
              Add to Portfolio
            </button>
            <button
              type="button"
              @click="closeAddPortfolioModal"
              class="flex-1 bg-gray-200 text-gray-800 px-4 py-2 rounded-lg hover:bg-gray-300"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Add to Watchlist Modal -->
    <div
      v-if="showAddWatchlistModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
      @click.self="closeAddWatchlistModal"
    >
      <div
        class="bg-white rounded-lg p-6 max-w-md w-full mx-4 max-h-[80vh] overflow-y-auto"
      >
        <h3 class="text-lg font-semibold mb-4">Add Stock to Watchlist</h3>

        <!-- Search Input -->
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1"
            >Search Stock</label
          >
          <input
            v-model="stockSearch"
            type="text"
            placeholder="Type symbol or company name..."
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            @input="searchStocks"
          />
        </div>

        <!-- Loading State -->
        <div v-if="loadingStocks" class="text-center py-4">
          <div
            class="inline-block animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"
          ></div>
          <p class="mt-2 text-sm text-gray-600">Loading stocks...</p>
        </div>

        <!-- Stock List -->
        <div
          v-else-if="filteredStocks.length > 0"
          class="space-y-2 max-h-60 overflow-y-auto"
        >
          <button
            v-for="stock in filteredStocks"
            :key="stock.symbol"
            @click="selectStockForWatchlist(stock)"
            class="w-full text-left px-3 py-2 border border-gray-200 rounded-lg hover:bg-blue-50 hover:border-blue-300 transition-colors"
          >
            <div class="font-semibold text-gray-900">{{ stock.symbol }}</div>
            <div class="text-sm text-gray-600">{{ stock.name || "N/A" }}</div>
            <div v-if="stock.ltp" class="text-sm text-gray-500 mt-1">
              LTP: Rs. {{ stock.ltp.toLocaleString() }}
            </div>
          </button>
        </div>

        <!-- No Results -->
        <div
          v-else-if="stockSearch.length > 0"
          class="text-center py-4 text-gray-500"
        >
          No stocks found matching "{{ stockSearch }}"
        </div>

        <!-- Instructions -->
        <div v-else class="text-center py-4 text-gray-500">
          Start typing to search for stocks
        </div>

        <div class="flex space-x-3 pt-4 mt-4 border-t">
          <button
            type="button"
            @click="closeAddWatchlistModal"
            class="flex-1 bg-gray-200 text-gray-800 px-4 py-2 rounded-lg hover:bg-gray-300"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import StarIcon from "./icons/StarIcon.vue";
import {
  fetchWatchlist,
  updateWatchlistItem,
  removeFromWatchlist,
  addToWatchlist,
  type WatchlistItem,
} from "../services/portfolio";
import axios from "axios";

const watchlistStocks = ref<WatchlistItem[]>([]);
const loading = ref(false);
const error = ref<string | null>(null);
const showAddWatchlistModal = ref(false);
const showAddPortfolioModal = ref(false);
const selectedStock = ref<WatchlistItem | null>(null);

// Stock search state
const stockSearch = ref("");
const allStocks = ref<any[]>([]);
const filteredStocks = ref<any[]>([]);
const loadingStocks = ref(false);

// Form data
const addPortfolioForm = ref({
  symbol: "",
  quantity: 100,
  avgPrice: 0,
  buyDate: new Date().toISOString().split("T")[0],
  notes: "",
});

onMounted(async () => {
  await loadData();
});

const loadData = async () => {
  loading.value = true;
  error.value = null;
  try {
    const watchlist = await fetchWatchlist();
    watchlistStocks.value = watchlist;
  } catch (err: any) {
    error.value = err.message || "Failed to load data";
    console.error("Error loading watchlist data:", err);
  } finally {
    loading.value = false;
  }
};

const toggleFavorite = async (stock: WatchlistItem) => {
  try {
    await updateWatchlistItem(stock.id, { favorite: !stock.favorite });
    await loadData();
  } catch (err: any) {
    error.value = err.message || "Failed to update favorite";
    console.error("Error toggling favorite:", err);
  }
};

const removeStock = async (id: number) => {
  if (!confirm("Remove this stock from watchlist?")) return;

  try {
    await removeFromWatchlist(id);
    await loadData();
  } catch (err: any) {
    error.value = err.message || "Failed to remove stock";
    console.error("Error removing stock:", err);
  }
};

const openAddPortfolioModal = (stock: WatchlistItem) => {
  selectedStock.value = stock;
  addPortfolioForm.value.symbol = stock.symbol;
  addPortfolioForm.value.avgPrice = stock.ltp || 0;
  showAddPortfolioModal.value = true;
};

const closeAddPortfolioModal = () => {
  showAddPortfolioModal.value = false;
  selectedStock.value = null;
  addPortfolioForm.value = {
    symbol: "",
    quantity: 100,
    avgPrice: 0,
    buyDate: new Date().toISOString().split("T")[0],
    notes: "",
  };
};

const submitAddToPortfolio = async () => {
  try {
    const { addToPortfolio } = await import("../services/portfolio");
    await addToPortfolio(
      addPortfolioForm.value.symbol,
      addPortfolioForm.value.quantity,
      addPortfolioForm.value.avgPrice,
      addPortfolioForm.value.buyDate,
      addPortfolioForm.value.notes
    );
    closeAddPortfolioModal();
    await loadData();
  } catch (err: any) {
    error.value = err.message || "Failed to add to portfolio";
    console.error("Error adding to portfolio:", err);
  }
};

// Watchlist Modal Functions
const openAddWatchlistModal = async () => {
  showAddWatchlistModal.value = true;
  stockSearch.value = "";
  filteredStocks.value = [];

  // Load all stocks from API
  if (allStocks.value.length === 0) {
    loadingStocks.value = true;
    try {
      const response = await axios.get("/api/price-volume");
      allStocks.value = response.data.stocks || [];
    } catch (err) {
      console.error("Error loading stocks:", err);
      error.value = "Failed to load stock list";
    } finally {
      loadingStocks.value = false;
    }
  }
};

const closeAddWatchlistModal = () => {
  showAddWatchlistModal.value = false;
  stockSearch.value = "";
  filteredStocks.value = [];
};

const searchStocks = () => {
  const query = stockSearch.value.toLowerCase().trim();

  if (query.length === 0) {
    filteredStocks.value = [];
    return;
  }

  filteredStocks.value = allStocks.value
    .filter((stock) => {
      const symbol = (stock.symbol || "").toLowerCase();
      const name = (stock.securityName || stock.name || "").toLowerCase();
      return symbol.includes(query) || name.includes(query);
    })
    .slice(0, 20); // Limit to 20 results
};

const selectStockForWatchlist = async (stock: any) => {
  try {
    await addToWatchlist(stock.symbol, false, "");
    closeAddWatchlistModal();
    await loadData();
  } catch (err: any) {
    error.value = err.message || "Failed to add to watchlist";
    console.error("Error adding to watchlist:", err);
  }
};
</script>
