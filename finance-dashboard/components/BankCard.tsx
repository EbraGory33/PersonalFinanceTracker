import { format_amount } from "@/lib/utils";
import Image from "next/image";
import Link from "next/link";
import React from "react";
import Copy from "./Copy";

const BankCard = ({
  account,
  user_name,
  show_balance = true,
}: credit_card_props) => {
  return (
    <div className="flex flex-col">
      <Link
        href={`/transaction-history/?id=${account.shareable_id}`}
        className="bank-card"
      >
        <div className="bank-card_content">
          <div>
            <h1 className="text-16 font-semibold text-white">
              {account.name || user_name}
            </h1>
            <p className="font-ibm-plex-serif font-black text-white">
              {format_amount(account.current_balance)}
            </p>
          </div>
          <article className="font-ibm-plex-serif flex flex-col gap-2">
            <div className="flex justify-between">
              <h1 className="text-12 font-semibold text-white">{user_name}</h1>
              <h2 className="text-12 font-semibold text-white">●● / ●●</h2>
            </div>
            <p className="text-14 font-semibold tracking-[1.1px] text-white">
              ●●●● ●●●● ●●●●{" "}
              <span className="text-14">{account.mask || 1234}</span>
            </p>
          </article>
        </div>

        <div className="bank-card_icon">
          <Image src="/icons/paypass.svg" height={20} width={20} alt="pay" />
          <Image
            src="/icons/mastercard.svg"
            width={45}
            height={32}
            alt="mastercard"
            className="ml-5"
          />
        </div>
        <Image
          src="/icons/lines.png"
          width={316}
          height={190}
          alt="line"
          className="absolute top-0 left-0"
        />
      </Link>

      {show_balance && <Copy title={account?.shareable_id} />}
    </div>
  );
};

export default BankCard;
