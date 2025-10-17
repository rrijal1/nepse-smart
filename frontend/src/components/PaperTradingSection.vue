<template>
  <div class="space-y-6">
    <!-- Account Summary or Fund CTA -->
    <div
      v-if="account && !loading && isUnfunded"
      class="bg-white border border-gray-200 rounded-xl p-6 flex items-center justify-between"
    >
      <div>
        <div class="text-lg font-semibold text-gray-800">
          Practice trading with virtual cash
        </div>
        <div class="text-gray-600 text-sm mt-1">
          Improve your skills without risking real money. We'll fund your paper
          account with Rs. 50,00,000.
        </div>
      </div>
      <div class="flex items-center gap-3">
        <button
          @click="fundAccount"
          :disabled="funding"
          class="px-4 py-2 rounded-md text-white"
          :class="
            funding
              ? 'bg-blue-300 cursor-not-allowed'
              : 'bg-blue-600 hover:bg-blue-700'
          "
        >
          <span v-if="!funding">Start with Rs. 50L</span>
          <span v-else>Funding...</span>
        </button>
      </div>
    </div>

    <div
      v-else-if="account && !loading"
      class="grid grid-cols-1 sm:grid-cols-3 gap-6 mb-2"
    >
      <div class="bg-white border border-gray-200 rounded-xl p-5">
        <div class="text-sm text-gray-500">Initial Capital</div>
        <div class="text-xl font-semibold">
          {{ formatCurrency(account.initial_capital) }}
        </div>
      </div>
      <div class="bg-white border border-gray-200 rounded-xl p-5">
        <div class="text-sm text-gray-500">Cash Available</div>
        <div class="text-xl font-semibold">
          {{
            formatCurrency(
              portfolioSummary?.cash_available || account.cash_balance
            )
          }}
        </div>
        <button
          @click="resetAccount"
          class="mt-2 text-xs text-gray-500 underline hover:text-gray-700"
        >
          Reset practice account
        </button>
      </div>
      <div
        class="bg-white border border-gray-200 rounded-xl p-5 flex items-center justify-between"
      >
        <div>
          <div class="text-sm text-gray-500">Quick Trade</div>
          <div class="text-xs text-gray-400">
            Executes at current market price
          </div>
        </div>
        <div class="flex space-x-2">
          <button
            @click="openQuickTrade('buy')"
            class="px-3 py-1.5 bg-green-600 text-white rounded-md text-sm"
          >
            Buy
          </button>
          <button
            @click="openQuickTrade('sell')"
            class="px-3 py-1.5 bg-red-600 text-white rounded-md text-sm"
          >
            Sell
          </button>
        </div>
      </div>
    </div>
    <!-- Loading State -->
    <div v-if="loading" class="text-center py-8">
      <div
        class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"
      ></div>
      <p class="mt-2 text-gray-600">Loading Paper Portfolio...</p>
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

    <!-- Portfolio Summary Cards (hidden until funded) -->
    <div
      v-if="!isUnfunded && portfolioSummary && !loading"
      class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 mb-6"
    >
      <div
        class="bg-gradient-to-br from-green-50 to-green-100 p-6 rounded-xl border border-green-200"
      >
        <div class="flex items-center justify-between mb-4">
          <h3 class="font-semibold text-green-800">Total Paper Portfolio</h3>
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
        <div
          v-if="portfolioSummary.apy_since"
          class="text-xs mt-2 text-gray-600"
        >
          APY:
          <span class="font-medium">{{
            formatPercent(portfolioSummary.apy_annualized || 0)
          }}</span>
          <span class="ml-1"
            >since {{ formatDate(portfolioSummary.apy_since as any) }}</span
          >
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

    <!-- Holdings Table (hidden until funded) -->
    <div
      v-if="!isUnfunded"
      class="bg-white border border-gray-200 rounded-xl overflow-hidden"
    >
      <div
        class="px-6 py-4 border-b border-gray-200 bg-gray-50 flex items-center justify-between"
      >
        <h3 class="text-lg font-semibold text-gray-800">Paper Holdings</h3>
        <div class="flex items-center gap-3">
          <span class="text-xs text-gray-600">Share:</span>
          <button
            @click="shareToTwitter"
            class="p-1 rounded hover:bg-gray-100"
            aria-label="Share on X"
            title="Share on X"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="currentColor"
              class="w-4 h-4 text-black"
            >
              <path
                d="M18.244 2.25h3.256l-7.104 8.115L23.5 21.75h-6.407l-5.02-6.545-5.74 6.545H3.076l7.593-8.662L.75 2.25h6.593l4.54 5.987 6.361-5.987zM17.157 19.5h1.804L6.94 4.39H5.03l12.127 15.11z"
              />
            </svg>
          </button>
          <button
            @click="shareToFacebook"
            class="p-1 rounded hover:bg-gray-100"
            aria-label="Share on Facebook"
            title="Share on Facebook"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="currentColor"
              class="w-4 h-4 text-blue-600"
            >
              <path
                d="M22 12.06C22 6.49 17.52 2 12 2S2 6.49 2 12.06c0 5.02 3.66 9.19 8.44 9.94v-7.03H7.9v-2.91h2.54V9.41c0-2.5 1.49-3.89 3.77-3.89 1.09 0 2.24.2 2.24.2v2.47h-1.26c-1.24 0-1.63.77-1.63 1.55v1.86h2.78l-.44 2.91h-2.34v7.03C18.34 21.25 22 17.08 22 12.06z"
              />
            </svg>
          </button>
          <button
            v-if="canWebShare"
            @click="shareViaWebShare"
            class="p-1 rounded hover:bg-gray-100"
            aria-label="Share"
            title="Share"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="currentColor"
              class="w-4 h-4 text-gray-600"
            >
              <path
                d="M18 16.08c-.76 0-1.44.3-1.96.77L8.91 12.7c.05-.23.09-.46.09-.7s-.04-.47-.09-.7l7.02-4.11A2.99 2.99 0 0 0 18 7.91c1.66 0 3-1.35 3-3.01A3 3 0 0 0 18 1.91a3 3 0 0 0-3 3.01c0 .24.03.47.09.7L8.07 9.73A3 3 0 0 0 6 9.09a3 3 0 0 0-3 3.01 3 3 0 0 0 3 3.01c.79 0 1.5-.31 2.03-.82l6.84 3.99c-.05.21-.08.43-.08.66a3 3 0 0 0 3 3.01 3 3 0 0 0 3-3.01 3 3 0 0 0-3-3.01z"
              />
            </svg>
          </button>
        </div>
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
                Trade
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
                {{ formatCountCompact(holding.quantity) }}
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
                {{ formatCurrencySigned(holding.pnl || 0) }}
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
                  @click="openQuickTrade('buy', holding.symbol)"
                  class="text-green-600 hover:text-green-800 text-sm font-medium"
                  title="Buy More"
                >
                  Buy
                </button>
                <button
                  @click="openQuickTrade('sell', holding.symbol)"
                  class="text-red-600 hover:text-red-800 text-sm font-medium"
                  title="Sell"
                >
                  Sell
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Removed Edit Holding Modal to prevent manual adjustments -->

    <!-- Quick Trade Modal -->
    <div
      v-if="showTradeModal"
      class="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
      @click.self="showTradeModal = false"
    >
      <div class="bg-white rounded-lg p-6 w-full max-w-sm">
        <h3 class="text-lg font-semibold mb-4">
          {{ tradeSide === "buy" ? "Buy" : "Sell" }} at Market
        </h3>
        <div class="space-y-3">
          <div>
            <label class="block text-sm text-gray-600 mb-1">Symbol</label>
            <div class="relative">
              <input
                v-model="symbolQuery"
                type="text"
                class="w-full border rounded px-3 py-2 pr-8"
                placeholder="Search symbol or company"
                @input="onSymbolQuery"
              />
              <div
                v-if="filteredCompanies.length && symbolQuery"
                class="absolute z-10 mt-1 w-full bg-white border border-gray-200 rounded-md max-h-56 overflow-auto shadow"
              >
                <div
                  v-for="c in filteredCompanies"
                  :key="c.symbol"
                  @click="selectSymbol(c.symbol)"
                  class="px-3 py-2 cursor-pointer hover:bg-gray-50 flex justify-between"
                >
                  <span class="font-medium">{{ c.symbol }}</span>
                  <span class="text-gray-500 text-xs ml-2">{{ c.name }}</span>
                </div>
              </div>
            </div>
            <div class="mt-1 text-xs text-gray-500" v-if="tradeSymbol">
              <span
                >Selected:
                <span class="font-semibold">{{ tradeSymbol }}</span></span
              >
            </div>
            <div class="mt-1 text-xs text-gray-500" v-if="tradeSymbol">
              <span
                >LTP:
                {{
                  currentPriceForSelected
                    ? "Rs. " + currentPriceForSelected.toLocaleString()
                    : "—"
                }}</span
              >
              <span
                v-if="tradeSide === 'sell' && availableToSell !== null"
                class="ml-2"
                >• You own: {{ availableToSell }}</span
              >
            </div>
          </div>

          <div>
            <label class="block text-sm text-gray-600 mb-1">Quantity</label>
            <input
              v-model.number="tradeQty"
              type="number"
              min="1"
              class="w-full border rounded px-3 py-2"
            />
            <p v-if="sellQuantityInvalid" class="mt-1 text-xs text-red-600">
              You cannot sell more than you own ({{ availableToSell }}).
            </p>
          </div>

          <div
            class="text-xs text-gray-600"
            v-if="currentPriceForSelected && tradeQty > 0"
          >
            Estimated total: Rs. {{ estimatedTotal.toLocaleString() }}
          </div>

          <div
            v-if="tradeError"
            class="bg-red-50 border border-red-200 text-red-700 text-sm rounded p-2"
          >
            {{ tradeError }}
          </div>

          <div class="flex space-x-2 pt-2">
            <button
              @click="submitTrade"
              :disabled="confirmDisabled || tradeSubmitting"
              class="flex-1 rounded px-4 py-2 text-white"
              :class="
                confirmDisabled || tradeSubmitting
                  ? 'bg-blue-300 cursor-not-allowed'
                  : 'bg-blue-600 hover:bg-blue-700'
              "
            >
              <span v-if="!tradeSubmitting">Confirm</span>
              <span v-else>Submitting...</span>
            </button>
            <button
              @click="showTradeModal = false"
              class="flex-1 bg-gray-200 rounded px-4 py-2"
            >
              Cancel
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import TrendingUpIcon from "./icons/TrendingUpIcon.vue";
import ChartIcon from "./icons/ChartIcon.vue";
import WalletIcon from "./icons/WalletIcon.vue";
import {
  fetchPaperPortfolio,
  fetchPaperPortfolioSummary,
  fetchPaperAccount,
  placePaperTrade,
  type PaperPortfolioHolding,
  type PaperPortfolioSummary,
  type PaperAccount,
} from "../services/paperTrading";
import {
  fetchCompanyList,
  fetchPriceVolume,
} from "../services/marketData_enhanced";

