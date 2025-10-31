<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <div class="space-y-6">
    <!-- Chart Controls -->
    <div class="flex items-center justify-between mb-6">
      <div class="flex items-center gap-4">
        <div class="flex items-center gap-2 relative">
          <label class="text-sm font-medium text-gray-700">Symbol:</label>
          <input
            ref="stockInputRef"
            v-model="selectedStock"
            @input="handleStockInput"
            @keyup.enter="handleStockSelection"
            @focus="showStockDropdown = filteredStocks.length > 0"
            placeholder="Enter stock symbol"
            class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[rgb(var(--color-nepse-primary))] focus:border-transparent"
            style="width: 120px"
          />
          <!-- Stock Suggestions Dropdown -->
          <div
            v-if="showStockDropdown && filteredStocks.length > 0"
            class="absolute top-full left-16 mt-1 w-48 bg-white border border-gray-300 rounded-lg shadow-lg z-10 max-h-60 overflow-y-auto"
          >
            <div
              v-for="stock in filteredStocks"
              :key="stock.symbol"
              @click="selectStockFromDropdown(stock.symbol)"
              class="px-4 py-2 hover:bg-gray-100 cursor-pointer text-sm border-b border-gray-100 last:border-b-0"
            >
              {{ stock.symbol }}
            </div>
          </div>
        </div>
        <div class="flex items-center gap-2">
          <button
            v-for="timeframe in timeframes"
            :key="timeframe"
            @click="selectedTimeframe = timeframe"
            :class="[
              'px-3 py-1 rounded-md text-sm font-medium transition-colors',
              selectedTimeframe === timeframe
                ? 'bg-[rgb(var(--color-nepse-primary))] text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200',
            ]"
          >
            {{ timeframe }}
          </button>
        </div>
      </div>
    </div>

    <!-- Main Chart Area -->
    <div class="bg-gray-50 rounded-xl p-6 relative">
      <div
        v-if="isLoading"
        class="absolute inset-0 flex items-center justify-center bg-gray-50 bg-opacity-75 z-10"
      >
        <div class="flex items-center space-x-2">
          <div
            class="animate-spin rounded-full h-8 w-8 border-b-2 border-[rgb(var(--color-nepse-primary))]"
          ></div>
          <span class="text-gray-600">Loading chart data...</span>
        </div>
      </div>

      <div
        v-if="error && !isLoading"
        class="absolute inset-0 flex items-center justify-center bg-gray-50 z-10"
      >
        <div class="text-center">
          <div class="text-red-500 text-lg font-semibold mb-2">
            Error Loading Data
          </div>
          <div class="text-gray-600">{{ error }}</div>
          <button
            @click="loadChartData"
            class="mt-4 px-4 py-2 bg-[rgb(var(--color-nepse-primary))] text-white rounded-lg hover:bg-opacity-90 transition-colors"
          >
            Retry
          </button>
        </div>
      </div>

      <ApexChart
        v-if="!isLoading && !error && chartOptions"
        type="candlestick"
        :options="chartOptions"
        :series="chartSeries"
        height="400"
      ></ApexChart>
    </div>

    <!-- Data Panels -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="bg-blue-50 p-4 rounded-lg border border-blue-200">
        <h4 class="font-semibold text-blue-800 mb-3 flex items-center gap-2">
          <BookIcon class="w-4 h-4" />
          Fundamental Data
        </h4>
        <div class="space-y-2 text-sm">
          <div v-if="fundamentalData">
            <div class="grid grid-cols-2 gap-2">
              <div>
                <span class="font-medium">Symbol:</span>
                {{ fundamentalData.symbol }}
              </div>
              <div>
                <span class="font-medium">LTP:</span> NPR
                {{ fundamentalData.ltp?.toFixed(2) }}
              </div>
              <div>
                <span class="font-medium">Change:</span>
                <span
                  :class="
                    fundamentalData.change >= 0
                      ? 'text-green-600'
                      : 'text-red-600'
                  "
                >
                  {{ fundamentalData.change >= 0 ? "+" : ""
                  }}{{ fundamentalData.change?.toFixed(2) }}
                </span>
              </div>
              <div>
                <span class="font-medium">Volume:</span>
                {{ fundamentalData.volume?.toLocaleString() }}
              </div>
            </div>
          </div>
          <div v-else class="text-gray-500">Loading fundamental data...</div>
        </div>
      </div>

      <div class="bg-green-50 p-4 rounded-lg border border-green-200">
        <h4 class="font-semibold text-green-800 mb-3 flex items-center gap-2">
          <WaveIcon class="w-4 h-4" />
          Macro Economic Data
        </h4>
        <div class="space-y-2 text-sm">
          <div
            v-if="
              macroData &&
              macroData.forex_rates &&
              macroData.forex_rates.length > 0
            "
          >
            <div class="font-medium mb-2">Exchange Rates (USD):</div>
            <div class="grid grid-cols-2 gap-1 text-xs">
              <div>
                Buy: NPR {{ macroData.forex_rates[0]?.rates?.[0]?.toFixed(2) }}
              </div>
              <div>
                Sell: NPR {{ macroData.forex_rates[0]?.rates?.[1]?.toFixed(2) }}
              </div>
            </div>
          </div>
          <div
            v-if="
              macroData &&
              macroData.banking_indicators &&
              macroData.banking_indicators.length > 0
            "
          >
            <div class="font-medium mb-2 mt-3">Banking Indicators:</div>
            <div class="text-xs">
              <div>
                {{ macroData.banking_indicators[0]?.indicator }}:
                {{ macroData.banking_indicators[0]?.current_value }}
              </div>
            </div>
          </div>
          <div v-else class="text-gray-500">Loading macro data...</div>
        </div>
      </div>

      <div class="bg-red-50 p-4 rounded-lg border border-red-200">
        <h4 class="font-semibold text-red-800 mb-3 flex items-center gap-2">
          <TrendingUpIcon class="w-4 h-4" />
          Key Levels
        </h4>
        <div class="space-y-2 text-sm">
          <div v-if="keyLevels">
            <div class="grid grid-cols-2 gap-2">
              <div>
                <span class="font-medium text-green-600">Support:</span>
              </div>
              <div>
                <span class="font-medium text-red-600">Resistance:</span>
              </div>
              <div>NPR {{ keyLevels.support?.[0]?.toFixed(2) }}</div>
              <div>NPR {{ keyLevels.resistance?.[0]?.toFixed(2) }}</div>
              <div>NPR {{ keyLevels.support?.[1]?.toFixed(2) }}</div>
              <div>NPR {{ keyLevels.resistance?.[1]?.toFixed(2) }}</div>
            </div>
          </div>
          <div v-else class="text-gray-500">Calculating key levels...</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, watch, computed } from "vue";
