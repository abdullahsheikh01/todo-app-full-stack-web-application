import styles from "./page.module.css";

export default function Home() {
  return (
    <div className={styles.page}>
      <main className={styles.main}>
        <h1 className={styles.title}>Todo App - Phase II</h1>
        <p className={styles.subtitle}>
          Full-stack web application with Next.js frontend and FastAPI backend,
          connected to Neon PostgreSQL.
        </p>
      </main>
    </div>
  );
}
