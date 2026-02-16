import csv
from db import init_db, get_connection
from pathlib import Path

CSV_PATH = Path(__file__).resolve().parent.parent / "data.csv"

init_db()
conn = get_connection()
cur = conn.cursor()

with open(CSV_PATH, encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        cur.execute("""
        INSERT OR REPLACE INTO patients VALUES (
            ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?
        )
        """, (
            int(row["patient_id"]),
            row["patient_name"],
            int(row["age"]),
            row["gender"],
            row["diagnosis"],
            row["diabetes"],
            row["smoking_status"],
            row["obesity"],
            row["chronic_kidney_disease"],
            row["anemia"],
            row["blood_pressure"],
            int(row["heart_rate"]),
            int(row["cholesterol"]),
            row["risk_level"],
            row["care_priority"],
            row["visit_date"]
        ))

conn.commit()
conn.close()
print(" CSV imported successfully")