import {
  fetchCompanyHistory,
  fetchCompanyList,
  fetchMacroData,
  fetchPriceVolume,
} from "../services/marketData_enhanced";
import BookIcon from "./icons/BookIcon.vue";
import WaveIcon from "./icons/WaveIcon.vue";
import TrendingUpIcon from "./icons/TrendingUpIcon.vue";
import VueApexCharts from "vue3-apexcharts";

const ApexChart = VueApexCharts;

const props = defineProps({
  symbol: {
    type: String,
    default: "NABIL",
  },
});

const isLoading = ref(false);
const error = ref<string | null>(null);

const selectedStock = ref(props.symbol);
const allStocks = ref<{ symbol: string }[]>([]);
const selectedTimeframe = ref("1D");
const timeframes = ["1D", "1W", "1M"];

const showStockDropdown = ref(false);
const stockInputRef = ref<HTMLInputElement | null>(null);

// Fundamental and Macro data
const fundamentalData = ref<any>(null);
const macroData = ref<any>(null);
const keyLevels = ref<any>(null);

// Computed property for filtered stocks
const filteredStocks = computed(() => {
  if (!selectedStock.value || selectedStock.value.length < 1) {
    return [];
  }

  const query = selectedStock.value.toUpperCase();
  return allStocks.value
    .filter((stock) => stock.symbol.toUpperCase().includes(query))
    .slice(0, 10); // Limit to 10 results
});

