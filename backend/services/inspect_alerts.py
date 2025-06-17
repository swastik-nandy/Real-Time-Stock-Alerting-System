import psycopg2
from dotenv import load_dotenv
import os
from pathlib import Path
from tabulate import tabulate

# Load environment variables
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=BASE_DIR / '.env')

DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

try:
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM alerts_alert LIMIT 5;")
    rows = cursor.fetchall()

    # Get column names
    colnames = [desc[0] for desc in cursor.description]

    print("\n=== ALERTS TABLE SAMPLE ===\n")
    print(tabulate(rows, headers=colnames, tablefmt="pretty"))

    cursor.close()
    conn.close()

except Exception as e:
    print(f"Database connection failed: {e}")
