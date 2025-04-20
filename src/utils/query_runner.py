import os
import psycopg2
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

def run_query(file_name, params=None):
    with open(f"queries/2-clientes_individuais/{file_name}", "r") as f:
        query = f.read()
    with get_connection() as conn:
        df = pd.read_sql_query(query, conn, params=params)
    return df