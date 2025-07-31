"use client";

import { useState } from "react";
import { apiFetch } from "@/utils/apiclients";

export const useAuth = () => {
  const [user, setUser] = useState<User>();
  const [loading, setLoading] = useState(true);
  const verify = async () => {
    try {
      const userData = await apiFetch("auth/authenticate");
      setUser(userData);
      return userData;
    } catch (error) {
      console.error("Error verifying user", error);
    } finally {
      setLoading(false);
    }
  };

  const signIn = async ({ email, password }: signInProps) => {
    try {
      const userData = await apiFetch(
        "auth/signin",
        { email, password },
        "POST"
      );
      setUser(userData);
      return userData;
    } catch (error) {
      console.error("Error signing in", error);
    }
  };

  const signUp = async (params: SignUpParams) => {
    try {
      const userData = await apiFetch("auth/signup", params, "POST");
      setUser(userData);
      return userData;
    } catch (error) {
      console.error("Error signing up", error);
    }
  };

  const logout = async () => {
    try {
      await apiFetch("auth/logout", {}, "POST");
    } catch (error) {
      console.error("Error logging out", error);
    }
  };

  return { user, loading, setLoading, verify, signIn, signUp, logout };
};
