import { apiFetch } from "@/utils/apiclients";
import { parse_stringify } from "../utils";

export const createTransfer = async ({
  source_funding_source_url,
  destination_funding_source_url,
  amount,
}: transfer_params) => {
  console.log("creating Transfer");
  const res = await apiFetch(
    "transaction/createTransfer",
    {
      source_funding_source_url,
      destination_funding_source_url,
      amount,
    },
    "POST"
  );
  console.log(`creating Transfer res : ${res}`);
  return res;
};

export const createTransaction = async (
  transaction: create_transaction_props
) => {
  try {
    const enrichedTransaction = {
      ...transaction,
      channel: "online",
      category: "TRANSFER",
    };
    const res = await apiFetch(
      "transaction/createTransaction",
      enrichedTransaction,
      "POST"
    );
    console.log("Link token response:", res);
    return parse_stringify(res);
  } catch (error) {
    console.error("Failed to create transaction:", error);
    return console.log(error);
  }
};
