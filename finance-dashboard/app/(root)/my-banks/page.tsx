"use client";
import BankCard from "@/components/BankCard";
import HeaderBox from "@/components/HeaderBox";
import { useAuth } from "@/lib/hooks/useAuth";
import { getAccounts } from "@/lib/actions/bank.actions";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import React from "react";

const MyBanks = () => {
  const router = useRouter();
  const { user, verify, logout, loading, setLoading } = useAuth();
  const [accounts, setAccounts] = useState<accounts_response>();

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);

        // Auth check
        await verify();

        // Accounts data
        const accounts_res = await getAccounts();
        setAccounts(accounts_res);

        setLoading(false);
      } catch (err) {
        console.error("Error during authentication or data fetching:", err);
        await logout();
        router.push("/sign-in");
      }
    };

    fetchData();
  }, []);

  if (loading || !user || !accounts) {
    return (
      <section className="home">
        <div className="home-content">loading</div>
      </section>
    );
  }
  return (
    <section className="flex">
      <div className="my-banks">
        <HeaderBox
          title="My Bank Accounts"
          subtext="Effortlessly manage your banking activites."
        />

        <div className="space-y-4">
          <h2 className="header-2">Your cards</h2>
          <div className="flex flex-wrap gap-6">
            {accounts &&
              accounts.accounts.map((a: AccountData) => (
                <BankCard
                  key={a.shareable_id}
                  account={a}
                  user_name={user?.first_name}
                />
              ))}
          </div>
        </div>
      </div>
    </section>
  );
};

export default MyBanks;
