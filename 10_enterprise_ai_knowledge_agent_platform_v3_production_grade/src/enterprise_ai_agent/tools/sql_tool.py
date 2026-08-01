from __future__ import annotations
import sqlite3
from pathlib import Path
import pandas as pd

TEMPLATES={
 "top_priority":"SELECT project, domain, primary_skill, risk_level, portfolio_priority FROM portfolio_metrics ORDER BY portfolio_priority DESC, project ASC LIMIT 10",
 "healthcare":"SELECT project, domain, primary_skill, risk_level, portfolio_priority FROM portfolio_metrics WHERE LOWER(domain) LIKE '%healthcare%' LIMIT 100",
 "risk_summary":"SELECT risk_level, COUNT(*) AS project_count FROM portfolio_metrics GROUP BY risk_level ORDER BY project_count DESC",
 "all":"SELECT project, domain, primary_skill, risk_level, portfolio_priority FROM portfolio_metrics LIMIT 100",
}
def initialize_database(csv_path: Path, db_path: Path) -> None:
    db_path.parent.mkdir(parents=True,exist_ok=True)
    df=pd.read_csv(csv_path)
    with sqlite3.connect(db_path) as conn: df.to_sql("portfolio_metrics",conn,if_exists="replace",index=False)
def select_template(question: str) -> str:
    q=question.lower()
    if any(t in q for t in ("highest","priority","top")): return "top_priority"
    if "healthcare" in q: return "healthcare"
    if "risk" in q: return "risk_summary"
    return "all"
def run_template(template_id: str, db_path: Path) -> pd.DataFrame:
    if template_id not in TEMPLATES: raise ValueError("Unknown SQL template")
    uri=f"file:{db_path}?mode=ro"
    with sqlite3.connect(uri,uri=True,timeout=5) as conn:
        return pd.read_sql_query(TEMPLATES[template_id],conn)
