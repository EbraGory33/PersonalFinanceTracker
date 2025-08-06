"use client";

import HeaderBox from "@/components/HeaderBox";
import RecentTransactions from "@/components/RecentTransactions";
import RightSidebar from "@/components/RightSidebar";
import TotalBalanceBox from "@/components/TotalBalanceBox";
import { getAccount, getAccounts } from "@/lib/actions/bank.actions";
import { useAuth } from "@/lib/hooks/useAuth";
import { useRouter, useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";

const Home = () => {
  const router = useRouter();
  const search_params = useSearchParams();
  const id = search_params.get("id");
  const current_page = Number(search_params.get("page")) || 1;

  const { user, verify, logout, loading, setLoading } = useAuth();

  const [accounts, set_accounts] = useState<accounts_response>();
  const [account, set_account] = useState<account>();

  useEffect(() => {
    const fetch_data = async () => {
      try {
        setLoading(true);

        // Auth check
        await verify();

        // Accounts data
        const accounts_res = await getAccounts();
        set_accounts(accounts_res);

        setLoading(false);
      } catch (err) {
        console.error("Error during authentication or data fetching:", err);
        await logout();
        router.push("/sign-in");
      }
    };

    fetch_data();
  }, []);

  useEffect(() => {
    const fetch_account = async () => {
      if (!accounts?.accounts?.length) return;

      const bank_id =
        (id as string) || accounts.accounts[0]?.shareable_id || "";

      console.log(`Fetching account for bank_id: ${bank_id}`);
      const account_res = await getAccount(bank_id);
      set_account(account_res);
    };

    fetch_account();
  }, [id, accounts]);

  const accounts_data = accounts?.accounts;

  const shareable_id = (id as string) || accounts_data?.[0]?.shareable_id;
  console.log(`shareable_id => ${shareable_id}`);
  console.log(`accounts_data => ${accounts_data}`);

  if (loading || !accounts) {
    return (
      <section className="home">
        <div className="home-content">loading</div>
      </section>
    );
  }

  return (
    <section className="home">
      <div className="home-content">
        <header className="home-header">
          <HeaderBox
            type="greeting"
            title="Welcome"
            user={user?.first_name || "Guest"}
            subtext="Access and manage your account and transactions efficiently."
          />

          <TotalBalanceBox
            accounts={accounts_data || []}
            total_banks={accounts?.total_banks}
            total_current_balance={accounts?.total_current_balance}
          />
        </header>

        <RecentTransactions
          accounts={accounts_data || []}
          transactions={account?.transactions || []}
          shareable_id={shareable_id || ""}
          page={current_page}
        />
      </div>

      <RightSidebar
        user={user || []}
        transactions={account?.transactions || []}
        banks={accounts_data?.slice(0, 2) || []}
      />
    </section>
  );
};

export default Home;
