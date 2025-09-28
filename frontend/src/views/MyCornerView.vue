<template>
  <div class="flex h-[calc(100vh-120px)]">
    <!-- Left Sidebar -->
    <div class="w-80 bg-white shadow-lg rounded-lg mr-6 overflow-hidden">
      <div
        class="p-4 bg-gradient-to-r from-[rgb(var(--color-nepse-primary))] to-[rgb(var(--color-nepse-secondary))] text-white"
      >
        <h2 class="text-lg font-semibold">My Corner</h2>
        <p class="text-sm opacity-90">Your personalized trading hub</p>
      </div>

      <!-- Navigation Menu -->
      <nav class="p-2">
        <div class="space-y-1">
          <button
            v-for="item in sidebarItems"
            :key="item.id"
            @click="activeSection = item.id"
            :class="[
              'w-full flex items-center gap-3 px-4 py-3 text-left rounded-lg transition-all duration-200',
              activeSection === item.id
                ? 'bg-[rgb(var(--color-nepse-primary))]/10 text-[rgb(var(--color-nepse-primary))] font-semibold border-l-4 ]'
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

    <!-- Main Content Area -->
    <div class="flex-1 bg-white rounded-lg shadow-lg overflow-hidden">
      <!-- Content Header -->
      <div class="p-6 border-b border-gray-200 bg-gray-50">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-2xl font-bold text-gray-900">
              {{ getCurrentSectionTitle() }}
            </h1>
            <p class="text-gray-600 mt-1">
              {{ getCurrentSectionDescription() }}
            </p>
          </div>
          <div class="flex items-center gap-3">
            <button
              class="px-4 py-2 bg-[rgb(var(--color-nepse-primary))] text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              <PlusIcon class="w-4 h-4 inline mr-2" />
              Add to Watchlist
            </button>
          </div>
        </div>
      </div>

      <!-- Dynamic Content -->
      <div class="p-6 h-full overflow-y-auto">
        <!-- Watchlist Section -->
        <div v-if="activeSection === 'watchlist'" class="space-y-6">
          <!-- Portfolio Summary Cards -->
          <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-6">
            <div
              class="bg-gradient-to-br from-green-50 to-green-100 p-6 rounded-xl border border-green-200"
            >
              <div class="flex items-center justify-between mb-4">
                <h3 class="font-semibold text-green-800">Total Portfolio</h3>
                <TrendingUpIcon class="w-5 h-5 text-green-600" />
              </div>
              <div class="text-2xl font-bold text-green-700">Rs. 12,45,000</div>
              <div class="text-sm text-green-600 mt-1">+Rs. 45,000 (3.75%)</div>
            </div>

            <div
              class="bg-gradient-to-br from-blue-50 to-blue-100 p-6 rounded-xl border border-blue-200"
            >
              <div class="flex items-center justify-between mb-4">
                <h3 class="font-semibold text-blue-800">Day's P&L</h3>
                <ChartIcon class="w-5 h-5 text-blue-600" />
              </div>
              <div class="text-2xl font-bold text-blue-700">+Rs. 8,500</div>
              <div class="text-sm text-blue-600 mt-1">+0.68% today</div>
            </div>

            <div
              class="bg-gradient-to-br from-purple-50 to-purple-100 p-6 rounded-xl border border-purple-200"
            >
              <div class="flex items-center justify-between mb-4">
                <h3 class="font-semibold text-purple-800">Holdings</h3>
                <PortfolioIcon class="w-5 h-5 text-purple-600" />
              </div>
              <div class="text-2xl font-bold text-purple-700">15</div>
              <div class="text-sm text-purple-600 mt-1">
                Stocks in portfolio
              </div>
            </div>

            <div
              class="bg-gradient-to-br from-yellow-50 to-yellow-100 p-6 rounded-xl border border-yellow-200"
            >
              <div class="flex items-center justify-between mb-4">
                <h3 class="font-semibold text-yellow-800">Cash Available</h3>
                <WalletIcon class="w-5 h-5 text-yellow-600" />
              </div>
              <div class="text-2xl font-bold text-yellow-700">Rs. 2,50,000</div>
              <div class="text-sm text-yellow-600 mt-1">Ready to invest</div>
            </div>
          </div>

          <!-- Watchlist Table -->
          <div
            class="bg-white border border-gray-200 rounded-xl overflow-hidden"
          >
            <div class="px-6 py-4 border-b border-gray-200 bg-gray-50">
              <h3 class="text-lg font-semibold text-gray-800">My Watchlist</h3>
            </div>
            <div class="overflow-x-auto">
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
                      Volume
                    </th>
                    <th
                      class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider"
                    >
                      Holdings
                    </th>
                    <th
                      class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider"
                    >
                      Action
                    </th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr
                    v-for="stock in watchlistStocks"
                    :key="stock.symbol"
                    class="hover:bg-gray-50"
                  >
                    <td class="px-6 py-4 whitespace-nowrap">
                      <div class="flex items-center">
                        <div class="font-semibold text-gray-900">
                          {{ stock.symbol }}
                        </div>
                        <StarIcon
                          :class="[
                            'w-4 h-4 ml-2 cursor-pointer',
                            stock.favorite
                              ? 'text-yellow-500 fill-current'
                              : 'text-gray-300',
                          ]"
                          @click="toggleFavorite(stock.symbol)"
                        />
                      </div>
                    </td>
                    <td
                      class="px-6 py-4 whitespace-nowrap text-right font-mono font-semibold"
                    >
                      Rs. {{ stock.ltp.toLocaleString() }}
                    </td>
                    <td
                      class="px-6 py-4 whitespace-nowrap text-right font-mono font-semibold"
                      :class="
                        stock.change >= 0 ? 'text-green-600' : 'text-red-600'
                      "
                    >
                      {{ stock.change >= 0 ? "+" : "" }}{{ stock.change }}
                    </td>
                    <td
                      class="px-6 py-4 whitespace-nowrap text-right font-mono font-semibold"
                      :class="
                        stock.changePercent >= 0
                          ? 'text-green-600'
                          : 'text-red-600'
                      "
                    >
                      {{ stock.changePercent >= 0 ? "+" : ""
                      }}{{ stock.changePercent }}%
                    </td>
                    <td
                      class="px-6 py-4 whitespace-nowrap text-right font-mono text-sm text-gray-600"
                    >
                      {{ stock.volume }}
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-right">
                      <div v-if="stock.holdings > 0" class="text-sm">
                        <div class="font-semibold text-gray-900">
                          {{ stock.holdings }} shares
                        </div>
                        <div class="text-gray-600">
                          Avg: Rs. {{ stock.avgPrice }}
                        </div>
                      </div>
                      <div v-else class="text-gray-400 text-sm">
                        Not holding
                      </div>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-center">
                      <button
                        class="text-[rgb(var(--color-nepse-primary))] hover:text-blue-700 text-sm font-medium"
                      >
                        Trade
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- News & Updates Section -->
        <div v-if="activeSection === 'news'" class="space-y-6">
          <!-- Filter Tabs -->
          <div class="flex items-center gap-4 mb-6">
            <div class="flex bg-gray-100 rounded-lg p-1">
              <button
                v-for="filter in newsFilters"
                :key="filter"
                @click="activeNewsFilter = filter"
                :class="[
                  'px-4 py-2 rounded-md text-sm font-medium transition-colors',
                  activeNewsFilter === filter
                    ? 'bg-white text-[rgb(var(--color-nepse-primary))] shadow-sm'
                    : 'text-gray-600 hover:text-gray-900',
                ]"
              >
                {{ filter }}
              </button>
            </div>
          </div>

          <!-- News Cards -->
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div
              v-for="news in filteredNews"
              :key="news.id"
              class="bg-white border border-gray-200 rounded-xl p-6 hover:shadow-md transition-shadow cursor-pointer"
            >
              <div class="flex items-start justify-between mb-4">
                <div class="flex items-center gap-2">
                  <span
                    :class="[
                      'px-2 py-1 rounded-full text-xs font-medium',
                      news.priority === 'high'
                        ? 'bg-red-100 text-red-800'
                        : news.priority === 'medium'
                        ? 'bg-yellow-100 text-yellow-800'
                        : 'bg-gray-100 text-gray-800',
                    ]"
                  >
                    {{ news.category }}
                  </span>
                  <span class="text-xs text-gray-500">{{ news.time }}</span>
                </div>
                <NewsIcon class="w-5 h-5 text-gray-400" />
              </div>
              <h3 class="font-semibold text-gray-800 mb-2">{{ news.title }}</h3>
              <p class="text-gray-600 text-sm mb-4">{{ news.excerpt }}</p>
              <div class="flex items-center justify-between">
                <span class="text-xs text-gray-500">{{ news.source }}</span>
                <button
                  class="text-[rgb(var(--color-nepse-primary))] text-sm font-medium hover:underline"
                >
                  Read More →
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Fundamentals Section -->
        <div v-if="activeSection === 'fundamentals'" class="space-y-6">
          <!-- Stock Screener -->
          <div class="bg-gray-50 p-6 rounded-xl">
            <h3 class="text-lg font-semibold text-gray-800 mb-4">
              Stock Screener
            </h3>
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2"
                  >Market Cap</label
                >
                <select
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[rgb(var(--color-nepse-primary))] focus:border-transparent"
                >
                  <option>Any</option>
                  <option>Large Cap</option>
                  <option>Mid Cap</option>
                  <option>Small Cap</option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2"
                  >P/E Ratio</label
                >
                <select
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[rgb(var(--color-nepse-primary))] focus:border-transparent"
                >
                  <option>Any</option>
                  <option>< 15</option>
                  <option>15-25</option>
                  <option>> 25</option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2"
                  >ROE</label
                >
                <select
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[rgb(var(--color-nepse-primary))] focus:border-transparent"
                >
                  <option>Any</option>
                  <option>> 15%</option>
                  <option>10-15%</option>
                  <option>< 10%</option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2"
                  >Debt/Equity</label
                >
                <select
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[rgb(var(--color-nepse-primary))] focus:border-transparent"
                >
                  <option>Any</option>
                  <option>< 0.5</option>
                  <option>0.5-1.0</option>
                  <option>> 1.0</option>
                </select>
              </div>
            </div>
            <button
              class="mt-4 px-6 py-2 bg-[rgb(var(--color-nepse-primary))] text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              Apply Filters
            </button>
          </div>

          <!-- Fundamental Analysis Results -->
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div
              v-for="stock in fundamentalStocks"
              :key="stock.symbol"
              class="bg-white border border-gray-200 rounded-xl p-6"
            >
              <div class="flex items-center justify-between mb-4">
                <h3 class="font-semibold text-gray-800">{{ stock.symbol }}</h3>
                <span
                  :class="[
                    'px-2 py-1 rounded-full text-xs font-medium',
                    stock.rating === 'Strong Buy'
                      ? 'bg-green-100 text-green-800'
                      : stock.rating === 'Buy'
                      ? 'bg-blue-100 text-blue-800'
                      : stock.rating === 'Hold'
                      ? 'bg-yellow-100 text-yellow-800'
                      : 'bg-red-100 text-red-800',
                  ]"
                >
                  {{ stock.rating }}
                </span>
              </div>
              <div class="grid grid-cols-2 gap-4 text-sm">
                <div class="space-y-2">
                  <div class="flex justify-between">
                    <span class="text-gray-600">P/E Ratio:</span>
                    <span class="font-semibold">{{ stock.pe }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-gray-600">ROE:</span>
                    <span class="font-semibold">{{ stock.roe }}%</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-gray-600">ROA:</span>
                    <span class="font-semibold">{{ stock.roa }}%</span>
                  </div>
                </div>
                <div class="space-y-2">
                  <div class="flex justify-between">
                    <span class="text-gray-600">Book Value:</span>
                    <span class="font-semibold">Rs. {{ stock.bookValue }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-gray-600">EPS:</span>
                    <span class="font-semibold">Rs. {{ stock.eps }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-gray-600">Debt/Equity:</span>
                    <span class="font-semibold">{{ stock.debtEquity }}</span>
                  </div>
                </div>
              </div>
              <button
                class="w-full mt-4 px-4 py-2 border border-[rgb(var(--color-nepse-primary))] text-[rgb(var(--color-nepse-primary))] rounded-lg hover:bg-[rgb(var(--color-nepse-primary))]/10 transition-colors text-sm font-medium"
              >
                View Details
              </button>
            </div>
          </div>
        </div>

        <!-- Technical Analysis Section -->
        <div v-if="activeSection === 'technical'" class="space-y-6">
          <!-- Technical Screener -->
          <div class="bg-gray-50 p-6 rounded-xl">
            <h3 class="text-lg font-semibold text-gray-800 mb-4">
              Technical Screener
            </h3>
            <div class="grid grid-cols-1 md:grid-cols-5 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2"
                  >RSI</label
                >
                <select
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[rgb(var(--color-nepse-primary))] focus:border-transparent"
                >
                  <option>Any</option>
                  <option>Overbought (>70)</option>
                  <option>Oversold (<30)</option>
                  <option>Neutral (30-70)</option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2"
                  >MACD</label
                >
                <select
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[rgb(var(--color-nepse-primary))] focus:border-transparent"
                >
                  <option>Any</option>
                  <option>Bullish Crossover</option>
                  <option>Bearish Crossover</option>
                  <option>Above Signal</option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2"
                  >Moving Average</label
                >
                <select
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[rgb(var(--color-nepse-primary))] focus:border-transparent"
                >
                  <option>Any</option>
                  <option>Above 50 SMA</option>
                  <option>Below 50 SMA</option>
                  <option>Golden Cross</option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2"
                  >Volume</label
                >
                <select
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[rgb(var(--color-nepse-primary))] focus:border-transparent"
                >
                  <option>Any</option>
                  <option>Above Average</option>
                  <option>High Volume</option>
                  <option>Low Volume</option>
                </select>
              </div>
              <div class="flex items-end">
                <button
                  class="w-full px-4 py-2 bg-[rgb(var(--color-nepse-primary))] text-white rounded-lg hover:bg-blue-700 transition-colors"
                >
                  Scan
                </button>
              </div>
            </div>
          </div>

          <!-- Technical Analysis Results -->
          <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div
              v-for="stock in technicalStocks"
              :key="stock.symbol"
              class="bg-white border border-gray-200 rounded-xl p-6"
            >
              <div class="flex items-center justify-between mb-4">
                <h3 class="font-semibold text-gray-800">{{ stock.symbol }}</h3>
                <span
                  :class="[
                    'px-2 py-1 rounded-full text-xs font-medium',
                    stock.signal === 'Strong Buy'
                      ? 'bg-green-100 text-green-800'
                      : stock.signal === 'Buy'
                      ? 'bg-blue-100 text-blue-800'
                      : stock.signal === 'Hold'
                      ? 'bg-yellow-100 text-yellow-800'
                      : 'bg-red-100 text-red-800',
                  ]"
                >
                  {{ stock.signal }}
                </span>
              </div>
              <div class="space-y-3 text-sm">
                <div class="flex items-center justify-between">
                  <span class="text-gray-600">RSI (14):</span>
                  <span
                    :class="[
                      'font-semibold',
                      stock.rsi > 70
                        ? 'text-red-600'
                        : stock.rsi < 30
                        ? 'text-green-600'
                        : 'text-gray-800',
                    ]"
                    >{{ stock.rsi }}</span
                  >
                </div>
                <div class="flex items-center justify-between">
                  <span class="text-gray-600">MACD:</span>
                  <span
                    :class="[
                      'font-semibold',
                      stock.macd === 'Bullish'
                        ? 'text-green-600'
                        : stock.macd === 'Bearish'
                        ? 'text-red-600'
                        : 'text-gray-800',
                    ]"
                    >{{ stock.macd }}</span
                  >
                </div>
                <div class="flex items-center justify-between">
                  <span class="text-gray-600">Support:</span>
                  <span class="font-mono font-semibold"
                    >Rs. {{ stock.support }}</span
                  >
                </div>
                <div class="flex items-center justify-between">
                  <span class="text-gray-600">Resistance:</span>
                  <span class="font-mono font-semibold"
                    >Rs. {{ stock.resistance }}</span
                  >
                </div>
                <div class="flex items-center justify-between">
                  <span class="text-gray-600">Volume Trend:</span>
                  <span
                    :class="[
                      'font-semibold',
                      stock.volumeTrend === 'High'
                        ? 'text-green-600'
                        : stock.volumeTrend === 'Low'
                        ? 'text-red-600'
                        : 'text-gray-800',
                    ]"
                    >{{ stock.volumeTrend }}</span
                  >
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Portfolio Section -->
        <div v-if="activeSection === 'portfolio'" class="space-y-6">
          <!-- Portfolio Performance Chart -->
          <div class="bg-white border border-gray-200 rounded-xl p-6">
            <h3 class="text-lg font-semibold text-gray-800 mb-4">
              Portfolio Performance
            </h3>
            <div
              class="h-64 bg-gray-50 rounded-lg flex items-center justify-center"
            >
              <div class="text-center">
                <ChartIcon class="w-12 h-12 text-gray-400 mx-auto mb-2" />
                <p class="text-gray-600">Portfolio performance chart</p>
                <p class="text-sm text-gray-500">+15.8% overall return</p>
              </div>
            </div>
          </div>

          <!-- Holdings Table -->
          <div
            class="bg-white border border-gray-200 rounded-xl overflow-hidden"
          >
            <div class="px-6 py-4 border-b border-gray-200 bg-gray-50">
              <h3 class="text-lg font-semibold text-gray-800">
                Current Holdings
              </h3>
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
                    <td
                      class="px-6 py-4 whitespace-nowrap text-right font-mono"
                    >
                      {{ holding.quantity }}
                    </td>
                    <td
                      class="px-6 py-4 whitespace-nowrap text-right font-mono"
                    >
                      Rs. {{ holding.avgPrice.toLocaleString() }}
                    </td>
                    <td
                      class="px-6 py-4 whitespace-nowrap text-right font-mono"
                    >
                      Rs. {{ holding.currentPrice.toLocaleString() }}
                    </td>
                    <td
                      class="px-6 py-4 whitespace-nowrap text-right font-mono font-semibold"
                      :class="
                        holding.pnl >= 0 ? 'text-green-600' : 'text-red-600'
                      "
                    >
                      {{ holding.pnl >= 0 ? "+" : "" }}Rs.
                      {{ Math.abs(holding.pnl).toLocaleString() }}
                    </td>
                    <td
                      class="px-6 py-4 whitespace-nowrap text-right font-mono font-semibold"
                      :class="
                        holding.pnlPercent >= 0
                          ? 'text-green-600'
                          : 'text-red-600'
                      "
                    >
                      {{ holding.pnlPercent >= 0 ? "+" : ""
                      }}{{ holding.pnlPercent }}%
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from "vue";

