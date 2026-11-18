"""
Marketing KPI Calculations & Financial Attribution Engine
Project: Email Campaign Effectiveness Analysis
Author: Moh Junaid (Roll: 250320140094), MCA 2nd Year (DA), ABES
Target Org: Nexura Tech Solutions Pvt. Ltd., Noida
"""

import pandas as pd
import numpy as np

def calculate_delivery_rate(delivered=0, dispatched=0) -> float:
    """
    Computes Delivery Rate (%) with zero-division guard.
    Supports either scalar values or a pandas DataFrame as first argument.
    """
    if isinstance(delivered, pd.DataFrame):
        df = delivered
        dispatched = len(df)
        delivered = int((df["delivery_status"] == "Delivered").sum()) if "delivery_status" in df.columns else int(df["is_delivered"].sum()) if "is_delivered" in df.columns else dispatched
    if dispatched <= 0:
        return 0.0
    return round((delivered / dispatched) * 100.0, 2)

def calculate_open_rate(unique_opens=0, delivered=0) -> float:
    """
    Computes Unique Open Rate (%) with zero-division guard.
    Supports either scalar values or a pandas DataFrame as first argument.
    """
    if isinstance(unique_opens, pd.DataFrame):
        df = unique_opens
        delivered = int((df["delivery_status"] == "Delivered").sum()) if "delivery_status" in df.columns else len(df)
        unique_opens = int(df["is_opened"].sum()) if "is_opened" in df.columns else 0
    if delivered <= 0:
        return 0.0
    return round((unique_opens / delivered) * 100.0, 2)

def calculate_ctr(unique_clicks=0, delivered=0) -> float:
    """
    Computes Click-Through Rate (CTR %) with zero-division guard.
    Supports either scalar values or a pandas DataFrame as first argument.
    """
    if isinstance(unique_clicks, pd.DataFrame):
        df = unique_clicks
        delivered = int((df["delivery_status"] == "Delivered").sum()) if "delivery_status" in df.columns else len(df)
        unique_clicks = int(df["is_clicked"].sum()) if "is_clicked" in df.columns else 0
    if delivered <= 0:
        return 0.0
    return round((unique_clicks / delivered) * 100.0, 2)

def calculate_ctor(unique_clicks=0, unique_opens=0) -> float:
    """
    Computes Click-to-Open Rate (CTOR %) with strict zero-division guard.
    Supports either scalar values or a pandas DataFrame as first argument.
    """
    if isinstance(unique_clicks, pd.DataFrame):
        df = unique_clicks
        unique_opens = int(df["is_opened"].sum()) if "is_opened" in df.columns else 0
        unique_clicks = int(df["is_clicked"].sum()) if "is_clicked" in df.columns else 0
    if unique_opens <= 0:
        return 0.0
    return round((unique_clicks / unique_opens) * 100.0, 2)

def calculate_conversion_rate(conversions=0, delivered=0) -> float:
    """
    Computes Conversion Rate (%) with zero-division guard.
    Supports either scalar values or a pandas DataFrame as first argument.
    """
    if isinstance(conversions, pd.DataFrame):
        df = conversions
        delivered = int((df["delivery_status"] == "Delivered").sum()) if "delivery_status" in df.columns else len(df)
        conversions = int(df["is_converted"].sum()) if "is_converted" in df.columns else 0
    if delivered <= 0:
        return 0.0
    return round((conversions / delivered) * 100.0, 2)

def calculate_bounce_rate(bounces=0, dispatched=0) -> float:
    """
    Computes Bounce Rate (%) with zero-division guard.
    Supports either scalar values or a pandas DataFrame as first argument.
    """
    if isinstance(bounces, pd.DataFrame):
        df = bounces
        dispatched = len(df)
        bounces = int((df["delivery_status"] == "Bounced").sum()) if "delivery_status" in df.columns else int(df["is_bounced"].sum()) if "is_bounced" in df.columns else 0
    if dispatched <= 0:
        return 0.0
    return round((bounces / dispatched) * 100.0, 2)

def calculate_unsubscribe_rate(unsubscribes=0, delivered=0) -> float:
    """
    Computes Unsubscribe Rate (%) with zero-division guard.
    Supports either scalar values or a pandas DataFrame as first argument.
    """
    if isinstance(unsubscribes, pd.DataFrame):
        df = unsubscribes
        delivered = int((df["delivery_status"] == "Delivered").sum()) if "delivery_status" in df.columns else len(df)
        unsubscribes = int(df["is_unsubscribed"].sum()) if "is_unsubscribed" in df.columns else 0
    if delivered <= 0:
        return 0.0
    return round((unsubscribes / delivered) * 100.0, 2)

