import React from "react";
import Link from "next/link";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { BankTabItem } from "./BankTabItem";
import BankInfo from "./BankInfo";
import TransactionsTable from "./TransactionsTable";
import { Pagination } from "./Pagination";

const RecentTransactions = ({
  accounts,
  transactions = [],
  shareable_id,
  page = 1,
}: recent_transactions_props) => {
  //   TODO: refine this
  const rowsPerPage = 10;
  const totalPages = Math.ceil(transactions.length / rowsPerPage);

  const indexOfLastTransaction = page * rowsPerPage;
  const indexOfFirstTransaction = indexOfLastTransaction - rowsPerPage;

  const currentTransactions = transactions.slice(
    indexOfFirstTransaction,
    indexOfLastTransaction
  );

  return (
    <section className="recent-transactions">
      <header className="flex items-center justify-between">
        <h2 className="recent-transactions-label">Recent transactions</h2>
        <Link
          href={`/transaction-history/?id=${shareable_id}`}
          className="view-all-btn"
        >
          View all
        </Link>
      </header>
      <Tabs defaultValue={shareable_id} className="w-full">
        <TabsList className="recent-transactions-tablist">
          {accounts.map((account: AccountData) => (
            // TODO Bank_ID:
            <TabsTrigger key={account.id} value={account.shareable_id}>
              <BankTabItem
                key={account.id}
                account={account}
                shareable_id={shareable_id}
              />
            </TabsTrigger>
          ))}
        </TabsList>

        {accounts.map((account: AccountData) => (
          <TabsContent
            value={account.shareable_id}
            key={account.id}
            className="space-y-4"
          >
            <BankInfo
              account={account}
              shareable_id={account.shareable_id}
              type="full"
            />

            <TransactionsTable transactions={currentTransactions} />

            {totalPages > 1 && (
              <div className="my-4 w-full">
                <Pagination total_pages={totalPages} page={page} />
              </div>
            )}
          </TabsContent>
        ))}
      </Tabs>
    </section>
  );
};

export default RecentTransactions;