import { defineComponent, h } from "vue";

// My Corner section icons - Using Vue 3 render functions
const TrendingUpIcon = defineComponent({
  name: "TrendingUpIcon",
  render: () =>
    h(
      "svg",
      {
        fill: "none",
        stroke: "currentColor",
        viewBox: "0 0 24 24",
        xmlns: "http://www.w3.org/2000/svg",
      },
      [
        h("path", {
          "stroke-linecap": "round",
          "stroke-linejoin": "round",
          "stroke-width": "2",
          d: "M13 7h8m0 0v8m0-8l-8 8-4-4-6 6",
        }),
      ]
    ),
});

const ChartIcon = defineComponent({
  name: "ChartIcon",
  render: () =>
    h(
      "svg",
      {
        fill: "none",
        stroke: "currentColor",
        viewBox: "0 0 24 24",
        xmlns: "http://www.w3.org/2000/svg",
      },
      [
        h("path", {
          "stroke-linecap": "round",
          "stroke-linejoin": "round",
          "stroke-width": "2",
          d: "M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z",
        }),
      ]
    ),
});

const PortfolioIcon = defineComponent({
  name: "PortfolioIcon",
  render: () =>
    h(
      "svg",
      {
        fill: "none",
        stroke: "currentColor",
        viewBox: "0 0 24 24",
        xmlns: "http://www.w3.org/2000/svg",
      },
      [
        h("path", {
          "stroke-linecap": "round",
          "stroke-linejoin": "round",
          "stroke-width": "2",
          d: "M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4",
        }),
      ]
    ),
});

