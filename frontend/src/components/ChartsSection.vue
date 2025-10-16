<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <div class="space-y-6">
    <!-- Chart Controls -->
    <div class="flex items-center justify-between mb-6">
      <div class="flex items-center gap-4">
        <div class="flex items-center gap-2">
          <label class="text-sm font-medium text-gray-700">Symbol:</label>
          <input
            v-model="selectedStock"
            @input="handleStockInput"
            @keyup.enter="handleStockSelection"
            placeholder="Enter stock symbol"
            class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[rgb(var(--color-nepse-primary))] focus:border-transparent"
            style="width: 120px;"
          />
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

        <!-- Indicators Selector -->
        <div class="flex items-center gap-2">
          <label class="text-sm font-medium text-gray-700">Indicator:</label>
          <select
            v-model="selectedIndicator"
            @change="handleIndicatorChange"
            class="px-3 py-1 border border-gray-300 rounded-md text-sm bg-white focus:outline-none focus:ring-2 focus:ring-[rgb(var(--color-nepse-primary))] focus:border-transparent"
          >
            <option
              v-for="indicator in indicators"
              :key="indicator"
              :value="indicator"
            >
              {{ indicator }}
            </option>
          </select>
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
          <!-- Fundamental data will go here -->
        </div>
      </div>

      <div class="bg-green-50 p-4 rounded-lg border border-green-200">
        <h4 class="font-semibold text-green-800 mb-3 flex items-center gap-2">
          <WaveIcon class="w-4 h-4" />
          Macro Economic Data
        </h4>
        <div class="space-y-2 text-sm">
          <!-- Macro data will go here -->
        </div>
      </div>

      <div class="bg-red-50 p-4 rounded-lg border border-red-200">
        <h4 class="font-semibold text-red-800 mb-3 flex items-center gap-2">
          <TrendingUpIcon class="w-4 h-4" />
          Key Levels
        </h4>
        <div class="space-y-2 text-sm">
          <!-- Key levels data will go here -->
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from "vue";
import {
  fetchHistoricalPrices,
  fetchCompanyList,
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
const selectedIndicator = ref("none");
const indicators = ["none", "SMA 20", "EMA 20", "RSI", "MACD"];

const chartSeries = ref<any[]>([]);
const chartOptions = ref<any>(null);

const handleIndicatorChange = () => {
  loadChartData();
};

const handleStockInput = () => {
  // Convert to uppercase as user types
  selectedStock.value = selectedStock.value.toUpperCase();
};

const handleStockSelection = () => {
  loadChartData();
};

// Calculate Simple Moving Average
const calculateSMA = (data: any[], period: number) => {
  const sma = [];
  for (let i = period - 1; i < data.length; i++) {
    const sum = data
      .slice(i - period + 1, i + 1)
      .reduce((acc, val) => acc + val.y[3], 0);
    sma.push({
      x: data[i].x,
      y: sum / period,
    });
  }
  return sma;
};

// Calculate Exponential Moving Average
const calculateEMA = (data: any[], period: number) => {
  const ema = [];
  const multiplier = 2 / (period + 1);

  // First EMA is SMA
  let sum = data.slice(0, period).reduce((acc, val) => acc + val.y[3], 0);
  ema.push({
    x: data[period - 1].x,
    y: sum / period,
  });

  // Calculate subsequent EMAs
  for (let i = period; i < data.length; i++) {
    const emaValue: number =
      (data[i].y[3] - ema[ema.length - 1].y) * multiplier +
      ema[ema.length - 1].y;
    ema.push({
      x: data[i].x,
      y: emaValue,
    });
  }

  return ema;
};

const loadChartData = async () => {
  if (!selectedStock.value) return;

  isLoading.value = true;
  error.value = null;

  try {
    const result = await fetchHistoricalPrices(selectedStock.value);
    if (result.error || !result.data || result.data.length === 0) {
      throw new Error(result.error || "No data found for this symbol");
    }

    const historicalData = result.data;

    // Sort data by date (oldest first)
    const sortedData = historicalData.sort(
      (a: any, b: any) =>
        new Date(a.date).getTime() - new Date(b.date).getTime()
    );

    // Take last 100 data points for better performance
    const recentData = sortedData.slice(-100);

    // Convert to ApexCharts candlestick format
    const candlestickData = recentData.map((d: any) => ({
      x: new Date(d.date).getTime(),
      y: [d.open, d.high, d.low, d.close || d.ltp], // OHLC format
    }));

    const volumeData = recentData.map((d: any) => ({
      x: new Date(d.date).getTime(),
      y: d.vol,
      fillColor: (d.close || d.ltp) > d.open ? '#00C853' : '#FF1744', // Green for up, red for down
    }));

    // Set up chart series - TradingView style with volume overlay
    const series: any[] = [
      {
        name: "Price",
        type: "candlestick",
        data: candlestickData,
        group: "price",
      },
      {
        name: "Volume",
        type: "bar",
        data: volumeData,
        group: "volume",
        color: function({ dataPointIndex, seriesIndex, w }: any) {
          const data = w.config.series[seriesIndex].data[dataPointIndex];
          return data.fillColor || '#666';
        }
      },
    ];

    // Add indicators if selected
    if (selectedIndicator.value === "SMA 20") {
      const smaData = calculateSMA(candlestickData, 20);
      series.push({
        name: "SMA 20",
        type: "line",
        data: smaData,
      });
    } else if (selectedIndicator.value === "EMA 20") {
      const emaData = calculateEMA(candlestickData, 20);
      series.push({
        name: "EMA 20",
        type: "line",
        data: emaData,
      });
    }

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
      yaxis: [
        {
          // Primary y-axis for price (candlesticks) - takes top 70% of chart
          seriesName: "Price",
          labels: {
            style: {
              colors: "#666",
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
          height: '70%', // Price takes 70% of height
        },
        {
          // Secondary y-axis for volume - takes bottom 30% of chart
          seriesName: "Volume",
          opposite: true,
          labels: {
            show: false, // Hide volume axis labels
          },
          title: {
            text: "",
          },
          axisBorder: {
            show: false,
          },
          axisTicks: {
            show: false,
          },
          height: '30%', // Volume takes 30% of height
          offsetY: 70, // Offset to position below price
        },
      ],
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
        bar: {
          columnWidth: "80%",
          distributed: true,
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
          const volume = w.config.series[1].data[dataPointIndex];
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
                <div style="margin-top: 4px;">Volume:</div><div style="text-align: right; margin-top: 4px; font-weight: bold;">${volume.y.toLocaleString()}</div>
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
