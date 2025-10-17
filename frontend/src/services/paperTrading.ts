import axios from "axios";

// All routes are proxied to the backend at /api
const API_BASE_URL = "/api";

export interface PaperPortfolioHolding {
  id: number;
  user_id: number;
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

export interface PaperPortfolioSummary {
  total_invested: number;
  current_value: number;
  total_pnl: number;
  total_pnl_percent: number;
  day_pnl: number;
  day_pnl_percent: number;
  total_holdings: number;
  cash_available: number;
  apy_annualized?: number;
  apy_since?: string | null;
}

export interface PaperAccount {
  user_id: number;
  initial_capital: number;
  cash_balance: number;
  created_at: string;
  updated_at?: string | null;
  funded_at?: string | null;
}

export interface PaperTradeResponse {
  message: string;
  symbol: string;
  side: "buy" | "sell";
  quantity: number;
  execution_price: number;
  cash_balance: number;
}

export async function fetchPaperPortfolio(): Promise<PaperPortfolioHolding[]> {
  try {
    const response = await axios.get(`${API_BASE_URL}/paper-trading/portfolio`);
    return response.data;
  } catch (error) {
    console.error("Error fetching paper portfolio:", error);
    throw error;
  }
}

export async function fetchPaperPortfolioSummary(): Promise<PaperPortfolioSummary> {
  try {
    const response = await axios.get(
      `${API_BASE_URL}/paper-trading/portfolio/summary`
    );
    return response.data;
  } catch (error) {
    console.error("Error fetching paper portfolio summary:", error);
    throw error;
  }
}

export async function fetchPaperAccount(): Promise<PaperAccount> {
  try {
    const response = await axios.get(`${API_BASE_URL}/paper-trading/account`);
    return response.data;
  } catch (error) {
    console.error("Error fetching paper account:", error);
    throw error;
  }
}

export async function initPaperAccount(
  initialCapital: number
): Promise<PaperAccount> {
  try {
    const response = await axios.post(
      `${API_BASE_URL}/paper-trading/account/init`,
      {
        initial_capital: initialCapital,
      }
    );
    return response.data;
  } catch (error) {
    console.error("Error initializing paper account:", error);
    throw error;
  }
}

export async function placePaperTrade(
  symbol: string,
  quantity: number,
  side: "buy" | "sell",
  notes?: string
): Promise<PaperTradeResponse> {
  try {
    const response = await axios.post(`${API_BASE_URL}/paper-trading/trade`, {
      symbol,
      quantity,
      side,
      notes,
    });
    return response.data;
  } catch (error) {
    console.error("Error placing paper trade:", error);
    throw error;
  }
}

export async function addToPaperPortfolio(
  symbol: string,
  quantity: number,
  avgPrice: number,
  buyDate: string,
  notes?: string
): Promise<PaperPortfolioHolding> {
  try {
    const response = await axios.post(
      `${API_BASE_URL}/paper-trading/portfolio`,
      {
        symbol,
        quantity,
        avg_price: avgPrice,
        buy_date: buyDate,
        notes,
      }
    );
    return response.data;
  } catch (error) {
    console.error("Error adding to paper portfolio:", error);
    throw error;
  }
}

export async function updatePaperPortfolioHolding(
  id: number,
  updates: {
    quantity?: number;
    avg_price?: number;
    buy_date?: string;
    notes?: string;
  }
): Promise<PaperPortfolioHolding> {
  try {
    const response = await axios.put(
      `${API_BASE_URL}/paper-trading/portfolio/${id}`,
      updates
    );
    return response.data;
  } catch (error) {
    console.error("Error updating paper portfolio holding:", error);
    throw error;
  }
}

export async function removeFromPaperPortfolio(id: number): Promise<void> {
  try {
    await axios.delete(`${API_BASE_URL}/paper-trading/portfolio/${id}`);
  } catch (error) {
    console.error("Error removing from paper portfolio:", error);
    throw error;
  }
}