const WalletIcon = defineComponent({
  name: "WalletIcon",
  render: () =>
    h(
      "svg",
      {
        fill: "none",
        stroke: "currentColor",
        viewBox: "0 0 24 24",
        xmlns: "http://www.w3.org/2000/svg",
      },
      [
        h("path", {
          "stroke-linecap": "round",
          "stroke-linejoin": "round",
          "stroke-width": "2",
          d: "M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z",
        }),
      ]
    ),
});

const StarIcon = defineComponent({
  name: "StarIcon",
  render: () =>
    h(
      "svg",
      {
        fill: "none",
        stroke: "currentColor",
        viewBox: "0 0 24 24",
        xmlns: "http://www.w3.org/2000/svg",
      },
      [
        h("path", {
          "stroke-linecap": "round",
          "stroke-linejoin": "round",
          "stroke-width": "2",
          d: "M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z",
        }),
      ]
    ),
});

const NewsIcon = defineComponent({
  name: "NewsIcon",
  render: () =>
    h(
      "svg",
      {
        fill: "none",
        stroke: "currentColor",
        viewBox: "0 0 24 24",
        xmlns: "http://www.w3.org/2000/svg",
      },
      [
        h("path", {
          "stroke-linecap": "round",
          "stroke-linejoin": "round",
          "stroke-width": "2",
          d: "M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z",
        }),
      ]
    ),
});

