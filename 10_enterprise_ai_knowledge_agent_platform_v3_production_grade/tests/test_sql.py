from pathlib import Path
from enterprise_ai_agent.tools.sql_tool import initialize_database,run_template
def test_sql(tmp_path:Path):
    csv=tmp_path/"d.csv"; csv.write_text("project,domain,primary_skill,risk_level,portfolio_priority\na,healthcare,rag,low,5\n",encoding="utf-8")
    db=tmp_path/"d.db"; initialize_database(csv,db)
    assert len(run_template("all",db))==1
