<template>
  <div class="space-y-6">
    <!-- Chart Controls -->
    <div class="flex items-center justify-between mb-6">
      <div class="flex items-center gap-4">
        <select
          v-model="selectedStock"
          class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[rgb(var(--color-nepse-primary))] focus:border-transparent"
        >
          <option value="NABIL">NABIL</option>
          <option value="NIL">NIL</option>
          <option value="SANIMA">SANIMA</option>
        </select>
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
      <div class="flex items-center gap-2">
        <!-- Chart Control Buttons -->
        <div class="flex items-center gap-1 border-r border-gray-300 pr-3 mr-3">
          <button
            @click="zoomIn"
            class="p-2 text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded transition-colors"
            title="Zoom In"
          >
            <svg
              class="w-4 h-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0zM10 7v3m0 0v3m0-3h3m-3 0H7"
              />
            </svg>
          </button>
          <button
            @click="zoomOut"
            class="p-2 text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded transition-colors"
            title="Zoom Out"
          >
            <svg
              class="w-4 h-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0zM13 10h3m0 0v3m0-3v-3m0 3H7"
              />
            </svg>
          </button>
          <button
            @click="fitContent"
            class="p-2 text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded transition-colors"
            title="Fit Content (Auto Scale)"
          >
            <svg
              class="w-4 h-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4"
              />
            </svg>
          </button>
          <button
            @click="toggleFullscreen"
            class="p-2 text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded transition-colors"
            title="Fullscreen Mode"
          >
            <svg
              class="w-4 h-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M21 3l-6 6m0 0V4m0 5h5M3 21l6-6m0 0v5m0-5H4"
              />
            </svg>
          </button>
        </div>
        <!-- Technical Indicators -->
        <div class="flex items-center gap-1">
          <button
            v-for="indicator in technicalIndicators"
            :key="indicator.id"
            @click="toggleIndicator(indicator.id)"
            :class="[
              'px-3 py-1 rounded-md text-sm font-medium transition-colors',
              indicator.active
                ? 'bg-green-100 text-green-800'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200',
            ]"
          >
            {{ indicator.name }}
          </button>
        </div>
      </div>
    </div>

    <!-- Main Chart Area -->
    <div class="bg-gray-50 rounded-xl p-6 relative">
      <!-- Loading Spinner -->
      <div v-if="isLoading" class="absolute inset-0 flex items-center justify-center bg-gray-50 bg-opacity-75 z-10">
        <div class="flex items-center space-x-2">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-[rgb(var(--color-nepse-primary))]"></div>
          <span class="text-gray-600">Loading chart data...</span>
        </div>
      </div>

      <!-- Error Message -->
      <div v-if="error && !isLoading" class="absolute inset-0 flex items-center justify-center bg-gray-50 z-10">
        <div class="text-center">
          <div class="text-red-500 text-lg font-semibold mb-2">Error Loading Data</div>
          <div class="text-gray-600">{{ error }}</div>
          <button
            @click="loadChartData"
            class="mt-4 px-4 py-2 bg-[rgb(var(--color-nepse-primary))] text-white rounded-lg hover:bg-opacity-90 transition-colors"
          >
            Retry
          </button>
        </div>
      </div>

      <!-- Combined Candlestick and Volume Chart -->
      <div class="h-96 w-full">
        <div ref="chartContainer" class="w-full h-full"></div>
      </div>

      <!-- Chart Overlay Information -->
      <div
        class="absolute top-4 left-4 bg-white rounded-lg shadow-sm p-3 text-sm z-10"
      >
        <div class="space-y-1">
          <div class="flex justify-between gap-8">
            <span class="text-gray-600">Current Price:</span>
            <span class="font-semibold">Rs. 1,235</span>
          </div>
          <div class="flex justify-between gap-8">
            <span class="text-gray-600">Stop Loss:</span>
            <span class="text-red-600 font-semibold">Rs. 1,180</span>
          </div>
          <div class="flex justify-between gap-8">
            <span class="text-gray-600">Take Profit:</span>
            <span class="text-green-600 font-semibold">Rs. 1,320</span>
          </div>
          <div class="flex justify-between gap-8">
            <span class="text-gray-600">R:R Ratio:</span>
            <span class="font-semibold">1:1.55</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Key Levels Panel -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="bg-red-50 p-4 rounded-lg border border-red-200">
        <h4 class="font-semibold text-red-800 mb-3 flex items-center gap-2">
          <TrendingDownIcon class="w-4 h-4" />
          Resistance Levels
        </h4>
        <div class="space-y-2 text-sm">
          <div class="flex justify-between">
            <span>Strong:</span>
            <span class="font-mono font-semibold">1,350</span>
          </div>
          <div class="flex justify-between">
            <span>Medium:</span>
            <span class="font-mono">1,280</span>
          </div>
          <div class="flex justify-between">
            <span>Weak:</span>
            <span class="font-mono">1,250</span>
          </div>
        </div>
      </div>

      <div class="bg-green-50 p-4 rounded-lg border border-green-200">
        <h4 class="font-semibold text-green-800 mb-3 flex items-center gap-2">
          <TrendingUpIcon class="w-4 h-4" />
          Support Levels
        </h4>
        <div class="space-y-2 text-sm">
          <div class="flex justify-between">
            <span>Strong:</span>
            <span class="font-mono font-semibold">1,150</span>
          </div>
          <div class="flex justify-between">
            <span>Medium:</span>
            <span class="font-mono">1,200</span>
          </div>
          <div class="flex justify-between">
            <span>Weak:</span>
            <span class="font-mono">1,220</span>
          </div>
        </div>
      </div>

      <div class="bg-blue-50 p-4 rounded-lg border border-blue-200">
        <h4 class="font-semibold text-blue-800 mb-3 flex items-center gap-2">
          <WaveIcon class="w-4 h-4" />
          Liquidity Zones
        </h4>
        <div class="space-y-2 text-sm">
          <div class="flex justify-between">
            <span>High Volume:</span>
            <span class="font-mono font-semibold">1,180-1,200</span>
          </div>
          <div class="flex justify-between">
            <span>Medium Volume:</span>
            <span class="font-mono">1,280-1,300</span>
          </div>
          <div class="flex justify-between">
            <span>Low Volume:</span>
            <span class="font-mono">1,320-1,340</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, onUnmounted, nextTick, watch } from "vue";