const PlusIcon = defineComponent({
  name: "PlusIcon",
  render: () =>
    h(
      "svg",
      {
        fill: "none",
        stroke: "currentColor",
        viewBox: "0 0 24 24",
        xmlns: "http://www.w3.org/2000/svg",
      },
      [
        h("path", {
          "stroke-linecap": "round",
          "stroke-linejoin": "round",
          "stroke-width": "2",
          d: "M12 6v6m0 0v6m0-6h6m-6 0H6",
        }),
      ]
    ),
});

const EyeIcon = defineComponent({
  name: "EyeIcon",
  render: () =>
    h(
      "svg",
      {
        fill: "none",
        stroke: "currentColor",
        viewBox: "0 0 24 24",
        xmlns: "http://www.w3.org/2000/svg",
      },
      [
        h("path", {
          "stroke-linecap": "round",
          "stroke-linejoin": "round",
          "stroke-width": "2",
          d: "M15 12a3 3 0 11-6 0 3 3 0 016 0z",
        }),
        h("path", {
          "stroke-linecap": "round",
          "stroke-linejoin": "round",
          "stroke-width": "2",
          d: "M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z",
        }),
      ]
    ),
});

const DocumentIcon = defineComponent({
  name: "DocumentIcon",
  render: () =>
    h(
      "svg",
      {
        fill: "none",
        stroke: "currentColor",
        viewBox: "0 0 24 24",
        xmlns: "http://www.w3.org/2000/svg",
      },
      [
        h("path", {
          "stroke-linecap": "round",
          "stroke-linejoin": "round",
          "stroke-width": "2",
          d: "M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z",
        }),
      ]
    ),
});

