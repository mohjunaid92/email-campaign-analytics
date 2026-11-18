"""
Technical Tests: KPI Formulas & Statistical Models (TC-T-06 to TC-T-10)
Project: Email Campaign Effectiveness Analysis
Author: Moh Junaid (Roll: 250320140094), MCA 2nd Year (DA), ABES
"""

import pytest
import math
from src.metrics import (
    calculate_delivery_rate,
    calculate_open_rate,
    calculate_ctr,
    calculate_ctor,
    calculate_conversion_rate,
    calculate_cpa,
    calculate_roi,
    classify_recency_cohort
)
from src.statistics import two_proportion_z_test

def test_tc_t_06_delivery_rate_formula():
    """
    TC-T-06: Test delivery rate calculation on a tiny known fixture and edge cases.
    """
    assert calculate_delivery_rate(delivered=98, dispatched=100) == 98.0
    assert calculate_delivery_rate(delivered=195, dispatched=200) == 97.5
    # Zero division guard
    assert calculate_delivery_rate(delivered=0, dispatched=0) == 0.0

def test_tc_t_07_open_rate_formula():
    """
    TC-T-07: Test unique open rate calculation on known numbers and edge cases.
    """
    assert calculate_open_rate(unique_opens=25, delivered=100) == 25.0
    assert calculate_open_rate(unique_opens=50, delivered=200) == 25.0
    # Zero division guard
    assert calculate_open_rate(unique_opens=0, delivered=0) == 0.0

def test_tc_t_08_ctr_and_ctor_with_zero_division_guard():
    """
    TC-T-08: Test CTR and CTOR formulas and verify that CTOR returns 0.0% when opens = 0.
    """
    # CTR = (Unique Clicks / Delivered) * 100
    assert calculate_ctr(unique_clicks=5, delivered=100) == 5.0
    assert calculate_ctr(unique_clicks=0, delivered=100) == 0.0
    assert calculate_ctr(unique_clicks=0, delivered=0) == 0.0
    
    # CTOR = (Unique Clicks / Unique Opens) * 100
    assert calculate_ctor(unique_clicks=5, unique_opens=25) == 20.0
    assert calculate_ctor(unique_clicks=10, unique_opens=50) == 20.0
    
    # CRITICAL: CTOR Zero Division Guard when unique_opens == 0
    assert calculate_ctor(unique_clicks=0, unique_opens=0) == 0.0

def test_tc_t_09_financial_cpa_and_roi():
    """
    TC-T-09: Test Cost Per Acquisition (CPA) and Net ROI on known financial numbers.
    """
    # CPA = Spend / Conversions
    assert calculate_cpa(total_cost=1500.0, conversions=10) == 150.0
    assert calculate_cpa(total_cost=1500.0, conversions=0) == 0.0  # Zero guard
    
    # ROI = ((Revenue - Cost) / Cost) * 100
    # Spend $1000, Revenue $3500 -> Net profit $2500 -> ROI = 250.0%
    assert calculate_roi(attributed_revenue=3500.0, total_cost=1000.0) == 250.0
    assert calculate_roi(attributed_revenue=1000.0, total_cost=1000.0) == 0.0
    assert calculate_roi(attributed_revenue=500.0, total_cost=1000.0) == -50.0

def test_tc_t_10_two_proportion_z_test_significance():
    """
    TC-T-10: Test SciPy two-proportion Z-test against known theoretical benchmarks.
    """
    # Known significant case:
    # Variant A: 18 opens out of 100 (18%)
    # Variant B: 34 opens out of 100 (34%)
    res = two_proportion_z_test(k1=34, n1=100, k2=18, n2=100, alpha=0.05)
    assert res["is_significant"] is True
    assert res["z_score"] > 1.96
    assert res["p_value"] < 0.05
    assert res["proportion_difference"] == 0.16
    
    # Known non-significant case (fluke margin):
    # Variant A: 20 opens out of 100
    # Variant B: 21 opens out of 100
    res_null = two_proportion_z_test(k1=21, n1=100, k2=20, n2=100, alpha=0.05)
    assert res_null["is_significant"] is False
    assert res_null["p_value"] > 0.05

def test_tc_t_11_recency_cohort_classification():
    """
    Test 90-day subscriber fatigue recency cohort logic.
    """
    assert classify_recency_cohort(10) == "Active"
    assert classify_recency_cohort(30) == "Active"
    assert classify_recency_cohort(45) == "Cooling"
    assert classify_recency_cohort(60) == "Cooling"
    assert classify_recency_cohort(75) == "Dormant"
    assert classify_recency_cohort(90) == "Dormant"
    assert classify_recency_cohort(91) == "Churned"
    assert classify_recency_cohort(180) == "Churned"