import ApexCharts from "apexcharts";
import TrendingUpIcon from "./icons/TrendingUpIcon.vue";
import TrendingDownIcon from "./icons/TrendingDownIcon.vue";
import WaveIcon from "./icons/WaveIcon.vue";
import { fetchCompanyHistory } from "../services/marketData_enhanced";

// Reactive state for data loading
const isLoading = ref(false);
const error = ref<string | null>(null);

// Parse API response data and format for ApexCharts
const parseHistoricalData = (apiData: any) => {
  const candlestickData = [];
  const volumeData = [];

  // Assuming apiData has structure like: { dates: [...], data: { open: [...], high: [...], low: [...], close: [...], volume: [...] } }
  // Adjust based on actual API response structure
  if (apiData && apiData.dates && apiData.data) {
    const { dates, data } = apiData;
    const { open, high, low, close, volume } = data;

    for (let i = 0; i < dates.length; i++) {
      const date = new Date(dates[i]);
      const timestamp = date.getTime();

      candlestickData.push([timestamp, [open[i], high[i], low[i], close[i]]]);
      volumeData.push([timestamp, volume[i]]);
    }
  }

  // Sort by time ascending
  return {
    candlestickData: candlestickData.sort((a: any[], b: any[]) => a[0] - b[0]),
    volumeData: volumeData.sort((a: any[], b: any[]) => a[0] - b[0]),
  };
};

const selectedStock = ref("NABIL");
const selectedTimeframe = ref("1D");
const chartContainer = ref<HTMLElement>();
let chart: any = null;
let chartCleanup: (() => void) | null = null;

const timeframes = ["5M", "15M", "1H", "4H", "1D", "1W", "1M"];
const technicalIndicators = reactive([
  { id: "ma", name: "MA", active: true },
  { id: "rsi", name: "RSI", active: false },
  { id: "macd", name: "MACD", active: true },
  { id: "bb", name: "BB", active: false },
]);

// Sample data for demonstration
const getSampleData = async () => {
  try {
    const response = await fetchCompanyHistory(selectedStock.value, 30);
    return parseHistoricalData(response);
  } catch (err) {
    console.error('Error fetching data:', err);
    error.value = 'Failed to load chart data';
    return { candlestickData: [], volumeData: [] };
  }
};