def calculate_cpa(total_cost: float = 0.0, conversions: int = 0) -> float:
    """
    Computes Cost Per Acquisition ($) with zero-division guard.
    """
    if conversions <= 0:
        return 0.0
    return round(total_cost / conversions, 2)

def calculate_total_revenue(df_or_revenue=0.0) -> float:
    """
    Computes Total Attributed Revenue ($).
    """
    if isinstance(df_or_revenue, pd.DataFrame):
        if "conversion_revenue" in df_or_revenue.columns:
            return round(float(df_or_revenue["conversion_revenue"].fillna(0).sum()), 2)
        return 0.0
    return round(float(df_or_revenue), 2)

def calculate_total_cost(df_or_cost=0.0) -> float:
    """
    Computes Total Campaign Cost / Spend ($).
    """
    if isinstance(df_or_cost, pd.DataFrame):
        if "campaign_budget" in df_or_cost.columns:
            # Drop duplicates if campaign_budget is repeated across dispatches
            if "campaign_id" in df_or_cost.columns:
                return round(float(df_or_cost.drop_duplicates(subset=["campaign_id"])["campaign_budget"].sum()), 2)
            return round(float(df_or_cost["campaign_budget"].sum()), 2)
        return 0.0
    return round(float(df_or_cost), 2)

def calculate_roi(attributed_revenue: float = 0.0, total_cost: float = 0.0) -> float:
    """
    Computes Net Return on Investment (ROI %) with zero-division guard.
    ROI = ((Attributed Revenue - Total Cost) / Total Cost) * 100
    Supports either scalar values or a single DataFrame.
    """
    if isinstance(attributed_revenue, pd.DataFrame):
        df = attributed_revenue
        attributed_revenue = calculate_total_revenue(df)
        total_cost = calculate_total_cost(df)
    if total_cost <= 0:
        return 0.0
    return round(((attributed_revenue - total_cost) / total_cost) * 100.0, 2)

def classify_recency_cohort(days_since_last_interaction: int) -> str:
    """
    Classifies subscriber engagement into longitudinal cohorts.
    """
    if days_since_last_interaction <= 30:
        return "Active"
    elif days_since_last_interaction <= 60:
        return "Cooling"
    elif days_since_last_interaction <= 90:
        return "Dormant"
    else:
        return "Churned"

def calculate_dataframe_kpis(df: pd.DataFrame) -> dict:
    """
    Computes all standard enterprise email KPIs for a filtered DataFrame.
    """
    total_dispatched = len(df)
    delivered = int((df["delivery_status"] == "Delivered").sum()) if "delivery_status" in df.columns else total_dispatched
    bounced = total_dispatched - delivered
    unique_opens = int(df["is_opened"].sum()) if "is_opened" in df.columns else 0
    unique_clicks = int(df["is_clicked"].sum()) if "is_clicked" in df.columns else 0
    conversions = int(df["is_converted"].sum()) if "is_converted" in df.columns else 0
    unsubscribes = int(df["is_unsubscribed"].sum()) if "is_unsubscribed" in df.columns else 0
    spam_complaints = int(df["is_spam_complaint"].sum()) if "is_spam_complaint" in df.columns else 0
    
    delivery_rate = calculate_delivery_rate(delivered, total_dispatched)
    open_rate = calculate_open_rate(unique_opens, delivered)
    ctr = calculate_ctr(unique_clicks, delivered)
    ctor = calculate_ctor(unique_clicks, unique_opens)
    conversion_rate = calculate_conversion_rate(conversions, delivered)
    bounce_rate = calculate_bounce_rate(bounced, total_dispatched)
    unsubscribe_rate = calculate_unsubscribe_rate(unsubscribes, delivered)
    spam_rate = round((spam_complaints / delivered * 100.0), 2) if delivered > 0 else 0.0
    
    total_revenue = calculate_total_revenue(df)
    total_cost = calculate_total_cost(df)
    roi = calculate_roi(total_revenue, total_cost)
    cpa = calculate_cpa(total_cost, conversions)
    
    return {
        "total_dispatched": total_dispatched,
        "delivered": delivered,
        "bounced": bounced,
        "delivery_rate": delivery_rate,
        "unique_opens": unique_opens,
        "open_rate": open_rate,
        "unique_clicks": unique_clicks,
        "ctr": ctr,
        "ctor": ctor,
        "conversions": conversions,
        "conversion_rate": conversion_rate,
        "unsubscribes": unsubscribes,
        "unsubscribe_rate": unsubscribe_rate,
        "spam_complaints": spam_complaints,
        "spam_rate": spam_rate,
        "total_revenue": total_revenue,
        "total_cost": total_cost,
        "net_profit": round(total_revenue - total_cost, 2),
        "roi": roi,
        "cpa": cpa
    }
