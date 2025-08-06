"use client";

import Image from "next/image";
import { useSearchParams, useRouter } from "next/navigation";

import {
  cn,
  form_url_query,
  format_amount,
  get_account_type_colors,
} from "@/lib/utils";

const BankInfo = ({ account, shareable_id, type }: bank_info_props) => {
  const router = useRouter();
  const searchParams = useSearchParams();

  const isActive = shareable_id === account?.shareable_id;

  const handleBankChange = () => {
    const newUrl = form_url_query({
      params: searchParams.toString(),
      key: "id",
      value: account?.shareable_id,
    });
    router.push(newUrl, { scroll: false });
  };

  const colors = get_account_type_colors(account?.type as account_types);

  return (
    <div
      onClick={handleBankChange}
      className={cn(`bank-info ${colors.bg}`, {
        "shadow-sm border-blue-700": type === "card" && isActive,
        "rounded-xl": type === "card",
        "hover:shadow-sm cursor-pointer": type === "card",
      })}
    >
      <figure
        className={`flex-center h-fit rounded-full bg-blue-100 ${colors.light_bg}`}
      >
        <Image
          src="/icons/connect-bank.svg"
          width={20}
          height={20}
          alt={account.subtype}
          className="m-2 min-w-5"
        />
      </figure>
      <div className="flex w-full flex-1 flex-col justify-center gap-1">
        <div className="bank-info_content">
          <h2
            className={`text-16 line-clamp-1 flex-1 font-bold text-blue-900 ${colors.title}`}
          >
            {account.name}
          </h2>
          {type === "full" && (
            <p
              className={`text-12 rounded-full px-3 py-1 font-medium text-blue-700 ${colors.sub_text} ${colors.light_bg}`}
            >
              {account.subtype}
            </p>
          )}
        </div>

        <p className={`text-16 font-medium text-blue-700 ${colors.sub_text}`}>
          {format_amount(account.current_balance)}
        </p>
      </div>
    </div>
  );
};

export default BankInfo;