const portfolioHoldings = ref<PaperPortfolioHolding[]>([]);
const portfolioSummary = ref<PaperPortfolioSummary | null>(null);
const account = ref<PaperAccount | null>(null);
const loading = ref(false);
const error = ref<string | null>(null);
// Removed edit modal state

onMounted(async () => {
  await loadData();
});

const loadData = async () => {
  loading.value = true;
  error.value = null;
  try {
    const [holdings, summary, acct, comps, priceVol] = await Promise.all([
      fetchPaperPortfolio(),
      fetchPaperPortfolioSummary(),
      fetchPaperAccount(),
      fetchCompanyList(),
      fetchPriceVolume(),
    ]);
    portfolioHoldings.value = holdings;
    portfolioSummary.value = summary;
    account.value = acct;
    companies.value = Array.isArray(comps)
      ? comps.map((c: any) => ({ symbol: c.symbol, name: c.name }))
      : [];
    // Build a quick price lookup map from price-volume
    priceMap.value = new Map<string, number>();
    if (Array.isArray(priceVol)) {
      for (const item of priceVol) {
        const sym = (item.symbol || item.Symbol || "").toString();
        const ltp = Number(
          item.ltp ?? item.LTP ?? item.close ?? item.price ?? NaN
        );
        if (sym && !Number.isNaN(ltp)) {
          priceMap.value.set(sym.toUpperCase(), ltp);
        }
      }
    }
  } catch (err: any) {
    error.value = err.message || "Failed to load paper portfolio data";
    console.error("Error loading paper portfolio data:", err);
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

// Compact integer formatter for share counts (e.g., 3.3L, 1.2Cr)
const formatCountCompact = (value: number | null | undefined): string => {
  if (value === null || value === undefined) return "N/A";
  const absValue = Math.abs(value);
  const sign = value < 0 ? "-" : "";
  if (absValue >= 10000000)
    return `${sign}${(absValue / 10000000).toFixed(2)}Cr`;
  if (absValue >= 100000) return `${sign}${(absValue / 100000).toFixed(2)}L`;
  if (absValue >= 10000) return `${sign}${(absValue / 1000).toFixed(1)}K`;
  return `${sign}${absValue.toLocaleString("en-IN", {
    maximumFractionDigits: 0,
  })}`;
};

// Signed currency version of formatCurrency
const formatCurrencySigned = (value: number): string => {
  if (value === 0) return "+Rs. 0";
  const formatted = formatCurrency(value);
  return value > 0 ? formatted.replace("Rs.", "+Rs.") : formatted;
};

// Utility: date format for APY since
const formatDate = (value: string | Date | null | undefined): string => {
  if (!value) return "";
  const d = typeof value === "string" ? new Date(value) : value;
  if (!(d instanceof Date) || isNaN(d.getTime())) return "";
  return d.toLocaleDateString();
};

// Removed edit/delete manual adjustment functions

// Quick Trade Modal
const showTradeModal = ref(false);
const tradeSide = ref<"buy" | "sell">("buy");
const tradeSymbol = ref("");
const tradeQty = ref<number>(0);
const tradeError = ref<string | null>(null);
const tradeSubmitting = ref(false);
const companies = ref<Array<{ symbol: string; name?: string }>>([]);
const priceMap = ref<Map<string, number>>(new Map());
const funding = ref(false);

// Show CTA when both initial_capital and cash are zero (unfunded)
const isUnfunded = computed(() => {
  return (
    !!account.value &&
    account.value.initial_capital === 0 &&
    account.value.cash_balance === 0
  );
});

// Symbol search state
const symbolQuery = ref("");
const filteredCompanies = computed(() => {
  const q = symbolQuery.value.trim().toLowerCase();
  if (!q) return [] as Array<{ symbol: string; name?: string }>;
  // If exact symbol is typed, hide it from dropdown to avoid duplication
  const exact = companies.value.find((c) => c.symbol.toLowerCase() === q);
  const list = companies.value.filter(
    (c) =>
      c.symbol.toLowerCase().includes(q) ||
      (c.name || "").toLowerCase().includes(q)
  );
  const withoutExact = exact
    ? list.filter((c) => c.symbol.toLowerCase() !== q)
    : list;
  return withoutExact.slice(0, 20);
});

const selectSymbol = (sym: string) => {
  tradeSymbol.value = sym;
  symbolQuery.value = `${sym}`;
};

const onSymbolQuery = () => {
  // if user typed an exact symbol, set it
  const exact = companies.value.find(
    (c) => c.symbol.toLowerCase() === symbolQuery.value.trim().toLowerCase()
  );
  if (exact) tradeSymbol.value = exact.symbol;
  else tradeSymbol.value = "";
};

const availableToSell = computed<number | null>(() => {
  const sym = tradeSymbol.value?.toUpperCase?.() || "";
  if (!sym) return null;
  const holding = portfolioHoldings.value.find(
    (h) => h.symbol?.toUpperCase() === sym
  );
  return holding ? Number(holding.quantity) : 0;
});

const currentPriceForSelected = computed<number | null>(() => {
  const sym = tradeSymbol.value?.toUpperCase?.() || "";
  if (!sym) return null;
  if (priceMap.value.has(sym)) return priceMap.value.get(sym) || null;
  const holding = portfolioHoldings.value.find(
    (h) => h.symbol?.toUpperCase() === sym
  );
  return holding && holding.current_price
    ? Number(holding.current_price)
    : null;
});

const estimatedTotal = computed<number>(() => {
  const price = currentPriceForSelected.value || 0;
  const qty = Number(tradeQty.value) || 0;
  return Math.max(0, Math.round(price * qty));
});

const sellQuantityInvalid = computed<boolean>(() => {
  if (tradeSide.value !== "sell") return false;
  const available = availableToSell.value;
  const qty = Number(tradeQty.value) || 0;
  if (available === null) return false;
  return qty > available;
});

const confirmDisabled = computed<boolean>(() => {
  return (
    !tradeSymbol.value ||
    !tradeQty.value ||
    tradeQty.value < 1 ||
    sellQuantityInvalid.value ||
    tradeSubmitting.value
  );
});

const openQuickTrade = (side: "buy" | "sell", preselectSymbol?: string) => {
  tradeSide.value = side;
  tradeSymbol.value = preselectSymbol ? preselectSymbol.toUpperCase() : "";
  tradeQty.value = 0;
  tradeError.value = null;
  symbolQuery.value = preselectSymbol ? preselectSymbol.toUpperCase() : "";
  showTradeModal.value = true;
};

const submitTrade = async () => {
  tradeError.value = null;
  if (confirmDisabled.value) return;
  try {
    tradeSubmitting.value = true;
    await placePaperTrade(tradeSymbol.value, tradeQty.value, tradeSide.value);
    showTradeModal.value = false;
    await loadData();
  } catch (err: any) {
    const msg =
      err?.response?.data?.detail || err?.message || "Failed to place trade";
    tradeError.value = msg;
    console.error("Trade error:", err);
  } finally {
    tradeSubmitting.value = false;
  }
};

// Fund CTA handler
import api from "../services/marketData_enhanced";
const fundAccount = async () => {
  try {
    funding.value = true;
    await api.post("/paper-trading/account/fund");
    await loadData();
  } catch (err: any) {
    error.value =
      err?.response?.data?.detail || err?.message || "Failed to fund account";
  } finally {
    funding.value = false;
  }
};

const resetAccount = async () => {
  try {
    funding.value = true;
    await api.post("/paper-trading/account/reset");
    await loadData();
  } catch (err: any) {
    error.value =
      err?.response?.data?.detail || err?.message || "Failed to reset account";
  } finally {
    funding.value = false;
  }
};

const canWebShare = computed(
  () => typeof navigator !== "undefined" && !!(navigator as any).share
);

// Compact amount without Rs. prefix for social text (e.g., 55K, 1.2L, 0.8Cr)
const formatAmountCompact = (value: number): string => {
  const absValue = Math.abs(value);
  const sign = value < 0 ? "-" : "";
  if (absValue >= 10000000)
    return `${sign}${(absValue / 10000000).toFixed(2)}Cr`;
  if (absValue >= 100000) return `${sign}${(absValue / 100000).toFixed(2)}L`;
  if (absValue >= 1000) return `${sign}${(absValue / 1000).toFixed(0)}K`;
  return `${sign}${absValue.toFixed(0)}`;
};

const buildShareText = () => {
  const pnlAmt = portfolioSummary.value?.total_pnl || 0;
  const pnlPct = portfolioSummary.value?.total_pnl_percent || 0;
  const since = portfolioSummary.value?.apy_since
    ? formatDate(portfolioSummary.value.apy_since as any)
    : undefined;
  const apy = portfolioSummary.value?.apy_annualized || 0;
  const amtStr = formatAmountCompact(pnlAmt);
  const pctStr = `${pnlPct >= 0 ? "+" : ""}${pnlPct.toFixed(2)}%`;
  const apyStr = `${apy >= 0 ? "+" : ""}${apy.toFixed(2)}%`;
  const sinceStr = since ? ` from ${since}` : "";
  return `I gained ${amtStr}, ${pctStr}${sinceStr}, APY ${apyStr} on NEPSE Smart`;
};

const shareToTwitter = () => {
  const text = buildShareText();
  const url = `https://twitter.com/intent/tweet?text=${encodeURIComponent(
    text
  )}`;
  window.open(url, "_blank", "noopener");
};

const shareToFacebook = () => {
  const text = buildShareText();
  const shareUrl = "https://nepse-smart.local"; // optional landing URL
  const url = `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(
    shareUrl
  )}&quote=${encodeURIComponent(text)}`;
  window.open(url, "_blank", "noopener");
};

const shareViaWebShare = async () => {
  try {
    const text = buildShareText();
    const nav: any = navigator;
    if (nav?.share) {
      await nav.share({ title: "NEPSE Smart", text });
    } else {
      shareToTwitter();
    }
  } catch (e) {
    // Fallback to Twitter on failure/cancel
    shareToTwitter();
  }
};
</script>

<style scoped></style>
