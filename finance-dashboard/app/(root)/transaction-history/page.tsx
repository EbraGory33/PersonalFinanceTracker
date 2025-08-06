"use client";
import HeaderBox from "@/components/HeaderBox";
import { Pagination } from "@/components/Pagination";
import TransactionsTable from "@/components/TransactionsTable";
import { getAccount, getAccounts } from "@/lib/actions/bank.actions";
import { useAuth } from "@/lib/hooks/useAuth";
import { useRouter, useSearchParams } from "next/navigation";

import React, { useEffect, useState } from "react";
import { format_amount } from "@/lib/utils";

const TransactionHistory = () => {
  const router = useRouter();
  const searchParams = useSearchParams();
  const id = searchParams.get("id");
  const currentPage = Number(searchParams.get("page")) || 1;

  const { verify, logout, loading, setLoading } = useAuth();

  // const [accounts, setAccounts] = useState<any>(null);
  // const [account, setAccount] = useState<any>(null);
  const [accounts, setAccounts] = useState<accounts_response>();
  const [account, setAccount] = useState<account>();

  const rowsPerPage = 10;
  const totalPages = Math.ceil(
    (account?.transactions?.length ?? 0) / rowsPerPage
  );

  const indexOfLastTransaction = currentPage * rowsPerPage;
  const indexOfFirstTransaction = indexOfLastTransaction - rowsPerPage;

  const currentTransactions = account?.transactions.slice(
    indexOfFirstTransaction,
    indexOfLastTransaction
  );

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);

        // Auth check
        await verify();

        // Accounts data
        const accountsRes = await getAccounts();
        setAccounts(accountsRes);

        // const Bank_ID =
        //   (id as string) || accountsRes?.accounts?.[0]?.shareableId || "";
        // console.log(`const Bank_ID = ${Bank_ID}`);
        // const accountRes = await getAccount(Bank_ID);
        // setAccount(accountRes);

        setLoading(false);
      } catch (err) {
        console.error("Error during authentication or data fetching:", err);
        await logout();
        router.push("/sign-in");
      }
    };

    fetchData();
  }, []);

  useEffect(() => {
    const fetchAccount = async () => {
      if (!accounts?.accounts?.length) return;

      const Bank_ID =
        (id as string) || accounts.accounts[0]?.shareable_id || "";

      console.log(`Fetching account for Bank_ID: ${Bank_ID}`);
      const accountRes = await getAccount(Bank_ID);
      setAccount(accountRes);
    };

    fetchAccount();
  }, [id, accounts]);

  // || !account
  if (loading || !accounts || !account) {
    return (
      <section className="home">
        <div className="home-content">loading</div>
      </section>
    );
  }

  return (
    <div className="transactions">
      <div className="transactions-header">
        <HeaderBox
          title="Transaction History"
          subtext="See your bank details and transactions."
        />
      </div>

      <div className="space-y-6">
        <div className="transactions-account">
          <div className="flex flex-col gap-2">
            <h2 className="text-18 font-bold text-white">
              {account?.data.name}
            </h2>
            <p className="text-14 text-blue-25">{account?.data.officialName}</p>
            <p className="text-14 font-semibold tracking-[1.1px] text-white">
              ●●●● ●●●● ●●●● {account?.data.mask}
            </p>
          </div>

          <div className="transactions-account-balance">
            <p className="text-14">
              Current balance{typeof account?.data.current_balance}
            </p>
            <p className="text-24 text-center font-bold">
              {format_amount(account?.data.current_balance)}
            </p>
          </div>
        </div>

        <section className="flex w-full flex-col gap-6">
          <TransactionsTable transactions={currentTransactions || []} />
          {totalPages > 1 && (
            <div className="my-4 w-full">
              <Pagination total_pages={totalPages} page={currentPage} />
            </div>
          )}
        </section>
      </div>
    </div>
  );
};

export default TransactionHistory;