// Reactive data
const activeSection = ref("watchlist");
const activeNewsFilter = ref("All");

// Sidebar items
const sidebarItems = [
  { id: "watchlist", label: "My Watchlist", icon: EyeIcon },
  { id: "news", label: "News & Updates", icon: NewsIcon, badge: "12" },
  { id: "fundamentals", label: "Fundamentals", icon: DocumentIcon },
  { id: "technical", label: "Technical Analysis", icon: ChartIcon },
  { id: "portfolio", label: "Portfolio", icon: PortfolioIcon },
];

// News filters
const newsFilters = [
  "All",
  "My Stocks",
  "Banking",
  "Insurance",
  "Hydropower",
  "Finance",
];

// Sample data
const watchlistStocks = reactive([
  {
    symbol: "NABIL",
    ltp: 1235,
    change: 45,
    changePercent: 3.78,
    volume: "2.3M",
    holdings: 100,
    avgPrice: 1180,
    favorite: true,
  },
  {
    symbol: "SCBL",
    ltp: 567,
    change: -12,
    changePercent: -2.07,
    volume: "1.8M",
    holdings: 0,
    avgPrice: 0,
    favorite: false,
  },
  {
    symbol: "HBL",
    ltp: 689,
    change: 28,
    changePercent: 4.24,
    volume: "1.5M",
    holdings: 50,
    avgPrice: 650,
    favorite: true,
  },
  {
    symbol: "EBL",
    ltp: 890,
    change: 35,
    changePercent: 4.09,
    volume: "1.2M",
    holdings: 75,
    avgPrice: 820,
    favorite: false,
  },
  {
    symbol: "UPPER",
    ltp: 456,
    change: -23,
    changePercent: -4.79,
    volume: "3.2M",
    holdings: 200,
    avgPrice: 480,
    favorite: true,
  },
]);

