from pathlib import Path
from enterprise_ai_agent.tools.sql_tool import initialize_database
ROOT=Path(__file__).resolve().parents[1]
if __name__=="__main__":
    initialize_database(ROOT/"data/sample/sql/project_portfolio_metrics.csv",ROOT/"data/runtime/enterprise_agent.db")
    print("Demo database initialized")