const initializeChart = async () => {
  if (!chartContainer.value) return;

  const { candlestickData, volumeData } = await getSampleData();

  // Create volume colors based on price movement
  const volumeColors = candlestickData.map((candle: any[]) => {
    const [, ohlc] = candle;
    const [open, , , close] = ohlc as number[];
    return close > open ? "#00C853" : "#FF1744"; // Green for increase, red for decrease
  });

  const options = {
    series: [
      {
        name: "Price",
        type: "candlestick",
        data: candlestickData,
      },
      {
        name: "Volume",
        type: "bar",
        data: volumeData,
        yAxisIndex: 1,
      },
    ],
    chart: {
      type: "candlestick",
      height: 450,
      id: "combo-chart",
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
      events: {
        zoomed: function (_chartContext: any, _xaxis: any) {
          // Handle zoom events if needed
        },
      },
    },
    plotOptions: {
      candlestick: {
        colors: {
          upward: "#00C853", // Green for bullish
          downward: "#FF1744", // Red for bearish
        },
      },
      bar: {
        columnWidth: "80%",
        colors: {
          ranges: volumeData.map((vol, index) => ({
            from: vol[1] * 0.99,
            to: vol[1] * 1.01,
            color: volumeColors[index],
          })),
        },
      },
    },
    xaxis: {
      type: "datetime",
      labels: {
        format: "dd MMM",
      },
    },
    yaxis: [
      {
        seriesName: "Price",
        opposite: false,
        title: {
          text: "Price (Rs.)",
        },
        labels: {
          formatter: function (value: any) {
            return "Rs. " + value.toFixed(2);
          },
        },
      },
      {
        seriesName: "Volume",
        opposite: true,
        show: true,
        title: {
          text: "Volume",
        },
        labels: {
          formatter: function (value: any) {
            return (value / 1000).toFixed(0) + "K";
          },
        },
        max: function (max: number) {
          return max * 4; // Scale volume to take less space
        },
      },
    ],
    grid: {
      show: true,
      borderColor: "#e1e1e1",
      strokeDashArray: 3,
    },
    tooltip: {
      shared: false,
      custom: function ({ series, seriesIndex, dataPointIndex, w }: any) {
        if (seriesIndex === 0) {
          // Candlestick tooltip
          const data = w.config.series[0].data[dataPointIndex];
          const [timestamp, [open, high, low, close]] = data;
          const date = new Date(timestamp);
          return `
            <div class="apexcharts-tooltip-candlestick">
              <div>Date: ${date.toLocaleDateString()}</div>
              <div>Open: ${open.toFixed(2)}</div>
              <div>High: ${high.toFixed(2)}</div>
              <div>Low: ${low.toFixed(2)}</div>
              <div>Close: ${close.toFixed(2)}</div>
            </div>
          `;
        } else {
          // Volume tooltip
          const volume = series[seriesIndex][dataPointIndex];
          return `
            <div class="apexcharts-tooltip-volume">
              <div>Volume: ${volume.toLocaleString()}</div>
            </div>
          `;
        }
      },
    },
    responsive: [
      {
        breakpoint: 768,
        options: {
          chart: {
            height: 300,
          },
        },
      },
    ],
  };

  // Create the chart
  chart = new ApexCharts(chartContainer.value, options);
  await chart.render();

  // Add keyboard shortcuts
  const handleKeyDown = (event: KeyboardEvent) => {
    if (event.ctrlKey || event.metaKey) {
      switch (event.key) {
        case "0":
          event.preventDefault();
          fitContent(); // Reset zoom
          break;
        case "+":
        case "=":
          event.preventDefault();
          zoomIn();
          break;
        case "-":
          event.preventDefault();
          zoomOut();
          break;
      }
    }
    if (event.key === "F11") {
      event.preventDefault();
      toggleFullscreen();
    }
  };

  document.addEventListener("keydown", handleKeyDown);

  // Store cleanup function
  const cleanup = () => {
    document.removeEventListener("keydown", handleKeyDown);
  };

  // Return cleanup function for onUnmounted
  return cleanup;
};

// Function to load chart data (for retry functionality)
const loadChartData = async () => {
  isLoading.value = true;
  error.value = null;
  await updateChartData();
  isLoading.value = false;
};

