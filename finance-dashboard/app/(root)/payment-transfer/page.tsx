"use client";
import HeaderBox from "@/components/HeaderBox";
import PaymentTransferForm from "@/components/PaymentTransferForm";
import { getAccounts } from "@/lib/actions/bank.actions";
import { useAuth } from "@/lib/hooks/useAuth";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import React from "react";

const Transfer = () => {
  const router = useRouter();

  const { verify, logout, loading, setLoading } = useAuth();

  const [accounts, setAccounts] = useState<accounts_response>();

  const accounts_data = accounts?.accounts;

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);

        // Auth check
        await verify();

        // Accounts data
        const accounts_res = await getAccounts();
        setAccounts(accounts_res);

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

  if (loading || !accounts) {
    return (
      <section className="home">
        <div className="home-content">loading</div>
      </section>
    );
  }

  return (
    <section className="payment-transfer">
      <HeaderBox
        title="Payment Transfer"
        subtext="Please provide any specific details or notes related to the payment transfer"
      />

      <section className="size-full pt-5">
        <PaymentTransferForm accounts={accounts_data || []} />
      </section>
    </section>
  );
};

export default Transfer;
