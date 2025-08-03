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
  const searchParams = useSearchParams(); // 🟢 Fix #2: use this with `useSearchParams`
  const id = searchParams.get("id");
  const currentPage = Number(searchParams.get("page")) || 1;

  const { user, verify, logout, loading, setLoading } = useAuth();

  const [accounts, setAccounts] = useState<any>(null);
  const [account, setAccount] = useState<any>(null);

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

      const Bank_ID = (id as string) || accounts.accounts[0]?.shareableId || "";

      console.log(`Fetching account for Bank_ID: ${Bank_ID}`);
      const accountRes = await getAccount(Bank_ID);
      setAccount(accountRes);
    };

    fetchAccount();
  }, [id, accounts]);

  const Bank_ID = id || accounts?.accounts?.[0]?.bankId || "";
  const accountsData = accounts?.accounts;

  const shareableId = (id as string) || accountsData?.[0]?.shareableId;
  // console.log(`shareableId => ${shareableId}`);
  // console.log(`accountsData => ${accountsData}`);

  // console.log(`Bank_ID->${Bank_ID}`);

  // || !account
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
            accounts={accounts?.accounts}
            totalBanks={accounts?.totalBanks}
            totalCurrentBalance={accounts?.totalCurrentBalance}
          />
        </header>
        <RecentTransactions
          accounts={accountsData}
          transactions={account?.transactions}
          shareableId={shareableId}
          page={currentPage}
        />
      </div>

      <RightSidebar
        user={user}
        transactions={account?.transactions}
        // transactions={[]}
        banks={[{ currentBalance: 123.5 }, { currentBalance: 123.5 }]}
      />
      {/* <RightSidebar 
        user={user}
        transactions={account?.transactions}
        banks={accountsData?.slice(0, 2)}
      /> */}
    </section>
  );
};

export default Home;
