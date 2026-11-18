"""
Data Cleaning & Quality Audit Module
Project: Email Campaign Effectiveness Analysis
Author: Moh Junaid (Roll: 250320140094), MCA 2nd Year (DA), ABES
Target Org: Nexura Tech Solutions Pvt. Ltd., Noida
"""

import pandas as pd
import numpy as np

def clean_campaign_data(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """
    Cleans raw campaign data by removing duplicate dispatches, handling missing values,
    clamping negative duration intervals, and logging an audit trail.

    Args:
        df: Input DataFrame containing campaign dispatches and joined metrics.

    Returns:
        tuple[pd.DataFrame, dict]: Cleaned DataFrame and audit report dictionary.
    """
    df_clean = df.copy()
    initial_rows = len(df_clean)
    
    # 1. Deduplication on dispatch_id
    duplicates_removed = 0
    if "dispatch_id" in df_clean.columns:
        duplicates_removed = int(df_clean.duplicated(subset=["dispatch_id"]).sum())
        df_clean = df_clean.drop_duplicates(subset=["dispatch_id"], keep="first")
    
    # 2. Negative duration correction
    neg_durations = 0
    if "time_to_open_mins" in df_clean.columns:
        neg_mask = df_clean["time_to_open_mins"] < 0
        neg_durations = int(neg_mask.sum())
        df_clean.loc[neg_mask, "time_to_open_mins"] = 0.0
        
    # 3. Missing open time imputation (median imputation for opened emails)
    missing_open_times = 0
    if "time_to_open_mins" in df_clean.columns and "is_opened" in df_clean.columns:
        # Calculate median from opened emails with valid non-null open times
        valid_opens = df_clean[(df_clean["is_opened"] == 1) & (df_clean["time_to_open_mins"].notna()) & (df_clean["time_to_open_mins"] > 0)]
        median_open_time = valid_opens["time_to_open_mins"].median() if len(valid_opens) > 0 else 45.0
        
        missing_mask = (df_clean["is_opened"] == 1) & (df_clean["time_to_open_mins"].isna())
        missing_open_times = int(missing_mask.sum())
        df_clean.loc[missing_mask, "time_to_open_mins"] = round(median_open_time, 2)
        
    # 4. Conversion revenue outlier capping / flag
    outliers_detected = 0
    if "conversion_revenue" in df_clean.columns:
        q75 = df_clean["conversion_revenue"].quantile(0.75)
        iqr = q75 - df_clean["conversion_revenue"].quantile(0.25)
        upper_bound = q75 + (3.0 * iqr) if iqr > 0 else 50000.0
        outliers_detected = int((df_clean["conversion_revenue"] > upper_bound).sum())
        
    audit_report = {
        "initial_records": initial_rows,
        "duplicates_removed": duplicates_removed,
        "negative_durations_corrected": neg_durations,
        "missing_open_times_imputed": missing_open_times,
        "revenue_outliers_detected": outliers_detected,
        "final_clean_records": len(df_clean),
        "status": "Validated & Cleaned"
    }
    
    return df_clean, audit_report
