"""
Data Loader & SQLite Connection Manager
Project: Email Campaign Effectiveness Analysis
Author: Moh Junaid (Roll: 250320140094), MCA 2nd Year (DA), ABES
"""

import os
import sqlite3
import pandas as pd
import streamlit as st

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "app.db")

def get_connection(db_path: str = DB_PATH) -> sqlite3.Connection:
    """
    Returns an active SQLite database connection with foreign key support enabled.
    """
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database file not found at: {db_path}")
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

@st.cache_data(ttl=3600, show_spinner=False)
def load_analytics_view(db_path: str = DB_PATH) -> pd.DataFrame:
    """
    Loads the 39-column flattened analytics view with caching.
    """
    conn = get_connection(db_path)
    query = "SELECT * FROM vw_campaign_effectiveness_analytics;"
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    # Datetime parsing
    if "dispatch_timestamp" in df.columns:
        df["dispatch_timestamp"] = pd.to_datetime(df["dispatch_timestamp"], errors="coerce")
    if "campaign_send_date" in df.columns:
        df["campaign_send_date"] = pd.to_datetime(df["campaign_send_date"], errors="coerce")
    return df

def get_table_counts(db_path: str = DB_PATH) -> dict:
    """
    Audits row counts across all physical database tables.
    """
    conn = get_connection(db_path)
    cursor = conn.cursor()
    tables = ["dim_campaigns", "dim_recipients", "fact_email_dispatches", "fact_conversions"]
    counts = {}
    for t in tables:
        counts[t] = cursor.execute(f"SELECT COUNT(*) FROM {t};").fetchone()[0]
    conn.close()
    return counts
