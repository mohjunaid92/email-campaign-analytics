"""
Screen 08: Academic Project Attribution & Technical Architecture (UI-08)
Project: Email Campaign Effectiveness Analysis
Author: Moh Junaid (Roll: 250320140094), MCA 2nd Year (DA), ABES
Target Org: Nexura Tech Solutions Pvt. Ltd., Noida
"""

import streamlit as st
import pandas as pd
from src.data_loader import get_table_counts, DB_PATH
from src.ui import render_tailwind_header, render_insight_box

st.set_page_config(page_title="About Project | Nexura", page_icon="ℹ️", layout="wide")

render_tailwind_header(
    title="Project Attribution & System Architecture",
    subtitle="Academic Capstone Metadata, Enterprise Profile, Database Schema & Governance",
    badge_text="UI-08 • Governance"
)

# Candidate & University Profile
st.markdown("### 🎓 Academic Capstone Metadata")
col_acad1, col_acad2 = st.columns(2)

with col_acad1:
    with st.container(border=True):
        st.markdown("#### 👤 Student Investigator")
        st.write("**Name:** Moh Junaid")
        st.write("**University Roll No:** 250320140094")
        st.write("**Degree:** Master of Computer Applications (MCA) — 2nd Year")
        st.write("**Specialization:** Data Analytics (DA)")
        st.write("**Institution:** ABES Engineering College, Ghaziabad, Uttar Pradesh")

with col_acad2:
    with st.container(border=True):
        st.markdown("#### 🏛️ Academic & Industry Context")
        st.write("**Project Mentor:** Mr. Dinesh")
        st.write("**Target Organisation:** Nexura Tech Solutions Pvt. Ltd.")
        st.write("**Location:** Sector 62, Noida, Uttar Pradesh, India")
        st.write("**Enterprise Profile:** 500 Employees | B2B SaaS & Digital Transformation")
        st.write("**Project Code:** ECEA-2024-NEXURA")

st.markdown("---")

# Production Endpoints
st.markdown("### 🌐 Live Production & Source Code Access")
col_end1, col_end2 = st.columns(2)

with col_end1:
    with st.container(border=True):
        st.markdown("#### ☁️ Streamlit Community Cloud")
        st.markdown("**Live Application:** [email-campaign-analytics-fce9uzyxn3arhsidpycbgp.streamlit.app](https://email-campaign-analytics-fce9uzyxn3arhsidpycbgp.streamlit.app/)")
        st.write("**Deployment Status:** Active & Public")
        st.write("**Environment:** Python 3.12 / Streamlit Multi-Page")

with col_end2:
    with st.container(border=True):
        st.markdown("#### 🐙 GitHub Repository")
        st.markdown("**Public Repository:** [mohjunaid92/email-campaign-analytics](https://github.com/mohjunaid92/email-campaign-analytics)")
        st.write("**Branch:** `main` (Verified clean working tree)")
        st.write("**License:** Academic Capstone Open Access")

st.markdown("---")

# Tech Stack & Architecture
st.markdown("### 🛠️ Production Technology Stack")
col_tech1, col_tech2, col_tech3 = st.columns(3)

with col_tech1:
    with st.container(border=True):
        st.markdown("#### 🐍 Backend & Logic")
        st.write("- **Language:** Python 3.12 (Pinned)")
        st.write("- **Data Manipulation:** pandas 2.2+, NumPy 1.26+")
        st.write("- **Statistical Modeling:** SciPy 1.12+, statsmodels")
        st.write("- **Test Automation:** pytest 8.0+")

with col_tech2:
    with st.container(border=True):
        st.markdown("#### 🗄️ Relational Data Tier")
        st.write("- **Engine:** SQLite 3 (`data/app.db`)")
        st.write("- **Schema:** Star/Snowflake Hybrid")
        st.write("- **Integrity:** `PRAGMA foreign_keys = ON`")
        st.write("- **Flat Analysis View:** 39 Columns")

with col_tech3:
    with st.container(border=True):
        st.markdown("#### 🎨 Frontend & Design")
        st.write("- **Framework:** Streamlit Multipage")
        st.write("- **Visualisation:** Plotly Express & Graph Objects")
        st.write("- **Micro-Components:** Tailwind CSS CDN")
        st.write("- **Sandboxing:** `st.components.v1.html`")

st.markdown("---")

# Database Inventory Table
st.markdown("### 📊 Database Relational Inventory")
counts = get_table_counts(DB_PATH)

table_data = pd.DataFrame([
    {"Table / Object Name": "dim_campaigns", "Classification": "Dimension", "Granularity": "1 row per campaign", "Row Count": f"{counts['dim_campaigns']:,}", "Primary Key": "campaign_id"},
    {"Table / Object Name": "dim_recipients", "Classification": "Dimension", "Granularity": "1 row per B2B recipient", "Row Count": f"{counts['dim_recipients']:,}", "Primary Key": "recipient_id"},
    {"Table / Object Name": "fact_email_dispatches", "Classification": "Fact (Dispatches)", "Granularity": "1 row per send event", "Row Count": f"{counts['fact_email_dispatches']:,}", "Primary Key": "dispatch_id"},
    {"Table / Object Name": "fact_conversions", "Classification": "Fact (Commercial)", "Granularity": "1 row per conversion deal", "Row Count": f"{counts['fact_conversions']:,}", "Primary Key": "conversion_id"},
    {"Table / Object Name": "vw_campaign_effectiveness_analytics", "Classification": "Reporting View", "Granularity": "1 row per dispatch (joined)", "Row Count": "375 rows (39 cols)", "Primary Key": "dispatch_id"}
])

st.dataframe(table_data, use_container_width=True, hide_index=True)

st.markdown("---")
render_insight_box(
    title="Traceability Governance Confirmation",
    message="Every metric, filter, and chart in this application is formally mapped through the Requirements Traceability Matrix (`docs/04_Traceability_Matrix.xlsx`), ensuring 100% bidirectional coverage across 10 Opportunity Questions (OQ), 12 Business Requirements (BR), 15 User Stories (US), and 12 Automated Test Suites (TC-T).",
    level="info"
)
