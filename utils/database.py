import sqlite3
import pandas as pd


DATABASE = "company.db"


def get_connection():

    return sqlite3.connect(DATABASE)


def load_data():

    conn = get_connection()

    df = pd.read_sql(
        "SELECT * FROM sales",
        conn
    )

    conn.close()

    df["order_date"] = pd.to_datetime(df["order_date"])

    return df
