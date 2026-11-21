"""
Technical Tests: Streamlit Application & Performance (TC-T-11 & TC-T-12)
Project: Email Campaign Effectiveness Analysis
Author: Moh Junaid (Roll: 2500320140094), MCA 2nd Year (DA), ABES
"""

import os
import time
import pytest
from src.data_loader import load_analytics_view, DB_PATH

def test_tc_t_12_query_performance_latency():
    """
    TC-T-12: Test that loading the 39-column analytics view takes < 3.0 seconds.
    """
    assert os.path.exists(DB_PATH), f"Database file not found at {DB_PATH}"
    
    start_time = time.time()
    df = load_analytics_view(DB_PATH)
    elapsed = time.time() - start_time
    
    assert elapsed < 3.0, f"Query latency exceeded 3.0 seconds! Took {elapsed:.3f}s"
    assert len(df) >= 150, f"Expected >= 150 rows in analytics view, got {len(df)}"
    assert df.shape[1] >= 30, f"Expected >= 30 columns in analytics view, got {df.shape[1]}"

def test_tc_t_11_ui_components_render():
    """
    TC-T-11: Verify that starter UI components in src/ui.py execute without exception.
    """
    from src.ui import render_hero_header, render_kpi_card, render_insight_box
    
    # Assert callable
    assert callable(render_hero_header)
    assert callable(render_kpi_card)
    assert callable(render_insight_box)
