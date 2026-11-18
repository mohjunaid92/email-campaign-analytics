"""
Screen 01: Executive Overview & Funnel Visualizer (UI-01)
Project: Email Campaign Effectiveness Analysis
Author: Moh Junaid (Roll: 250320140094), MCA 2nd Year (DA), ABES
Target Org: Nexura Tech Solutions Pvt. Ltd., Noida
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.data_loader import load_joined_data
from src.data_cleaner import clean_campaign_data
from src.metrics import calculate_dataframe_kpis
from src.ui import render_tailwind_header, render_kpi_card, render_insight_box

st.set_page_config(page_title="Executive Overview | Nexura", page_icon="📈", layout="wide")

# Retrieve filtered data or load fresh
if "active_filtered_df" in st.session_state and st.session_state["active_filtered_df"] is not None:
    df = st.session_state["active_filtered_df"]
else:
    raw_df = load_joined_data()
    df, _ = clean_campaign_data(raw_df)

render_tailwind_header(
    title="Executive Campaign Cockpit & Funnel Visualizer",
    subtitle="Full-Funnel Pipeline Attribution, Stage Drop-Off Analysis & Channel Velocity",
    badge_text="UI-01 • Executive"
)

# Top KPI row
kpis = calculate_dataframe_kpis(df)
c1, c2, c3, c4 = st.columns(4)
with c1:
    render_kpi_card("Delivered Volume", f"{kpis['delivered']:,}", f"{kpis['delivery_rate']}% of Sent", "positive")
with c2:
    render_kpi_card("Unique Open Rate", f"{kpis['open_rate']}%", "Benchmark: 22.0%", "positive" if kpis['open_rate'] >= 22.0 else "warning")
with c3:
    render_kpi_card("Click-Through Rate", f"{kpis['ctr']}%", "Benchmark: 3.5%", "positive" if kpis['ctr'] >= 3.5 else "warning")
with c4:
    render_kpi_card("Attributed Revenue", f"${kpis['total_revenue']:,.2f}", f"ROI {kpis['roi']}%", "positive" if kpis['roi'] > 0 else "negative")

st.markdown("---")

col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("🔻 Marketing Conversion Funnel")
    st.caption("Stage-by-stage drop-off from initial dispatch to enterprise commercial conversion.")
    
    funnel_stages = ["1. Dispatched", "2. Delivered", "3. Opened", "4. Clicked", "5. Converted"]
    funnel_values = [
        kpis["total_dispatched"],
        kpis["delivered"],
        kpis["unique_opens"],
        kpis["unique_clicks"],
        kpis["conversions"]
    ]
    
    fig_funnel = go.Figure(go.Funnel(
        y=funnel_stages,
        x=funnel_values,
        textinfo="value+percent previous+percent initial",
        marker={"color": ["#1E3A8A", "#2563EB", "#3B82F6", "#60A5FA", "#10B981"]},
        connector={"line": {"color": "#CBD5E1", "width": 1.5}}
    ))
    fig_funnel.update_layout(
        margin=dict(l=20, r=20, t=20, b=20),
        height=380,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig_funnel, use_container_width=True)

with col_right:
    st.subheader("📊 Open Rate & CTR by Campaign Type")
    st.caption("Benchmarking engagement rates across promotional, educational, and transactional formats.")
    
    if "campaign_type" in df.columns:
        type_summary = df.groupby("campaign_type").apply(
            lambda g: pd.Series({
                "Delivered": (g["delivery_status"] == "Delivered").sum(),
                "Opens": g["is_opened"].sum(),
                "Clicks": g["is_clicked"].sum(),
                "Open Rate (%)": round((g["is_opened"].sum() / max(1, (g["delivery_status"] == "Delivered").sum())) * 100, 2),
                "CTR (%)": round((g["is_clicked"].sum() / max(1, (g["delivery_status"] == "Delivered").sum())) * 100, 2)
            })
        ).reset_index().sort_values(by="Open Rate (%)", ascending=True)

        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            y=type_summary["campaign_type"],
            x=type_summary["Open Rate (%)"],
            name="Open Rate (%)",
            orientation="h",
            marker=dict(color="#1E3A8A")
        ))
        fig_bar.add_trace(go.Bar(
            y=type_summary["campaign_type"],
            x=type_summary["CTR (%)"],
            name="CTR (%)",
            orientation="h",
            marker=dict(color="#10B981")
        ))
        fig_bar.update_layout(
            barmode="group",
            margin=dict(l=20, r=20, t=20, b=20),
            height=380,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("---")

# Campaign Performance Leaderboard Table
st.subheader("🏆 Campaign Performance Leaderboard")
st.caption("Filtered campaign summary ranked by attributed revenue and commercial impact.")

if "campaign_name" in df.columns:
    camp_summary = df.groupby(["campaign_name", "campaign_type"]).apply(
        lambda g: pd.Series({
            "Dispatched": len(g),
            "Delivered": (g["delivery_status"] == "Delivered").sum(),
            "Opens": int(g["is_opened"].sum()),
            "Open Rate (%)": round((g["is_opened"].sum() / max(1, (g["delivery_status"] == "Delivered").sum())) * 100, 2),
            "Clicks": int(g["is_clicked"].sum()),
            "CTR (%)": round((g["is_clicked"].sum() / max(1, (g["delivery_status"] == "Delivered").sum())) * 100, 2),
            "Conversions": int(g["is_converted"].sum()),
            "Revenue ($)": round(g["conversion_revenue"].fillna(0).sum(), 2)
        })
    ).reset_index().sort_values(by="Revenue ($)", ascending=False)

    st.dataframe(
        camp_summary.style.format({
            "Dispatched": "{:,}",
            "Delivered": "{:,}",
            "Opens": "{:,}",
            "Open Rate (%)": "{:.2f}%",
            "Clicks": "{:,}",
            "CTR (%)": "{:.2f}%",
            "Conversions": "{:,}",
            "Revenue ($)": "${:,.2f}"
        }),
        use_container_width=True,
        hide_index=True
    )
    
    # Download filtered summary
    csv_data = camp_summary.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Campaign Performance Leaderboard (CSV)",
        data=csv_data,
        file_name="nexura_campaign_leaderboard.csv",
        mime="text/csv"
    )

st.markdown("---")
render_insight_box(
    title="Executive Optimization Takeaway",
    message=f"The conversion funnel reveals that {kpis['open_rate']}% of delivered recipients open emails, but only {kpis['ctor']}% of openers click through (CTOR). Increasing CTA contrast and personalization can dramatically lift pipeline conversions.",
    level="tip"
)
