"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { signOut } from "@/lib/auth-client";
import styles from "./SignOutButton.module.css";

export default function SignOutButton() {
  const [isLoading, setIsLoading] = useState(false);
  const router = useRouter();

  const handleSignOut = async () => {
    setIsLoading(true);

    try {
      await signOut();
      router.push("/signin");
    } catch {
      // Even on error, redirect to signin
      router.push("/signin");
    }
  };

  return (
    <button
      onClick={handleSignOut}
      disabled={isLoading}
      className={styles.button}
      aria-label="Sign out"
    >
      {isLoading ? "Signing out..." : "Sign Out"}
    </button>
  );
}
