from pathlib import Path
import pandas as pd
import sqlite3


def load_csv_to_sqlite(csv_path: str, table_name: str = "portfolio_metrics", db_path: str = "data/sql/enterprise_agent.db"):
    csv_path = Path(csv_path)
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(csv_path)
    conn = sqlite3.connect(db_path)
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.close()
    return str(db_path)


def run_sql_query(query: str, db_path: str = "data/sql/enterprise_agent.db") -> pd.DataFrame:
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


def safe_sql_agent(question: str, db_path: str = "data/sql/enterprise_agent.db"):
    q = question.lower()

    if "highest" in q or "priority" in q or "top" in q:
        sql = """
        SELECT project, domain, primary_skill, risk_level, portfolio_priority
        FROM portfolio_metrics
        ORDER BY portfolio_priority DESC, project ASC
        LIMIT 10
        """
    elif "healthcare" in q:
        sql = """
        SELECT project, domain, primary_skill, risk_level, portfolio_priority
        FROM portfolio_metrics
        WHERE LOWER(domain) LIKE '%healthcare%'
        """
    elif "risk" in q:
        sql = """
        SELECT risk_level, COUNT(*) AS project_count
        FROM portfolio_metrics
        GROUP BY risk_level
        ORDER BY project_count DESC
        """
    else:
        sql = """
        SELECT project, domain, primary_skill, risk_level, portfolio_priority
        FROM portfolio_metrics
        """

    return sql, run_sql_query(sql, db_path)
