import api from "./marketData_enhanced";

export interface AgentDetail {
  score: number;
  summary: string;
}

export interface AgentAnalysisResponse {
  stock_symbol: string;
  analysis: string;
  overall_score: number;
  agent_details: {
    technical_analysis: AgentDetail;
    fundamental_analysis: AgentDetail;
    macro_news_analysis: AgentDetail;
  };
  timestamp: string;
  processing_time_ms: number;
}

export interface StructuredResponse {
  quick_answer: string;
  key_insights: string[];
  recommendation: string;
  risk_factors: string;
  stock_metrics: Record<
    string,
    {
      overall_score: number;
      technical_score: number;
      fundamental_score: number;
      macro_score: number;
      recommendation: string;
    }
  >;
}

export interface AgentQuestionResponse {
  question: string;
  answer: string;
  structured_response: StructuredResponse | null;
  related_stocks: string[];
  confidence: string;
  timestamp: string;
  processing_time_ms: number;
}

export interface AgentStockListResponse {
  available_stocks: string[];
}

export const fetchAgentStocks = async (): Promise<string[]> => {
  try {
    const { data } = await api.get<AgentStockListResponse>("/agent/stocks");
    return data.available_stocks || [];
  } catch (error) {
    console.error("Error fetching agent stocks:", error);
    return [];
  }
};

export const analyzeAgentStock = async (
  stockSymbol: string
): Promise<AgentAnalysisResponse> => {
  const payload = { stock_symbol: stockSymbol };

  try {
    const { data } = await api.post<AgentAnalysisResponse>(
      "/agent/analyze",
      payload
    );
    return data;
  } catch (error: any) {
    console.error("Error analyzing stock via agent:", error);
    if (error?.response?.data?.detail) {
      throw new Error(error.response.data.detail);
    }
    throw new Error("Failed to analyze stock. Please try again later.");
  }
};

export const askAgentQuestion = async (
  question: string
): Promise<AgentQuestionResponse> => {
  const payload = { question };

  try {
    const { data } = await api.post<AgentQuestionResponse>(
      "/agent/ask",
      payload
    );
    return data;
  } catch (error: any) {
    console.error("Error asking agent question:", error);
    if (error?.response?.data?.detail) {
      throw new Error(error.response.data.detail);
    }
    throw new Error("Failed to ask question. Please try again later.");
  }
};
