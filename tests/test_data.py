"""
Technical Tests: Database Integrity & Data Loading (TC-T-01 to TC-T-05)
Project: Email Campaign Effectiveness Analysis
Author: Moh Junaid (Roll: 250320140094), MCA 2nd Year (DA), ABES
"""

import os
import sqlite3
import pytest
import pandas as pd
from src.data_loader import get_connection, get_table_counts, DB_PATH

def test_tc_t_01_sqlite_connection():
    """
    TC-T-01: Verify SQLite database connects successfully with PRAGMA foreign_keys ON.
    """
    assert os.path.exists(DB_PATH), f"Database file does not exist at {DB_PATH}"
    conn = get_connection(DB_PATH)
    assert conn is not None
    cursor = conn.cursor()
    fk_setting = cursor.execute("PRAGMA foreign_keys;").fetchone()[0]
    conn.close()
    assert fk_setting == 1, "Foreign keys must be enabled (PRAGMA foreign_keys = 1)"

def test_tc_t_02_table_row_and_column_counts():
    """
    TC-T-02: Verify row counts match Step 8/10 targets and main fact table has 150+ rows.
    """
    counts = get_table_counts(DB_PATH)
    assert counts["dim_campaigns"] >= 20, "dim_campaigns must have >= 20 rows"
    assert counts["dim_recipients"] >= 100, "dim_recipients must have >= 100 rows"
    assert counts["fact_email_dispatches"] >= 150, "Main fact table must have >= 150 rows"
    assert counts["fact_conversions"] >= 15, "fact_conversions must have >= 15 rows"

def test_tc_t_03_primary_key_uniqueness():
    """
    TC-T-03: Verify primary keys are unique and non-null across all physical tables.
    """
    conn = get_connection(DB_PATH)
    cursor = conn.cursor()
    
    # Check dim_campaigns
    camp_dups = cursor.execute("SELECT campaign_id, COUNT(*) FROM dim_campaigns GROUP BY campaign_id HAVING COUNT(*) > 1;").fetchall()
    assert len(camp_dups) == 0, "Duplicate PK found in dim_campaigns"
    
    # Check dim_recipients
    rec_dups = cursor.execute("SELECT recipient_id, COUNT(*) FROM dim_recipients GROUP BY recipient_id HAVING COUNT(*) > 1;").fetchall()
    assert len(rec_dups) == 0, "Duplicate PK found in dim_recipients"
    
    # Check fact_email_dispatches
    disp_dups = cursor.execute("SELECT dispatch_id, COUNT(*) FROM fact_email_dispatches GROUP BY dispatch_id HAVING COUNT(*) > 1;").fetchall()
    assert len(disp_dups) == 0, "Duplicate PK found in fact_email_dispatches"
    
    # Check fact_conversions
    conv_dups = cursor.execute("SELECT conversion_id, COUNT(*) FROM fact_conversions GROUP BY conversion_id HAVING COUNT(*) > 1;").fetchall()
    assert len(conv_dups) == 0, "Duplicate PK found in fact_conversions"
    conn.close()

def test_tc_t_04_foreign_key_integrity():
    """
    TC-T-04: Verify zero foreign key violations using SQLite PRAGMA foreign_key_check.
    """
    conn = get_connection(DB_PATH)
    cursor = conn.cursor()
    fk_errors = cursor.execute("PRAGMA foreign_key_check;").fetchall()
    conn.close()
    assert len(fk_errors) == 0, f"Foreign key check failed! Violations found: {fk_errors}"

def test_tc_t_05_schema_boundaries_and_enums():
    """
    TC-T-05: Verify data integrity boundaries (non-negative counts, allowed enums).
    """
    conn = get_connection(DB_PATH)
    cursor = conn.cursor()
    
    # No negative opens or clicks
    neg_opens = cursor.execute("SELECT COUNT(*) FROM fact_email_dispatches WHERE total_opens_count < 0 OR total_clicks_count < 0;").fetchone()[0]
    assert neg_opens == 0, "Negative open or click counts detected"
    
    # Valid delivery status enums
    inv_status = cursor.execute("SELECT COUNT(*) FROM fact_email_dispatches WHERE delivery_status NOT IN ('Delivered', 'Bounced');").fetchone()[0]
    assert inv_status == 0, "Invalid delivery status enum values detected"
    
    # Analytics View column count check (should be between 30 and 40 columns)
    cursor.execute("PRAGMA table_info(vw_campaign_effectiveness_analytics);")
    cols = cursor.fetchall()
    conn.close()
    assert 30 <= len(cols) <= 40, f"Analytics view must have 30-40 columns, got {len(cols)}"
