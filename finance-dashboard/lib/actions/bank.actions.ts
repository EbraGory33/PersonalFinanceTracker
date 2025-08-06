import { apiFetch } from "@/utils/apiclients";
import { revalidateHome } from "./revalidate";

export const createLinkToken = async () => {
  try {
    const res = await apiFetch("bank/plaid/create_link_token", {}, "POST");
    console.log("Link token response:", res);
    return res;
  } catch (error) {
    console.error("Failed to create link token:", error);
    return null;
  }
};

export const exchangePublicToken = async ({
  public_token,
}: exchange_public_token_props) => {
  try {
    await apiFetch(
      "bank/plaid/exchange_public_token",
      { public_token: public_token },
      "POST"
    );
    revalidateHome();
  } catch (error) {
    console.error("An error occurred while creating exchanging token:", error);
  }
};

export const getAccounts = async () => {
  try {
    const res = await apiFetch("bank/getAccounts", {}, "GET");
    return res;
  } catch (error) {
    console.error("Failed to create link token:", error);
    return null;
  }
};
export const getAccount = async (bankId: string) => {
  try {
    const res = await apiFetch(
      "bank/getAccount",
      { shareableId: bankId },
      "GET"
    );
    return res;
  } catch (error) {
    console.error("Failed to create link token:", error);
    return null;
  }
};

export const getBankingInfo = async () => {
  try {
    const res = await apiFetch("bank/userBanks", {}, "GET");
    return res.data;
  } catch (error) {
    console.error("Failed to fetch bank by account id:", error);
    return null;
  }
};

export const getBankByAccountId = async (shareableId: string) => {
  try {
    console.log(`shareableId request => ${shareableId}`);
    const res = await apiFetch(
      "bank/getBank",
      { shareableId: shareableId },
      "GET"
    );
    console.log(`getBankByAccountId-res request => ${res}`);
    console.log(`getBankByAccountId-res.data request => ${res.data}`);
    return res;
  } catch (error) {
    console.error("Failed to fetch bank by account id:", error);
    return null;
  }
};
