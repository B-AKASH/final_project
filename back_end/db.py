import sqlite3
import pandas as pd

CSV_PATH = "data.csv"
DB_PATH = "a.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_csv(CSV_PATH)

    df.to_sql("patients", conn, if_exists="replace", index=False)
    conn.commit()
    conn.close()

    print("SQLite DB initialized from CSV")

if __name__ == "__main__":
    init_db()
