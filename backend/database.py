import mysql.connector
import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

def get_db_connection():
    db_name = os.getenv("DB_NAME", "credit_cards_db")
    print("🚨 Connecting to database:", db_name)  # DEBUG LINE
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=db_name
    )
