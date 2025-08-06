"use client";

import React from "react";
import { useSearchParams, useRouter } from "next/navigation";
import { cn, form_url_query } from "@/lib/utils";

export const BankTabItem = ({ account, shareable_id }: bank_tab_item_props) => {
  const searchParams = useSearchParams();
  const router = useRouter();
  const isActive = shareable_id === account?.shareable_id;

  const handleBankChange = () => {
    const newUrl = form_url_query({
      params: searchParams.toString(),
      key: "id",
      value: account?.shareable_id,
    });
    router.push(newUrl, { scroll: false });
  };

  return (
    <div
      onClick={handleBankChange}
      className={cn(`banktab-item`, {
        " border-blue-600": isActive,
      })}
    >
      <p
        className={cn(`text-16 line-clamp-1 flex-1 font-medium text-gray-500`, {
          " text-blue-600": isActive,
        })}
      >
        {account.name}
      </p>
    </div>
  );
};
