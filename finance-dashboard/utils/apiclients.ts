import axios from "axios";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

type HttpMethod = "GET" | "POST" | "PUT" | "PATCH" | "DELETE";

const apiClient = axios.create({
  baseURL: API_URL,
  withCredentials: true,
  headers: {
    "Content-Type": "application/json",
  },
});

export async function apiFetch(
  path: string,
  data?: Record<string, any>,
  method: HttpMethod = "GET"
) {
  try {
    const config = {
      url: path,
      method,
      data: ["POST", "PUT", "PATCH", "DELETE"].includes(method)
        ? data
        : undefined,
      params: method === "GET" ? data : undefined, // for GET, treat data as query params
    };

    const response = await apiClient(config);
    return response.data;
  } catch (error: any) {
    if (error.response && error.response.data) {
      throw new Error(error.response.data.detail || "API request failed");
    } else {
      throw new Error(error.message || "API request failed");
    }
  }
}
