"use client";

import MobileNav from "@/components/MobileNav";
import Sidebar from "@/components/Sidebar";
import Image from "next/image";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/hooks/useAuth";
import { useEffect } from "react";

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const { user, verify, loading, logout, setLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (user) {
      setLoading(false);
    }
  }, [user]);

  useEffect(() => {
    authenticated();
  }, []);

  const authenticated = async () => {
    try {
      setLoading(true);
      try {
        const userdata = await verify();
        console.log("userdata:", userdata);
        console.log("user:", user);
        //alert(`User data: ${JSON.stringify(userdata)}`);
      } catch (error) {
        console.error("Error during User authentication:", error);
        await logout();
        // Redirect to sign-in
        router.push("/sign-in");
      } finally {
        setLoading(false);
      }

      setLoading(false);
    } catch (error) {
      console.error("Error during authentication:", error);
      alert("Authentication failed. Check console for details.");
    }
  };

  async function handleLogout() {
    await logout();
  }

  if (loading) {
    return (
      <main className="flex h-screen items-center justify-center">
        <p>Loading...</p>
      </main>
    );
  }

  if (!user && !loading) {
    // Redirect to sign-in if not authenticated
    handleLogout();
    router.push("/sign-in");
    return null; // Avoid rendering UI
  }

  return (
    <main className="flex h-screen w-full font-inter">
      {user ? <Sidebar user={user} /> : <></>}
      <div className="flex size-full flex-col">
        <div className="root-layout">
          <Image src="/icons/logo.svg" width={30} height={30} alt="logo" />
          <div>
            <MobileNav user={user} />
          </div>
        </div>
        {children}
      </div>
    </main>
  );
}