const chartSeries = ref<any[]>([]);
const chartOptions = ref<any>(null);

const handleStockInput = () => {
  // Convert to uppercase as user types
  selectedStock.value = selectedStock.value.toUpperCase();
  showStockDropdown.value = filteredStocks.value.length > 0;
};

const handleStockSelection = () => {
  showStockDropdown.value = false;
  loadChartData();
  loadFundamentalData();
};

const selectStockFromDropdown = (symbol: string) => {
  selectedStock.value = symbol;
  showStockDropdown.value = false;
  loadChartData();
  loadFundamentalData();
};

const loadFundamentalData = async () => {
  try {
    const priceData = await fetchPriceVolume(); // Get latest price data
    const stockData = priceData.find(
      (stock: any) => stock.symbol === selectedStock.value
    );
    if (stockData) {
      fundamentalData.value = stockData;
    }
  } catch (error) {
    console.error("Error loading fundamental data:", error);
  }
};

const loadMacroData = async () => {
  try {
    const data = await fetchMacroData();
    if (data && !data.error) {
      macroData.value = data;
    }
  } catch (error) {
    console.error("Error loading macro data:", error);
  }
};

// Calculate support and resistance levels
const calculateSupportResistance = (data: any[]) => {
  if (data.length < 10) return { support: [], resistance: [] };

  const highs = data.map((d) => d.y[1]); // High prices
  const lows = data.map((d) => d.y[2]); // Low prices

  // Simple pivot point calculation
  const pivot =
    (highs.reduce((a, b) => a + b, 0) +
      lows.reduce((a, b) => a + b, 0) +
      data[data.length - 1].y[3]) /
    (highs.length + lows.length + 1);

  const resistance1 = 2 * pivot - lows.reduce((a, b) => a + b, 0) / lows.length;
  const support1 = 2 * pivot - highs.reduce((a, b) => a + b, 0) / highs.length;

  const resistance2 =
    pivot +
    (highs.reduce((a, b) => a + b, 0) / highs.length -
      lows.reduce((a, b) => a + b, 0) / lows.length);
  const support2 =
    pivot -
    (highs.reduce((a, b) => a + b, 0) / highs.length -
      lows.reduce((a, b) => a + b, 0) / lows.length);

  return {
    support: [support1, support2],
    resistance: [resistance1, resistance2],
  };
};

const calculateKeyLevels = (data: any[]) => {
  if (data.length >= 10) {
    keyLevels.value = calculateSupportResistance(data);
  }
};

const handleClickOutside = (event: Event) => {
  const target = event.target as HTMLElement;
  if (stockInputRef.value && !stockInputRef.value.contains(target)) {
    showStockDropdown.value = false;
  }
};

