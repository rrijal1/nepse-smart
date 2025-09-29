import axios from "axios";

export const fetchTopGainers = async () => {
  try {
    const response = await axios.get(`/api/top-gainers`);
    return response.data;
  } catch (error) {
    console.error("Error fetching top gainers:", error);
    return [];
  }
};

export const fetchTopLosers = async () => {
  try {
    const response = await axios.get(`/api/top-losers`);
    return response.data;
  } catch (error) {
    console.error("Error fetching top losers:", error);
    return [];
  }
};
