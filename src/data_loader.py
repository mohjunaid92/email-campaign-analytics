"""
Data Loader & SQLite Connection Manager
Project: Email Campaign Effectiveness Analysis
Author: Moh Junaid (Roll: 250320140094), MCA 2nd Year (DA), ABES
Target Org: Nexura Tech Solutions Pvt. Ltd., Noida
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

def standardize_campaign_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardizes raw tabular data (from SQLite, CSV, or Excel uploads)
    by mapping database columns to uniform analytical aliases.
    """
    df = df.copy()

    # Datetime parsing
    if "dispatch_timestamp" in df.columns:
        df["dispatch_timestamp"] = pd.to_datetime(df["dispatch_timestamp"], errors="coerce")
    if "dispatch_date" in df.columns:
        df["dispatch_date"] = pd.to_datetime(df["dispatch_date"], errors="coerce")
        if "dispatch_timestamp" not in df.columns:
            df["dispatch_timestamp"] = df["dispatch_date"]
    if "campaign_send_date" in df.columns:
        df["campaign_send_date"] = pd.to_datetime(df["campaign_send_date"], errors="coerce")

    # Standard friendly column aliases for dashboard and test compatibility
    if "campaign_category" in df.columns and "campaign_type" not in df.columns:
        df["campaign_type"] = df["campaign_category"]
    elif "campaign_type" in df.columns and "campaign_category" not in df.columns:
        df["campaign_category"] = df["campaign_type"]

    if "recipient_industry" in df.columns and "industry" not in df.columns:
        df["industry"] = df["recipient_industry"]
    elif "industry" in df.columns and "recipient_industry" not in df.columns:
        df["recipient_industry"] = df["industry"]

    if "recipient_account_tier" in df.columns:
        if "company_size" not in df.columns:
            df["company_size"] = df["recipient_account_tier"]
        if "account_tier" not in df.columns:
            df["account_tier"] = df["recipient_account_tier"]
        if "job_seniority_level" not in df.columns:
            seniority_map = {
                "Enterprise": "C-Suite",
                "Mid-Market": "VP",
                "SMB": "Director",
                "Startup": "Manager"
            }
            df["job_seniority_level"] = df["recipient_account_tier"].map(seniority_map).fillna("Director")
    elif "account_tier" in df.columns or "company_size" in df.columns:
        tier_col = "account_tier" if "account_tier" in df.columns else "company_size"
        if "recipient_account_tier" not in df.columns:
            df["recipient_account_tier"] = df[tier_col]
        if "company_size" not in df.columns:
            df["company_size"] = df[tier_col]
        if "job_seniority_level" not in df.columns:
            seniority_map = {
                "Enterprise": "C-Suite",
                "Mid-Market": "VP",
                "SMB": "Director",
                "Startup": "Manager"
            }
            df["job_seniority_level"] = df[tier_col].map(seniority_map).fillna("Director")

    if "campaign_budget_cost" in df.columns and "campaign_budget" not in df.columns:
        df["campaign_budget"] = df["campaign_budget_cost"]
    elif "campaign_budget" in df.columns and "campaign_budget_cost" not in df.columns:
        df["campaign_budget_cost"] = df["campaign_budget"]
    elif "campaign_cost" in df.columns:
        if "campaign_budget" not in df.columns:
            df["campaign_budget"] = df["campaign_cost"]
        if "campaign_budget_cost" not in df.columns:
            df["campaign_budget_cost"] = df["campaign_cost"]

    if "conversion_deal_value" in df.columns and "conversion_revenue" not in df.columns:
        df["conversion_revenue"] = df["conversion_deal_value"].fillna(0.0)
    elif "conversion_revenue" in df.columns and "conversion_deal_value" not in df.columns:
        df["conversion_deal_value"] = df["conversion_revenue"].fillna(0.0)

    if "campaign_send_hour" in df.columns and "send_hour" not in df.columns:
        df["send_hour"] = df["campaign_send_hour"]
    elif "send_hour" in df.columns and "campaign_send_hour" not in df.columns:
        df["campaign_send_hour"] = df["send_hour"]

    if "campaign_send_day_name" in df.columns:
        if "send_day" not in df.columns:
            df["send_day"] = df["campaign_send_day_name"]
        if "weekday" not in df.columns:
            df["weekday"] = df["campaign_send_day_name"]
    elif "send_day" in df.columns:
        if "weekday" not in df.columns:
            df["weekday"] = df["send_day"]
        if "campaign_send_day_name" not in df.columns:
            df["campaign_send_day_name"] = df["send_day"]

    if "time_to_open_mins" not in df.columns and "first_open_timestamp" in df.columns and "dispatch_timestamp" in df.columns:
        open_dt = pd.to_datetime(df["first_open_timestamp"], errors="coerce")
        disp_dt = pd.to_datetime(df["dispatch_timestamp"], errors="coerce")
        df["time_to_open_mins"] = (open_dt - disp_dt).dt.total_seconds() / 60.0

    if "is_delivered" not in df.columns and "delivery_status" in df.columns:
        df["is_delivered"] = (df["delivery_status"] == "Delivered").astype(int)
    if "is_bounced" not in df.columns and "delivery_status" in df.columns:
        df["is_bounced"] = (df["delivery_status"] == "Bounced").astype(int)
    if "is_spam_complaint" not in df.columns:
        df["is_spam_complaint"] = 0
    if "is_converted" in df.columns:
        df["is_converted"] = df["is_converted"].fillna(0).astype(int)

    return df

@st.cache_data(ttl=3600, show_spinner=False)
def load_analytics_view(db_path: str = DB_PATH) -> pd.DataFrame:
    """
    Loads the flattened analytics view with caching and adds standard analytical aliases.
    """
    conn = get_connection(db_path)
    query = "SELECT * FROM vw_campaign_effectiveness_analytics;"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return standardize_campaign_dataframe(df)

def load_joined_data(db_path: str = DB_PATH) -> pd.DataFrame:
    """
    Alias for load_analytics_view to support standard naming across Build Plan specifications.
    """
    return load_analytics_view(db_path)

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