const newsItems = reactive([
  {
    id: 1,
    title: "NABIL Bank Reports Strong Q3 Results",
    excerpt: "Net profit increased by 18% compared to previous quarter...",
    category: "Banking",
    priority: "high",
    source: "Company Report",
    time: "2 hours ago",
  },
  {
    id: 2,
    title: "Hydropower Sector Gets Government Support",
    excerpt: "New policy framework announced to boost renewable energy...",
    category: "Hydropower",
    priority: "medium",
    source: "Government News",
    time: "4 hours ago",
  },
  {
    id: 3,
    title: "SCBL Announces Dividend Distribution",
    excerpt: "Board recommends 15% bonus shares for shareholders...",
    category: "Banking",
    priority: "high",
    source: "Corporate Action",
    time: "6 hours ago",
  },
  {
    id: 4,
    title: "Market Analysis: Banking Sector Outlook",
    excerpt: "Expert analysis suggests continued growth in banking sector...",
    category: "Analysis",
    priority: "low",
    source: "Market Analysis",
    time: "8 hours ago",
  },
]);

const fundamentalStocks = reactive([
  {
    symbol: "NABIL",
    rating: "Strong Buy",
    pe: 12.5,
    roe: 18.2,
    roa: 2.1,
    bookValue: 890,
    eps: 98.7,
    debtEquity: 0.3,
  },
  {
    symbol: "SCBL",
    rating: "Buy",
    pe: 15.2,
    roe: 16.8,
    roa: 1.9,
    bookValue: 456,
    eps: 37.3,
    debtEquity: 0.4,
  },
  {
    symbol: "HBL",
    rating: "Hold",
    pe: 18.7,
    roe: 14.5,
    roa: 1.7,
    bookValue: 523,
    eps: 36.8,
    debtEquity: 0.5,
  },
  {
    symbol: "EBL",
    rating: "Buy",
    pe: 14.1,
    roe: 17.3,
    roa: 2.0,
    bookValue: 678,
    eps: 63.1,
    debtEquity: 0.35,
  },
]);

