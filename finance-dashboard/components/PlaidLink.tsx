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
            Connect Bank
          </Button>
        ) : (
          <Button
            onClick={() => open()}
            disabled={!ready}
            className="plaidlink-default"
          >
            Connect Bank
          </Button>
        )}
      </>
    </div>
  );
};
