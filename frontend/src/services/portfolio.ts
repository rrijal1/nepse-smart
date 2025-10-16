import axios from "axios";

// Use relative URLs so Vite proxy can handle requests in development
// In production, nginx will proxy /api requests to the backend
const API_BASE_URL = "";

// ==================== TYPES ====================

export interface WatchlistItem {
  id: number;
  symbol: string;
  added_date: string;
  favorite: boolean;
  notes?: string;
  created_at: string;
  ltp?: number;
  change?: number;
  change_percent?: number;
  volume?: string;
  holdings?: number;
  avg_holding_price?: number;
}

export interface PortfolioHolding {
  id: number;
  symbol: string;
  quantity: number;
  avg_price: number;
  buy_date: string;
  notes?: string;
  created_at: string;
  invested_amount: number;
  current_price?: number;
  current_value?: number;
  pnl?: number;
  pnl_percent?: number;
}

export interface PortfolioSummary {
  total_invested: number;
  current_value: number;
  total_pnl: number;
  total_pnl_percent: number;
  day_pnl: number;
  day_pnl_percent: number;
  total_holdings: number;
  cash_available: number;
}

export interface Transaction {
  id: number;
  symbol: string;
  transaction_type: "buy" | "sell";
  quantity: number;
  price: number;
  transaction_date: string;
  notes?: string;
  total_amount: number;
  created_at: string;
}

// ==================== WATCHLIST API ====================

export async function fetchWatchlist(): Promise<WatchlistItem[]> {
  try {
    const response = await axios.get(`${API_BASE_URL}/api/watchlist`);
    return response.data;
  } catch (error) {
    console.error("Error fetching watchlist:", error);
    throw error;
  }
}

export async function addToWatchlist(
  symbol: string,
  favorite: boolean = false,
  notes?: string
): Promise<WatchlistItem> {
  try {
    const response = await axios.post(`${API_BASE_URL}/api/watchlist`, {
      symbol,
      favorite,
      notes,
    });
    return response.data;
  } catch (error) {
    console.error("Error adding to watchlist:", error);
    throw error;
  }
}

export async function updateWatchlistItem(
  id: number,
  updates: { favorite?: boolean; notes?: string }
): Promise<WatchlistItem> {
  try {
    const response = await axios.patch(
      `${API_BASE_URL}/api/watchlist/${id}`,
      updates
    );
    return response.data;
  } catch (error) {
    console.error("Error updating watchlist item:", error);
    throw error;
  }
}

export async function removeFromWatchlist(id: number): Promise<void> {
  try {
    await axios.delete(`${API_BASE_URL}/api/watchlist/${id}`);
  } catch (error) {
    console.error("Error removing from watchlist:", error);
    throw error;
  }
}

// ==================== PORTFOLIO API ====================

export async function fetchPortfolio(): Promise<PortfolioHolding[]> {
  try {
    const response = await axios.get(`${API_BASE_URL}/api/portfolio`);
    return response.data;
  } catch (error) {
    console.error("Error fetching portfolio:", error);
    throw error;
  }
}

export async function fetchPortfolioSummary(): Promise<PortfolioSummary> {
  try {
    const response = await axios.get(`${API_BASE_URL}/api/portfolio/summary`);
    return response.data;
  } catch (error) {
    console.error("Error fetching portfolio summary:", error);
    throw error;
  }
}

export async function addToPortfolio(
  symbol: string,
  quantity: number,
  avgPrice: number,
  buyDate: string,
  notes?: string
): Promise<PortfolioHolding> {
  try {
    const response = await axios.post(`${API_BASE_URL}/api/portfolio`, {
      symbol,
      quantity,
      avg_price: avgPrice,
      buy_date: buyDate,
      notes,
    });
    return response.data;
  } catch (error) {
    console.error("Error adding to portfolio:", error);
    throw error;
  }
}

export async function updatePortfolioHolding(
  id: number,
  updates: {
    quantity?: number;
    avg_price?: number;
    buy_date?: string;
    notes?: string;
  }
): Promise<PortfolioHolding> {
  try {
    const response = await axios.put(
      `${API_BASE_URL}/api/portfolio/${id}`,
      updates
    );
    return response.data;
  } catch (error) {
    console.error("Error updating portfolio holding:", error);
    throw error;
  }
}

export async function removeFromPortfolio(id: number): Promise<void> {
  try {
    await axios.delete(`${API_BASE_URL}/api/portfolio/${id}`);
  } catch (error) {
    console.error("Error removing from portfolio:", error);
    throw error;
  }
}

// ==================== TRANSACTIONS API ====================

export async function fetchTransactions(
  symbol?: string,
  limit: number = 50
): Promise<Transaction[]> {
  try {
    const params: any = { limit };
    if (symbol) params.symbol = symbol;

    const response = await axios.get(`${API_BASE_URL}/api/transactions`, {
      params,
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching transactions:", error);
    throw error;
  }
}

// ==================== LEGACY ====================

export async function fetchLatestPrice(symbol: string): Promise<number | null> {
  try {
    const response = await axios.get(
      `${API_BASE_URL}/api/company-price-volume-history`,
      {
        params: { symbol },
      }
    );
    const data = response.data;
    const content = Array.isArray(data.content) ? data.content : [];
    if (content.length > 0) {
      // Assume most recent is first
      const latest = content[0];
      return (
        latest.closePrice ||
        latest.close ||
        latest.closingPrice ||
        latest.price ||
        null
      );
    }
    return null;
  } catch (error) {
    console.error("Error fetching latest price for", symbol, error);
    return null;
  }
}