const technicalStocks = reactive([
  {
    symbol: "NABIL",
    signal: "Strong Buy",
    rsi: 45,
    macd: "Bullish",
    support: 1180,
    resistance: 1280,
    volumeTrend: "High",
  },
  {
    symbol: "SCBL",
    signal: "Sell",
    rsi: 75,
    macd: "Bearish",
    support: 520,
    resistance: 580,
    volumeTrend: "Low",
  },
  {
    symbol: "HBL",
    signal: "Buy",
    rsi: 55,
    macd: "Bullish",
    support: 650,
    resistance: 720,
    volumeTrend: "Medium",
  },
  {
    symbol: "EBL",
    signal: "Hold",
    rsi: 60,
    macd: "Neutral",
    support: 850,
    resistance: 920,
    volumeTrend: "Medium",
  },
  {
    symbol: "UPPER",
    signal: "Strong Sell",
    rsi: 25,
    macd: "Bearish",
    support: 420,
    resistance: 480,
    volumeTrend: "High",
  },
  {
    symbol: "CHCL",
    signal: "Buy",
    rsi: 35,
    macd: "Bullish",
    support: 480,
    resistance: 550,
    volumeTrend: "High",
  },
]);

const portfolioHoldings = reactive([
  {
    symbol: "NABIL",
    quantity: 100,
    avgPrice: 1180,
    currentPrice: 1235,
    pnl: 5500,
    pnlPercent: 4.66,
  },
  {
    symbol: "HBL",
    quantity: 50,
    avgPrice: 650,
    currentPrice: 689,
    pnl: 1950,
    pnlPercent: 6.0,
  },
  {
    symbol: "EBL",
    quantity: 75,
    avgPrice: 820,
    currentPrice: 890,
    pnl: 5250,
    pnlPercent: 8.54,
  },
  {
    symbol: "UPPER",
    quantity: 200,
    avgPrice: 480,
    currentPrice: 456,
    pnl: -4800,
    pnlPercent: -5.0,
  },
  {
    symbol: "BOKL",
    quantity: 150,
    avgPrice: 320,
    currentPrice: 345,
    pnl: 3750,
    pnlPercent: 7.81,
  },
]);

