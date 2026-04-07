import pandas as pd
import pyodbc
from config import SYNAPSE_SERVER, SYNAPSE_DATABASE, SYNAPSE_USERNAME, SYNAPSE_PASSWORD, DATA_DIR

SQL_QUERY = """
WITH child_base AS (
    SELECT
        c.ChildKey,
        c.Age,
        c.GenderCode,
        c.PrimaryLanguageCode,
        c.IEPIndicator,
        c.CalWORKsIndicator,
        cl.ClassroomKey,
        cl.ProgramType,
        cl.Capacity,
        CASE
            WHEN c.ChildKey IS NOT NULL THEN 1
            ELSE 0
        END AS enrollment_flag
    FROM dbo.Child c
    LEFT JOIN dbo.ChildClassroom cc
        ON c.ChildKey = cc.ChildKey
    LEFT JOIN dbo.Classroom cl
        ON cc.ClassroomKey = cl.ClassroomKey
)
SELECT *
FROM child_base
"""

def get_connection() -> pyodbc.Connection:
    conn_str = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={SYNAPSE_SERVER};"
        f"DATABASE={SYNAPSE_DATABASE};"
        f"UID={SYNAPSE_USERNAME};"
        f"PWD={SYNAPSE_PASSWORD};"
        "Encrypt=yes;TrustServerCertificate=no;"
    )
    return pyodbc.connect(conn_str)

def main() -> None:
    conn = get_connection()
    df = pd.read_sql(SQL_QUERY, conn)
    out_path = DATA_DIR / "raw_capsdac.csv"
    df.to_csv(out_path, index=False)
    print(f"Saved raw data to {out_path}")

if __name__ == "__main__":
    main()
