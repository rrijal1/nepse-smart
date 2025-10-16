// Enhanced Market Data Service - Using Our Own Data
import axios from "axios";

const API_BASE = "/api";

// Create axios instance with base configuration
const api = axios.create({
  baseURL: API_BASE,
  timeout: 10000,
  headers: {
    "Content-Type": "application/json",
  },
});

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error("API Error:", error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// Market Data Functions
export const fetchMarketSummary = async () => {
  try {
    const response = await api.get("/summary");
    return response.data;
  } catch (error) {
    console.error("Error fetching market summary:", error);
    return { error: "Failed to fetch market summary" };
  }
};

export const fetchTopGainers = async (limit = 10) => {
  try {
    const response = await api.get(`/top-gainers?limit=${limit}`);
    return response.data.gainers || [];
  } catch (error) {
    console.error("Error fetching top gainers:", error);
    return [];
  }
};

export const fetchTopLosers = async (limit = 10) => {
  try {
    const response = await api.get(`/top-losers?limit=${limit}`);
    return response.data.losers || [];
  } catch (error) {
    console.error("Error fetching top losers:", error);
    return [];
  }
};

export const fetchNepseIndex = async () => {
  try {
    const response = await api.get("/nepse-index");
    return response.data;
  } catch (error) {
    console.error("Error fetching NEPSE index:", error);
    return { error: "Failed to fetch NEPSE index" };
  }
};

export const fetchSubIndices = async () => {
  try {
    const response = await api.get("/sub-indices");
    return response.data.sub_indices || [];
  } catch (error) {
    console.error("Error fetching sub-indices:", error);
    return [];
  }
};

export const fetchPriceVolume = async (limit = null) => {
  try {
    const url = limit ? `/price-volume?limit=${limit}` : "/price-volume";
    const response = await api.get(url);
    return response.data.stocks || [];
  } catch (error) {
    console.error("Error fetching price volume:", error);
    return [];
  }
};

export const fetchCompanyList = async () => {
  try {
    const response = await api.get("/company-list");
    return response.data.companies || [];
  } catch (error) {
    console.error("Error fetching company list:", error);
    return [];
  }
};

// New Enhanced Functions
export const fetchMacroData = async () => {
  try {
    const response = await api.get("/macro-data");
    return response.data;
  } catch (error) {
    console.error("Error fetching macro data:", error);
    return { error: "Failed to fetch macro data" };
  }
};

export const fetchHistoricalData = async (
  dataType: string,
  days: number = 30
) => {
  try {
    const response = await api.get(`/historical/${dataType}?days=${days}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching historical ${dataType}:`, error);
    return { error: `Failed to fetch historical ${dataType}` };
  }
};

export const fetchCompanyHistory = async (
  symbol: string,
  days: number = 30
) => {
  try {
    const response = await api.get(`/company-history/${symbol}?days=${days}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching ${symbol} history:`, error);
    return { error: `Failed to fetch ${symbol} history` };
  }
};

export const searchStocks = async (query: string, limit: number = 20) => {
  try {
    const response = await api.get(
      `/search-stocks?query=${encodeURIComponent(query)}&limit=${limit}`
    );
    return response.data.results || [];
  } catch (error) {
    console.error("Error searching stocks:", error);
    return [];
  }
};

// System Monitoring Functions
export const fetchSystemStatus = async () => {
  try {
    const response = await api.get("/system-status");
    return response.data;
  } catch (error) {
    console.error("Error fetching system status:", error);
    return { error: "Failed to fetch system status" };
  }
};

export const fetchDataFreshness = async () => {
  try {
    const response = await api.get("/data-freshness");
    return response.data;
  } catch (error) {
    console.error("Error fetching data freshness:", error);
    return { error: "Failed to fetch data freshness" };
  }
};

export const fetchDataQuality = async () => {
  try {
    const response = await api.get("/data-quality");
    return response.data;
  } catch (error) {
    console.error("Error fetching data quality:", error);
    return { error: "Failed to fetch data quality" };
  }
};

export const checkMarketStatus = async () => {
  try {
    const response = await api.get("/market-status");
    return response.data;
  } catch (error) {
    console.error("Error checking market status:", error);
    return { error: "Failed to check market status", is_open: false };
  }
};

// Utility Functions
export const formatCurrency = (value: number | null | undefined): string => {
  if (value === null || value === undefined) return "N/A";
  return new Intl.NumberFormat("en-NP", {
    style: "currency",
    currency: "NPR",
    minimumFractionDigits: 2,
  }).format(value);
};

export const formatPercentage = (value: number | null | undefined): string => {
  if (value === null || value === undefined) return "N/A";
  const sign = value >= 0 ? "+" : "";
  return `${sign}${value.toFixed(2)}%`;
};

export const formatNumber = (value: number | null | undefined): string => {
  if (value === null || value === undefined) return "N/A";
  return new Intl.NumberFormat("en-NP").format(value);
};

// Export default api instance for direct use
export default api;
