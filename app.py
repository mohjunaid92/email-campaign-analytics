"""
Master Entrypoint & Global Filter Hub
Project: Email Campaign Effectiveness Analysis
Author: Moh Junaid (Roll: 250320140094), MCA 2nd Year (DA), ABES
Target Org: Nexura Tech Solutions Pvt. Ltd., Noida
"""

import os
import streamlit as st
import pandas as pd
import datetime
from src.data_loader import load_joined_data, standardize_campaign_dataframe, BASE_DIR
from src.data_cleaner import clean_campaign_data
from src.metrics import calculate_dataframe_kpis
from src.ui import render_hero_header, render_kpi_card, render_insight_box

# Page configuration
st.set_page_config(
    page_title="Nexura Email Analytics",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar Filter & Ingestion Hub
with st.sidebar:
    st.markdown("### 🏢 Nexura Tech Solutions")
    st.caption("B2B SaaS Email Marketing Intelligence | Noida, India")
    st.markdown("---")

    # Ingestion Option: Upload Custom Data
    st.markdown("#### 📂 Ingest Custom Campaign Data")
    uploaded_file = st.file_uploader(
        "Upload Campaign CSV or Excel",
        type=["csv", "xlsx", "xls"],
        help="Upload your own email marketing dataset to instantly calculate KPIs, conversion funnels, and benchmarks."
    )

    template_path = os.path.join(BASE_DIR, "data", "vw_campaign_effectiveness_analytics.csv")
    if os.path.exists(template_path):
        with open(template_path, "rb") as f_temp:
            st.download_button(
                label="📥 Download Sample CSV Template",
                data=f_temp.read(),
                file_name="nexura_sample_campaign_data.csv",
                mime="text/csv",
                use_container_width=True
            )

    st.markdown("---")

# Determine Data Source (Uploaded File vs Default Database)
if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith((".xlsx", ".xls")):
            raw_upload = pd.read_excel(uploaded_file)
        else:
            raw_upload = pd.read_csv(uploaded_file)
        standardized_df = standardize_campaign_dataframe(raw_upload)
        df_clean, audit_info = clean_campaign_data(standardized_df)
        raw_df = standardized_df
        st.session_state["is_custom_dataset"] = True
        st.session_state["dataset_source_name"] = uploaded_file.name
    except Exception as e:
        st.sidebar.error(f"Error parsing uploaded file: {e}")
        raw_df = load_joined_data()
        df_clean, audit_info = clean_campaign_data(raw_df)
        st.session_state["is_custom_dataset"] = False
        st.session_state["dataset_source_name"] = "Default SQLite Database"
else:
    raw_df = load_joined_data()
    df_clean, audit_info = clean_campaign_data(raw_df)
    st.session_state["is_custom_dataset"] = False
    st.session_state["dataset_source_name"] = "Default SQLite Database"

# Store active dataframes in session state for child pages
st.session_state["raw_df"] = raw_df
st.session_state["audit_info"] = audit_info

# Initialize Session State Filters
all_campaign_types = sorted(list(df_clean["campaign_type"].dropna().unique())) if "campaign_type" in df_clean.columns else []
all_industries = sorted(list(df_clean["industry"].dropna().unique())) if "industry" in df_clean.columns else []
all_sizes = sorted(list(df_clean["company_size"].dropna().unique())) if "company_size" in df_clean.columns else []
all_seniorities = sorted(list(df_clean["job_seniority_level"].dropna().unique())) if "job_seniority_level" in df_clean.columns else []

if "filters_initialized" not in st.session_state or st.session_state.get("last_loaded_dataset") != st.session_state["dataset_source_name"]:
    st.session_state["filters_initialized"] = True
    st.session_state["last_loaded_dataset"] = st.session_state["dataset_source_name"]
    st.session_state["selected_campaign_types"] = all_campaign_types
    st.session_state["selected_industries"] = all_industries
    st.session_state["selected_sizes"] = all_sizes
    st.session_state["selected_seniorities"] = all_seniorities

# Sidebar Filter Hub Controls
with st.sidebar:
    if st.session_state.get("is_custom_dataset", False):
        st.success(f"🟢 **Custom Data Active:** `{st.session_state['dataset_source_name']}` ({len(df_clean):,} records)")
    else:
        st.info(f"📊 **Active:** {st.session_state['dataset_source_name']} (375 records)")

    st.markdown("#### 🎯 Global Dynamic Filters")

    # Filter 1: Campaign Type
    selected_campaign_types = st.multiselect(
        "Campaign Type",
        options=all_campaign_types,
        default=[t for t in st.session_state.get("selected_campaign_types", all_campaign_types) if t in all_campaign_types]
    )
    st.session_state["selected_campaign_types"] = selected_campaign_types

    # Filter 2: Industry
    selected_industries = st.multiselect(
        "Recipient Industry",
        options=all_industries,
        default=[i for i in st.session_state.get("selected_industries", all_industries) if i in all_industries]
    )
    st.session_state["selected_industries"] = selected_industries

    # Filter 3: Company Size
    selected_sizes = st.multiselect(
        "Company Size",
        options=all_sizes,
        default=[s for s in st.session_state.get("selected_sizes", all_sizes) if s in all_sizes]
    )
    st.session_state["selected_sizes"] = selected_sizes

    # Filter 4: Seniority
    selected_seniorities = st.multiselect(
        "Job Seniority",
        options=all_seniorities,
        default=[sn for sn in st.session_state.get("selected_seniorities", all_seniorities) if sn in all_seniorities]
    )
    st.session_state["selected_seniorities"] = selected_seniorities

    st.markdown("---")
    if st.button("🔄 Reset All Filters", use_container_width=True):
        st.session_state["selected_campaign_types"] = all_campaign_types
        st.session_state["selected_industries"] = all_industries
        st.session_state["selected_sizes"] = all_sizes
        st.session_state["selected_seniorities"] = all_seniorities
        st.rerun()

    st.caption("Filters dynamically update all 8 analytical pages.")

# Apply filters to current view
filtered_df = df_clean.copy()
if selected_campaign_types and "campaign_type" in filtered_df.columns:
    filtered_df = filtered_df[filtered_df["campaign_type"].isin(selected_campaign_types)]
if selected_industries and "industry" in filtered_df.columns:
    filtered_df = filtered_df[filtered_df["industry"].isin(selected_industries)]
if selected_sizes and "company_size" in filtered_df.columns:
    filtered_df = filtered_df[filtered_df["company_size"].isin(selected_sizes)]
if selected_seniorities and "job_seniority_level" in filtered_df.columns:
    filtered_df = filtered_df[filtered_df["job_seniority_level"].isin(selected_seniorities)]

# Store active filtered dataframe in session state for child pages
st.session_state["active_filtered_df"] = filtered_df

# Main Presentation
render_hero_header(
    title="Email Campaign Effectiveness Analysis",
    subtitle="Enterprise Performance Cockpit | Attribution, Deliverability & A/B Statistical Inference",
    badge_text="Nexura Tech Solutions • Live"
)

if st.session_state.get("is_custom_dataset", False):
    st.success(f"📂 **Custom Dataset Active:** Currently evaluating `{st.session_state.get('dataset_source_name')}` with **{len(df_clean):,}** clean records. All KPI cards, charts, and 8 navigation pages reflect your uploaded data.")

st.markdown("### 📊 Enterprise Marketing KPI Snapshot")
kpis = calculate_dataframe_kpis(filtered_df)

c1, c2, c3, c4 = st.columns(4)
with c1:
    render_kpi_card("Total Dispatched", f"{kpis['total_dispatched']:,}", f"{kpis['delivery_rate']}% Delivered", "positive")
with c2:
    render_kpi_card("Unique Open Rate", f"{kpis['open_rate']}%", "Target ≥ 22.0%", "positive" if kpis['open_rate'] >= 22.0 else "warning")
with c3:
    render_kpi_card("Click-Through Rate", f"{kpis['ctr']}%", "Target ≥ 3.5%", "positive" if kpis['ctr'] >= 3.5 else "warning")
with c4:
    render_kpi_card("Attributed Revenue", f"${kpis['total_revenue']:,.2f}", f"ROI {kpis['roi']}%", "positive" if kpis['roi'] > 0 else "negative")

st.markdown("---")

# Navigation Guidance & Architecture Overview
st.markdown("### 🧭 Modular Analytical Workspaces")
st.markdown("Select a module from the **left sidebar** to begin deep-dive exploratory data analysis:")

col_a, col_b = st.columns(2)

with col_a:
    with st.container(border=True):
        st.markdown("#### 📈 01 · Executive Overview & Funnel")
        st.write("Top-line KPI cockpit, full marketing funnel conversion drop-offs, and campaign type leaderboards.")
        st.caption("Supports: OQ-01, OQ-02, OQ-07 | BR-01, BR-02, BR-07 | US-01, US-02, US-03")

    with st.container(border=True):
        st.markdown("#### 👥 02 · Audience Segmentation")
        st.write("Granular B2B cohort drill-downs across Recipient Industry, Company Size, and Seniority tiers.")
        st.caption("Supports: OQ-03, OQ-04 | BR-04, BR-05 | US-04, US-05")

    with st.container(border=True):
        st.markdown("#### ⚖️ 03 · Campaign Compare")
        st.write("Side-by-side radar benchmarking and Cost per Acquisition (CPA) vs. Revenue bubble matrices.")
        st.caption("Supports: OQ-06 | BR-06 | US-06, US-07")

    with st.container(border=True):
        st.markdown("#### ⏰ 04 · Temporal Trends & Send Timing")
        st.write("Hour-of-day and day-of-week engagement heatmaps identifying the optimal email send windows.")
        st.caption("Supports: OQ-08 | BR-08 | US-08, US-09")

with col_b:
    with st.container(border=True):
        st.markdown("#### 🧪 05 · A/B Testing & Statistical Lab")
        st.write("Two-proportion pooled z-tests, p-value calculations, and normal distribution confidence curves.")
        st.caption("Supports: OQ-09, OQ-10 | BR-09, BR-10 | US-10, US-11")

    with st.container(border=True):
        st.markdown("#### 🛡️ 06 · Deliverability & Churn Watchtower")
        st.write("Hard and soft bounce tracking, spam complaints, unsubscribe rates, and sender reputation scores.")
        st.caption("Supports: OQ-05 | BR-03 | US-12, US-13")

    with st.container(border=True):
        st.markdown("#### 🧹 07 · Data Quality & Cleaning Audit")
        st.write("Transparent data engineering audit log showing deduplication, median imputation, and outlier fixes.")
        st.caption("Supports: BR-11, BR-12 | US-14")

    with st.container(border=True):
        st.markdown("#### ℹ️ 08 · About & Technical Architecture")
        st.write("Academic project metadata, Nexura Tech Solutions profile, Snowflake schema, and technology stack.")
        st.caption("Supports: US-15 | Project Governance & Academic Submission")

st.markdown("---")
render_insight_box(
    title="Data Governance & Privacy Confirmation",
    message="This system operates strictly on synthetic, privacy-compliant data (Seed 42) modeling 375 dispatches across 25 B2B campaigns for Nexura Tech Solutions Pvt. Ltd., Noida. Zero real-world PII is stored or processed.",
    level="info"
)
