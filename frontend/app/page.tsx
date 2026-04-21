import Link from "next/link";
import { headers } from "next/headers";
import { redirect } from "next/navigation";
import { auth } from "@/lib/auth";
import styles from "./page.module.css";

export default async function Home() {
  // Check if user is authenticated
  const session = await auth.api.getSession({
    headers: await headers(),
  });

  // If authenticated, redirect to dashboard
  if (session) {
    redirect("/dashboard");
  }

  return (
    <div className={styles.page}>
      <main className={styles.main}>
        <h1 className={styles.title}>Todo App</h1>
        <p className={styles.subtitle}>
          Organize your tasks, boost your productivity. A full-stack web
          application built with Next.js, FastAPI, and PostgreSQL.
        </p>
        <div className={styles.actions}>
          <Link href="/signup" className={styles.primaryButton}>
            Get Started
          </Link>
          <Link href="/signin" className={styles.secondaryButton}>
            Sign In
          </Link>
        </div>
      </main>
    </div>
  );
}
