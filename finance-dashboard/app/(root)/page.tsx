"use client";
import HeaderBox from "@/components/HeaderBox";
import RightSidebar from "@/components/RightSidebar";
import TotalBalanceBox from "@/components/TotalBalanceBox";
import { useAuth } from "@/lib/hooks/useAuth";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

const Home = () => {
  const { user, verify, logout, loading } = useAuth();
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();
  //const [user, setUser] = useState<User>();
  const loggedIn = {
    first_name: "Ebrahim", // TODO: Remove this
    last_name: "Gory", // TODO: Remove this
    email: "eGory@gmail.com", // TODO: Remove this
  };

  useEffect(() => {
    if (user) {
      setIsLoading(false);
    }
  }, [user]);
  /*}
  
  useEffect(() => {
    authenticated();
  }, []);

  

  const authenticated = async () => {
    try {
      setIsLoading(true);
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
        setIsLoading(false);
      }

      setIsLoading(false);
    } catch (error) {
      console.error("Error during authentication:", error);
      alert("Authentication failed. Check console for details.");
    }
  };
  */
  if (loading) {
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
            accounts={[]}
            totalBanks={1}
            totalCurrentBalance={1250.35}
          />
        </header>
        RECENT TRANSACTIONS
      </div>

      <RightSidebar
        user={user}
        transactions={[]}
        banks={[{ currentBalance: 123.5 }, { currentBalance: 123.5 }]}
      />
    </section>
  );
};

export default Home;