// Function to update chart data when stock changes
const updateChartData = async () => {
  if (chart) {
    const { candlestickData, volumeData } = await getSampleData();

    // Create volume colors based on price movement
    const volumeColors = candlestickData.map((candle: any[]) => {
      const [, ohlc] = candle;
      const [open, , , close] = ohlc as number[];
      return close > open ? "#00C853" : "#FF1744";
    });

    chart.updateSeries([
      {
        name: "candle",
        type: "candlestick",
        data: candlestickData,
      },
      {
        name: "volume",
        type: "bar",
        data: volumeData,
      },
    ]);

    // Update volume colors
    chart.updateOptions({
      plotOptions: {
        bar: {
          columnWidth: "80%",
          colors: {
            ranges: volumeColors.map((color: string, index: number) => ({
              from: volumeData[index][1] - 1,
              to: volumeData[index][1] + 1,
              color: color,
            })),
          },
        },
      },
    });
  }
};

const toggleIndicator = (id: string) => {
  const indicator = technicalIndicators.find((i) => i.id === id);
  if (indicator) {
    indicator.active = !indicator.active;
    // TODO: Implement actual indicator overlay
  }
};

// Chart control methods
const zoomIn = () => {
  if (chart) {
    // ApexCharts zoom in by reducing the visible range
    const currentRange =
      chart.w.globals.minX !== undefined && chart.w.globals.maxX !== undefined
        ? { min: chart.w.globals.minX, max: chart.w.globals.maxX }
        : chart.w.globals.initialMinX !== undefined &&
          chart.w.globals.initialMaxX !== undefined
        ? { min: chart.w.globals.initialMinX, max: chart.w.globals.initialMaxX }
        : null;

    if (currentRange) {
      const range = currentRange.max - currentRange.min;
      const center = (currentRange.min + currentRange.max) / 2;
      const newRange = range * 0.8; // Zoom in by 20%
      chart.zoomX(center - newRange / 2, center + newRange / 2);
    }
  }
};

const zoomOut = () => {
  if (chart) {
    // ApexCharts zoom out by increasing the visible range
    const currentRange =
      chart.w.globals.minX !== undefined && chart.w.globals.maxX !== undefined
        ? { min: chart.w.globals.minX, max: chart.w.globals.maxX }
        : chart.w.globals.initialMinX !== undefined &&
          chart.w.globals.initialMaxX !== undefined
        ? { min: chart.w.globals.initialMinX, max: chart.w.globals.initialMaxX }
        : null;

    if (currentRange) {
      const range = currentRange.max - currentRange.min;
      const center = (currentRange.min + currentRange.max) / 2;
      const newRange = range * 1.25; // Zoom out by 25%
      chart.zoomX(center - newRange / 2, center + newRange / 2);
    }
  }
};

const fitContent = () => {
  if (chart) {
    // Reset zoom to show all data
    chart.resetSeries();
  }
};

const toggleFullscreen = () => {
  if (!document.fullscreenElement) {
    // Enter fullscreen
    if (chartContainer.value?.requestFullscreen) {
      chartContainer.value.requestFullscreen().then(() => {
        // Adjust chart sizes after entering fullscreen
        setTimeout(() => {
          if (chart) {
            chart.updateOptions({
              chart: {
                height: window.innerHeight - 200,
              },
            });
          }
        }, 100);
      });
    }
  } else {
    // Exit fullscreen
    if (document.exitFullscreen) {
      document.exitFullscreen().then(() => {
        // Reset chart sizes
        setTimeout(() => {
          if (chart) {
            chart.updateOptions({
              chart: {
                height: 450,
              },
            });
          }
        }, 100);
      });
    }
  }
};

// Handle window resize
const handleResize = () => {
  if (chart && chartContainer.value) {
    const isFullscreen = !!document.fullscreenElement;
    chart.updateOptions({
      chart: {
        height: isFullscreen ? window.innerHeight - 200 : 450,
      },
    });
  }
};

// Handle fullscreen change
const handleFullscreenChange = () => {
  setTimeout(() => {
    handleResize();
  }, 100);
};

onMounted(async () => {
  await nextTick();
  isLoading.value = true;
  error.value = null;
  const cleanup = await initializeChart();
  isLoading.value = false;
  window.addEventListener("resize", handleResize);
  document.addEventListener("fullscreenchange", handleFullscreenChange);

  // Store cleanup for onUnmounted
  if (cleanup) {
    chartCleanup = cleanup;
  }
});

// Watch for stock selection changes and update chart data
watch(selectedStock, async () => {
  isLoading.value = true;
  error.value = null;
  await updateChartData();
  isLoading.value = false;
});

onUnmounted(() => {
  if (chart) {
    chart.destroy();
  }
  if (chartCleanup) {
    chartCleanup();
  }
  window.removeEventListener("resize", handleResize);
  document.removeEventListener("fullscreenchange", handleFullscreenChange);
});
</script>
