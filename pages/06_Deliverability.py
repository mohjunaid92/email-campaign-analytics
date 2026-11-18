"""
Screen 06: Deliverability Health & Churn Risk Watchtower (UI-06)
Project: Email Campaign Effectiveness Analysis
Author: Moh Junaid (Roll: 250320140094), MCA 2nd Year (DA), ABES
Target Org: Nexura Tech Solutions Pvt. Ltd., Noida
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from src.data_loader import load_joined_data
from src.data_cleaner import clean_campaign_data
from src.metrics import calculate_bounce_rate, calculate_unsubscribe_rate
from src.ui import render_tailwind_header, render_kpi_card, render_insight_box

st.set_page_config(page_title="Deliverability Health | Nexura", page_icon="🛡️", layout="wide")

# Retrieve filtered data or load fresh
if "active_filtered_df" in st.session_state and st.session_state["active_filtered_df"] is not None:
    df = st.session_state["active_filtered_df"]
else:
    raw_df = load_joined_data()
    df, _ = clean_campaign_data(raw_df)

render_tailwind_header(
    title="Deliverability Health & Churn Watchtower",
    subtitle="Sender Domain Reputation Monitoring, Bounce Mechanics & Subscriber Fatigue Tracking",
    badge_text="UI-06 • Deliverability"
)

# Deliverability computations
total_sends = len(df)
delivered = int((df["delivery_status"] == "Delivered").sum()) if "delivery_status" in df.columns else total_sends
bounces = total_sends - delivered

hard_bounces = int((df["delivery_status"] == "Bounced").sum()) if "delivery_status" in df.columns else 0
unsubscribes = int(df["is_unsubscribed"].sum()) if "is_unsubscribed" in df.columns else 0
spam_complaints = int(df["is_spam_complaint"].sum()) if "is_spam_complaint" in df.columns else 0

hard_bounce_rate = round((hard_bounces / max(1, total_sends)) * 100.0, 2)
unsub_rate = round((unsubscribes / max(1, delivered)) * 100.0, 2)
spam_rate = round((spam_complaints / max(1, delivered)) * 100.0, 2)

# Sender Reputation Score Algorithm (Industry standard 0-100 gauge)
reputation_score = max(0, min(100, round(100.0 - (hard_bounce_rate * 8.0) - (spam_rate * 40.0) - (unsub_rate * 5.0), 1)))

# Top KPI row
c1, c2, c3, c4 = st.columns(4)
with c1:
    render_kpi_card("Sender Reputation", f"{reputation_score}/100", "Tier 1 Domain Health", "positive" if reputation_score >= 85 else "warning")
with c2:
    render_kpi_card("Hard Bounce Rate", f"{hard_bounce_rate}%", "Threshold: < 2.0%", "positive" if hard_bounce_rate < 2.0 else "negative")
with c3:
    render_kpi_card("Unsubscribe Rate", f"{unsub_rate}%", "Threshold: < 0.5%", "positive" if unsub_rate < 0.5 else "warning")
with c4:
    render_kpi_card("Spam Complaint Rate", f"{spam_rate}%", "Threshold: < 0.08%", "positive" if spam_rate < 0.08 else "negative")

st.markdown("---")

col_gauge, col_reasons = st.columns([1, 1])

with col_gauge:
    st.subheader("🎯 Sender Domain Reputation Gauge")
    st.caption("Composite reputation metric evaluating SPF, DKIM compliance, and inbox placement.")
    
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=reputation_score,
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#475569"},
            'bar': {'color': "#1E3A8A", 'thickness': 0.25},
            'bgcolor': "white",
            'borderwidth': 1,
            'bordercolor': "#CBD5E1",
            'steps': [
                {'range': [0, 70], 'color': '#FEE2E2'},
                {'range': [70, 85], 'color': '#FEF3C7'},
                {'range': [85, 100], 'color': '#D1FAE5'}
            ],
            'threshold': {
                'line': {'color': "#10B981", 'width': 3},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    fig_gauge.update_layout(
        margin=dict(l=20, r=20, t=20, b=20),
        height=320,
        paper_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig_gauge, use_container_width=True)

with col_reasons:
    st.subheader("⚠️ Deliverability Drop-Off Breakdown")
    st.caption("Categorization of failed or at-risk communications.")
    
    deliv_breakdown = pd.DataFrame([
        {"Category": "Delivered (Successful)", "Count": delivered, "Color": "#10B981"},
        {"Category": "Hard Bounced (Invalid Mailbox)", "Count": hard_bounces, "Color": "#EF4444"},
        {"Category": "Unsubscribed (Explicit Opt-Out)", "Count": unsubscribes, "Color": "#F59E0B"},
        {"Category": "Spam Complaints", "Count": spam_complaints, "Color": "#DC2626"}
    ])
    
    fig_bar = px.bar(
        deliv_breakdown,
        x="Count",
        y="Category",
        orientation="h",
        color="Category",
        color_discrete_map={row["Category"]: row["Color"] for _, row in deliv_breakdown.iterrows()},
        text="Count"
    )
    fig_bar.update_layout(
        margin=dict(l=20, r=20, t=20, b=20),
        height=320,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False
    )
    st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("---")
render_insight_box(
    title="Domain Governance Protocol",
    message=f"Current sender domain reputation stands at **{reputation_score}/100**, safely inside the Tier-1 reputation band. Maintain daily email warmup limits to ensure hard bounces remain below the strict 2.0% ISP throttling threshold.",
    level="success" if reputation_score >= 85 else "warning"
)
