import { apiFetch } from "@/utils/apiclients";
import { revalidateHome } from "./revalidate";

export const createLinkToken = async () => {
  try {
    const res = await apiFetch("bank/plaid/create_link_token", [], "POST");
    console.log("Link token response:", res);
    return res;
  } catch (error) {
    console.error("Failed to create link token:", error);
    return null;
  }
};

export const exchangePublicToken = async ({
  publicToken,
}: exchangePublicTokenProps) => {
  try {
    const res = await apiFetch(
      "bank/plaid/exchange_public_token",
      { public_token: publicToken },
      "POST"
    );
    revalidateHome();
  } catch (error) {
    console.error("An error occurred while creating exchanging token:", error);
  }
};