// Computed properties
const filteredNews = computed(() => {
  if (activeNewsFilter.value === "All") return newsItems;
  if (activeNewsFilter.value === "My Stocks") {
    const myStockSymbols = watchlistStocks
      .filter((s) => s.holdings > 0)
      .map((s) => s.symbol);
    return newsItems.filter((news) =>
      myStockSymbols.some((symbol) => news.title.includes(symbol))
    );
  }
  return newsItems.filter((news) => news.category === activeNewsFilter.value);
});

// Methods
const getCurrentSectionTitle = () => {
  const section = sidebarItems.find((item) => item.id === activeSection.value);
  return section ? section.label : "My Corner";
};

const getCurrentSectionDescription = () => {
  const descriptions: Record<string, string> = {
    watchlist: "Monitor your favorite stocks and portfolio performance",
    news: "Stay updated with news relevant to your investments",
    fundamentals: "Analyze stocks based on financial metrics and ratios",
    technical: "Technical analysis and trading signals for your stocks",
    portfolio: "Track your portfolio performance and holdings",
  };
  return descriptions[activeSection.value] || "Your personalized trading hub";
};

const toggleFavorite = (symbol: string) => {
  const stock = watchlistStocks.find((s) => s.symbol === symbol);
  if (stock) {
    stock.favorite = !stock.favorite;
  }
};
</script>
