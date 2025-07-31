import { apiFetch } from "@/utils/apiclients";
import { revalidateHome } from "./revalidate";

export const verify = async () => {
  try {
    const user = await apiFetch("auth/authenticate");
    return user;
  } catch (error) {
    console.error("Error", error);
  }
};

export const signIn = async ({ email, password }: signInProps) => {
  try {
    const user = await apiFetch("auth/signin", { email, password }, "POST");
    return user;
  } catch (error) {
    console.error("Error", error);
  }
};

export const signUp = async (params: SignUpParams) => {
  try {
    const user = await apiFetch("auth/signup", params, "POST");
    return user;
  } catch (error) {
    console.error("Error", error);
  }
};

export const createLinkToken = async () => {
  try {
    const res = await apiFetch("auth/plaid/create_link_token", [], "POST");
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
      "auth/plaid/exchange_public_token",
      [publicToken],
      "POST"
    );
    revalidateHome();
  } catch (error) {
    console.error("An error occurred while creating exchanging token:", error);
  }
};
