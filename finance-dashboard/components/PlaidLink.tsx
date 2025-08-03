import React, { useCallback, useState, useEffect } from "react";
import { Button } from "./ui/button";
import {
  PlaidLinkOnSuccess,
  PlaidLinkOptions,
  usePlaidLink,
} from "react-plaid-link";
import { useRouter } from "next/navigation";
import {
  createLinkToken,
  exchangePublicToken,
} from "@/lib/actions/bank.actions";
import Image from "next/image";

export const PlaidLink = ({ user, variant }: PlaidLinkProps) => {
  const router = useRouter();
  const [token, setToken] = useState("");

  useEffect(() => {
    const getLinkToken = async () => {
      const data = await createLinkToken();
      setToken(data?.link_token);
    };
    getLinkToken();
  }, []);

  const onSuccess = useCallback<PlaidLinkOnSuccess>(
    async (public_token: string) => {
      console.log("Calling exchangePublicToken");
      await exchangePublicToken({
        publicToken: public_token,
      });

      router.push("/");
    },
    [user]
  );

  const config: PlaidLinkOptions = {
    token,
    onSuccess,
  };
  const { open, ready } = usePlaidLink(config);

  return (
    <div>
      <>
        {variant === "primary" ? (
          <Button
            onClick={() => open()}
            disabled={!ready}
            className="plaidlink-primary"
          >
            Connect Bank
          </Button>
        ) : variant === "ghost" ? (
          <Button
            onClick={() => open()}
            disabled={!ready}
            className="plaidlink-ghost"
          >
            <Image
              src="/icons/connect-bank.svg"
              alt="connect-bank"
              width={24}
              height={24}
            />
            <p className=" hidden xl:block text-[16px] font-semibold text-black-2">
              Connect Bank
            </p>
          </Button>
        ) : (
          <Button
            onClick={() => open()}
            disabled={!ready}
            className="plaidlink-default shadow-none"
          >
            <Image
              src="/icons/connect-bank.svg"
              alt="connect-bank"
              width={24}
              height={24}
            />
            <p className="text-[16px] font-semibold text-black-2">
              Connect Bank
            </p>
          </Button>
        )}
      </>
    </div>
  );
};