const loadChartData = async () => {
  if (!selectedStock.value) return;

  isLoading.value = true;
  error.value = null;

  try {
    // Fetch all available historical data for the stock (365 days should cover most data)
    const result = await fetchCompanyHistory(selectedStock.value, 365);
    if (result.error || !result.data || result.data.length === 0) {
      throw new Error(result.error || "No data found for this symbol");
    }

    const historicalData = result.data;

    // Data comes pre-sorted from backend (oldest first)
    const chartData = historicalData;

    // Convert to ApexCharts candlestick format
    const candlestickData = chartData.map((d: any) => ({
      x: new Date(d.date).getTime(),
      y: [d.open, d.high, d.low, d.close], // OHLC format
    }));

    // Set up chart series - Only price candles, no volume
    const series: any[] = [
      {
        name: "Price",
        type: "candlestick",
        data: candlestickData,
      },
    ];

    // Calculate key levels
    calculateKeyLevels(candlestickData);

    chartSeries.value = series;

    // Set up chart options - TradingView style
    chartOptions.value = {
      chart: {
        type: "candlestick",
        height: 500,
        toolbar: {
          show: true,
          tools: {
            download: true,
            selection: true,
            zoom: true,
            zoomin: true,
            zoomout: true,
            pan: true,
            reset: true,
          },
        },
        background: "#ffffff",
      },
      title: {
        text: `${selectedStock.value} Price Chart`,
        align: "left",
        style: {
          fontSize: "16px",
          fontWeight: "bold",
          color: "#333",
        },
      },
      xaxis: {
        type: "datetime",
        labels: {
          format: "MMM dd",
          style: {
            colors: "#666",
          },
        },
        axisBorder: {
          show: true,
          color: "#ddd",
        },
        axisTicks: {
          show: true,
          color: "#ddd",
        },
      },
      yaxis: {
        labels: {
          style: {
            colors: "#666",
          },
          formatter: function (value: any) {
            return Math.round(value);
          },
        },
        title: {
          text: "Price (NPR)",
          style: {
            color: "#666",
          },
        },
        axisBorder: {
          show: true,
          color: "#ddd",
        },
        axisTicks: {
          show: true,
          color: "#ddd",
        },
      },
      plotOptions: {
        candlestick: {
          colors: {
            upward: "#00C853",
            downward: "#FF1744",
          },
          wick: {
            useFillColor: true,
          },
        },
      },
      stroke: {
        show: true,
        colors: ["#000000"],
        width: 1,
      },
      dataLabels: {
        enabled: false,
      },
      grid: {
        show: true,
        borderColor: "#f0f0f0",
        strokeDashArray: 3,
        xaxis: {
          lines: {
            show: false,
          },
        },
        yaxis: {
          lines: {
            show: true,
          },
        },
      },
      tooltip: {
        shared: true,
        intersect: false,
        custom: function ({ dataPointIndex, w }: any) {
          if (!w.config.series[0].data[dataPointIndex]) return "";

          const data = w.config.series[0].data[dataPointIndex];
          const date = new Date(data.x);

          return `
            <div class="apexcharts-tooltip-custom" style="
              background: rgba(255,255,255,0.95);
              border: 1px solid #ddd;
              border-radius: 4px;
              padding: 8px;
              box-shadow: 0 2px 8px rgba(0,0,0,0.1);
              font-family: Arial, sans-serif;
              font-size: 12px;
            ">
              <div style="font-weight: bold; margin-bottom: 4px; color: #333;">
                ${date.toLocaleDateString("en-US", {
                  year: "numeric",
                  month: "short",
                  day: "numeric",
                })}
              </div>
              <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 4px;">
                <div>Open:</div><div style="text-align: right; font-weight: bold;">${
                  data.y[0]
                }</div>
                <div>High:</div><div style="text-align: right; font-weight: bold; color: #00C853;">${
                  data.y[1]
                }</div>
                <div>Low:</div><div style="text-align: right; font-weight: bold; color: #FF1744;">${
                  data.y[2]
                }</div>
                <div>Close:</div><div style="text-align: right; font-weight: bold;">${
                  data.y[3]
                }</div>
              </div>
            </div>
          `;
        },
      },
      responsive: [
        {
          breakpoint: 768,
          options: {
            chart: {
              height: 400,
            },
          },
        },
      ],
    };
  } catch (e: any) {
    error.value = e.message || "Failed to load chart data.";
  } finally {
    isLoading.value = false;
  }
};

onMounted(async () => {
  allStocks.value = await fetchCompanyList();
  await loadChartData();
  await loadFundamentalData();
  await loadMacroData();

  // Add click outside listener
  document.addEventListener("click", handleClickOutside);
});

onBeforeUnmount(() => {
  // Remove click outside listener
  document.removeEventListener("click", handleClickOutside);
});

watch(
  () => props.symbol,
  (newSymbol) => {
    if (newSymbol) {
      selectedStock.value = newSymbol;
      loadChartData();
    }
  }
);
</script>
