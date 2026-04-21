import { headers } from "next/headers";
import { auth } from "@/lib/auth";
import SignOutButton from "@/components/SignOutButton";
import styles from "./page.module.css";

export default async function HomePage() {
  const session = await auth.api.getSession({
    headers: await headers(),
  });

  return (
    <div className={styles.page}>
      <header className={styles.header}>
        <h1 className={styles.logo}>Todo App</h1>
        <div className={styles.userInfo}>
          <span className={styles.userName}>{session?.user?.name || session?.user?.email}</span>
          <SignOutButton />
        </div>
      </header>
      <main className={styles.main}>
        <h2 className={styles.title}>Welcome, {session?.user?.name || "User"}!</h2>
        <p className={styles.subtitle}>
          Your tasks will appear here. Start by adding your first task.
        </p>
      </main>
    </div>
  );
}
