import axios from "axios";

export async function fetchLatestPrice(symbol: string): Promise<number | null> {
  try {
    const response = await axios.get("/api/company-price-volume-history", {
      params: { symbol },
    });
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
