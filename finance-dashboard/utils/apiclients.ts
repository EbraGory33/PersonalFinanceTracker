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
  data?: Record<string, unknown>,
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
  } catch (error: unknown) {
    if (
      typeof error === "object" &&
      error !== null &&
      "response" in error &&
      typeof (error as any).response === "object" &&
      (error as any).response !== null &&
      "data" in (error as any).response
    ) {
      const err = error as { response: { data: { error?: string } } };
      throw new Error(err.response.data.error || "API request failed");
    } else if (error instanceof Error) {
      throw new Error(error.message || "API request failed");
    } else {
      throw new Error("API request failed");
    }
  }
}

//   } catch (error: any) {
//     if (
//       typeof error === "object" &&
//       error !== null &&
//       "response" in error &&
//       typeof (error as any).response === "object" &&
//       (error as any).response !== null &&
//       "data" in (error as any).response
//     ) {
//       const err = error as { response: { data: { error?: string } } };
//       throw new Error(err.response.data.error || "API request failed");
//     } else if (error instanceof Error) {
//       throw new Error(error.message || "API request failed");
//     } else {
//       throw new Error("API request failed");
//     }
// }
