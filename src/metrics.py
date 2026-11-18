"""
Marketing KPI Calculations & Financial Attribution Engine
Project: Email Campaign Effectiveness Analysis
Author: Moh Junaid (Roll: 250320140094), MCA 2nd Year (DA), ABES
"""

def calculate_delivery_rate(delivered: int, dispatched: int) -> float:
    """
    Computes Delivery Rate (%) with zero-division guard.
    Delivery Rate = (Delivered / Dispatched) * 100
    """
    if dispatched <= 0:
        return 0.0
    return round((delivered / dispatched) * 100.0, 2)

def calculate_open_rate(unique_opens: int, delivered: int) -> float:
    """
    Computes Unique Open Rate (%) with zero-division guard.
    Open Rate = (Unique Opens / Delivered) * 100
    """
    if delivered <= 0:
        return 0.0
    return round((unique_opens / delivered) * 100.0, 2)

def calculate_ctr(unique_clicks: int, delivered: int) -> float:
    """
    Computes Click-Through Rate (CTR %) with zero-division guard.
    CTR = (Unique Clicks / Delivered) * 100
    """
    if delivered <= 0:
        return 0.0
    return round((unique_clicks / delivered) * 100.0, 2)

def calculate_ctor(unique_clicks: int, unique_opens: int) -> float:
    """
    Computes Click-to-Open Rate (CTOR %) with strict zero-division guard.
    CTOR = (Unique Clicks / Unique Opens) * 100
    Returns 0.0% if Unique Opens == 0.
    """
    if unique_opens <= 0:
        return 0.0
    return round((unique_clicks / unique_opens) * 100.0, 2)

def calculate_conversion_rate(conversions: int, delivered: int) -> float:
    """
    Computes Conversion Rate (%) with zero-division guard.
    Conversion Rate = (Conversions / Delivered) * 100
    """
    if delivered <= 0:
        return 0.0
    return round((conversions / delivered) * 100.0, 2)

def calculate_cpa(total_cost: float, conversions: int) -> float:
    """
    Computes Cost Per Acquisition ($) with zero-division guard.
    CPA = Total Cost / Conversions
    """
    if conversions <= 0:
        return 0.0
    return round(total_cost / conversions, 2)

def calculate_roi(attributed_revenue: float, total_cost: float) -> float:
    """
    Computes Net Return on Investment (ROI %) with zero-division guard.
    ROI = ((Attributed Revenue - Total Cost) / Total Cost) * 100
    """
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
