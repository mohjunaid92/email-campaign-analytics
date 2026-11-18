"""
Screen 03: Campaign Performance Benchmarking & Deep Comparison (UI-03)
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
from src.metrics import calculate_cpa, calculate_roi
from src.ui import render_tailwind_header, render_insight_box

st.set_page_config(page_title="Campaign Compare | Nexura", page_icon="⚖️", layout="wide")

# Retrieve filtered data or load fresh
if "active_filtered_df" in st.session_state and st.session_state["active_filtered_df"] is not None:
    df = st.session_state["active_filtered_df"]
else:
    raw_df = load_joined_data()
    df, _ = clean_campaign_data(raw_df)

render_tailwind_header(
    title="Campaign Benchmarking & Comparative Matrix",
    subtitle="Head-to-Head Multi-Vector Radar Benchmarking, Cost Efficiency & Revenue Attribution",
    badge_text="UI-03 • Comparison"
)

# Campaign Selector
available_campaigns = sorted(list(df["campaign_name"].dropna().unique()))
default_campaigns = available_campaigns[:3] if len(available_campaigns) >= 3 else available_campaigns

selected_camps = st.multiselect(
    "Select 2 to 5 Campaigns for Head-to-Head Benchmarking:",
    options=available_campaigns,
    default=default_campaigns,
    max_selections=5
)

if len(selected_camps) < 2:
    st.warning("⚠️ Please select at least 2 campaigns from the selector above to generate comparison charts.")
else:
    comp_df = df[df["campaign_name"].isin(selected_camps)]
    
    # Compute metrics per selected campaign
    metrics_list = []
    for c_name in selected_camps:
        sub = comp_df[comp_df["campaign_name"] == c_name]
        dispatched = len(sub)
        delivered = int((sub["delivery_status"] == "Delivered").sum())
        opens = int(sub["is_opened"].sum())
        clicks = int(sub["is_clicked"].sum())
        convs = int(sub["is_converted"].sum())
        
        deliv_rate = round((delivered / max(1, dispatched)) * 100, 2)
        open_rate = round((opens / max(1, delivered)) * 100, 2)
        ctr = round((clicks / max(1, delivered)) * 100, 2)
        ctor = round((clicks / max(1, opens)) * 100, 2) if opens > 0 else 0.0
        conv_rate = round((convs / max(1, delivered)) * 100, 2)
        
        cost = float(sub["campaign_budget"].iloc[0]) if "campaign_budget" in sub.columns and len(sub) > 0 else 1000.0
        rev = float(sub["conversion_revenue"].fillna(0).sum())
        cpa = calculate_cpa(cost, convs)
        roi = calculate_roi(rev, cost)
        
        metrics_list.append({
            "Campaign": c_name,
            "Dispatched": dispatched,
            "Delivered": delivered,
            "Delivery Rate (%)": deliv_rate,
            "Opens": opens,
            "Open Rate (%)": open_rate,
            "Clicks": clicks,
            "CTR (%)": ctr,
            "CTOR (%)": ctor,
            "Conversions": convs,
            "Conversion Rate (%)": conv_rate,
            "Budget ($)": cost,
            "Revenue ($)": rev,
            "CPA ($)": cpa,
            "ROI (%)": roi
        })

    comp_summary = pd.DataFrame(metrics_list)

    col_radar, col_scatter = st.columns([1, 1])

    with col_radar:
        st.subheader("🕸️ Multi-Vector Radar Performance")
        st.caption("Normalised multi-dimensional profile comparing core efficiency ratios.")
        
        radar_categories = ["Delivery Rate (%)", "Open Rate (%)", "CTR (%)", "CTOR (%)", "Conversion Rate (%)"]
        palette = ["#1E3A8A", "#10B981", "#F59E0B", "#8B5CF6", "#EC4899"]
        
        fig_radar = go.Figure()
        for idx, row in comp_summary.iterrows():
            values = [row[c] for c in radar_categories]
            # Close the polygon
            values.append(values[0])
            cats_closed = radar_categories + [radar_categories[0]]
            
            fig_radar.add_trace(go.Scatterpolar(
                r=values,
                theta=cats_closed,
                fill="toself",
                fillcolor=f"rgba{tuple(list(int(palette[idx % len(palette)].lstrip('#')[i:i+2], 16) for i in (0, 2, 4)) + [0.2])}",
                line=dict(color=palette[idx % len(palette)], width=2),
                name=row["Campaign"]
            ))

        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, max(40, comp_summary["Open Rate (%)"].max() + 10)])
            ),
            margin=dict(l=30, r=30, t=20, b=20),
            height=380,
            paper_bgcolor="rgba(0,0,0,0)",
            legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    with col_scatter:
        st.subheader("💰 CPA vs. Attributed Revenue")
        st.caption("Cost efficiency frontier: Lower CPA and higher Revenue represent peak efficiency.")
        
        fig_scatter = px.scatter(
            comp_summary,
            x="CPA ($)",
            y="Revenue ($)",
            size="Dispatched",
            color="Campaign",
            text="Campaign",
            color_discrete_sequence=palette
        )
        fig_scatter.update_traces(textposition="top center", marker=dict(sizemin=14))
        fig_scatter.update_layout(
            margin=dict(l=20, r=20, t=20, b=20),
            height=380,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            showlegend=False
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    st.markdown("---")
    st.subheader("📋 Side-by-Side Metric Comparison Table")
    st.dataframe(
        comp_summary.style.format({
            "Dispatched": "{:,}",
            "Delivered": "{:,}",
            "Delivery Rate (%)": "{:.2f}%",
            "Opens": "{:,}",
            "Open Rate (%)": "{:.2f}%",
            "Clicks": "{:,}",
            "CTR (%)": "{:.2f}%",
            "CTOR (%)": "{:.2f}%",
            "Conversions": "{:,}",
            "Conversion Rate (%)": "{:.2f}%",
            "Budget ($)": "${:,.2f}",
            "Revenue ($)": "${:,.2f}",
            "CPA ($)": "${:,.2f}",
            "ROI (%)": "{:.2f}%"
        }),
        use_container_width=True,
        hide_index=True
    )

    # Top winner insight
    best_cpa_camp = comp_summary.sort_values(by="CPA ($)").iloc[0]
    best_rev_camp = comp_summary.sort_values(by="Revenue ($)", ascending=False).iloc[0]

    st.markdown("---")
    render_insight_box(
        title="Comparative Synthesis & Budget Allocation",
        message=f"**{best_rev_camp['Campaign']}** achieved maximum top-line revenue (${best_rev_camp['Revenue ($)']:,.2f}), while **{best_cpa_camp['Campaign']}** demonstrated peak acquisition cost efficiency at ${best_cpa_camp['CPA ($)']:.2f} CPA. Combining their copywriting and targeting frameworks is recommended for next quarter's playbook.",
        level="tip"
    )
