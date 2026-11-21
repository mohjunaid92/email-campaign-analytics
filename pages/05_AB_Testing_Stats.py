"""
Screen 05: A/B Testing & Statistical Hypothesis Lab (UI-05)
Project: Email Campaign Effectiveness Analysis
Author: Moh Junaid (Roll: 2500320140094), MCA 2nd Year (DA), ABES
Target Org: Nexura Tech Solutions Pvt. Ltd., Noida
"""

import streamlit as st
import pandas as pd
import numpy as np
from scipy import stats
import plotly.graph_objects as go
from src.data_loader import load_joined_data
from src.data_cleaner import clean_campaign_data
from src.statistics import two_proportion_z_test
from src.ui import render_tailwind_header, render_kpi_card, render_insight_box

st.set_page_config(page_title="A/B Testing Stats | Nexura", page_icon="🧪", layout="wide")

# Retrieve filtered data or load fresh
if "active_filtered_df" in st.session_state and st.session_state["active_filtered_df"] is not None:
    df = st.session_state["active_filtered_df"]
else:
    raw_df = load_joined_data()
    df, _ = clean_campaign_data(raw_df)

render_tailwind_header(
    title="A/B Testing & Statistical Hypothesis Lab",
    subtitle="Two-Sample Pooled Z-Test, P-Value Inference Engine & Normal Distribution Curve",
    badge_text="UI-05 • Statistics"
)

st.markdown("### 🔬 Hypothesis Formulation & Experiment Selection")
st.write(r"**Null Hypothesis ($H_0$):** $p_A = p_B$ (There is no true difference in engagement rates between Variant A and Variant B)")
st.write(r"**Alternative Hypothesis ($H_1$):** $p_A \ne p_B$ (Two-tailed difference in engagement rates)")

campaigns = sorted(list(df["campaign_name"].dropna().unique()))
camp_a_default = campaigns[0] if len(campaigns) > 0 else None
camp_b_default = campaigns[1] if len(campaigns) > 1 else camp_a_default

col_ctrl, col_test = st.columns(2)
with col_ctrl:
    camp_a = st.selectbox("Select Variant A (Control)", options=campaigns, index=0)
with col_test:
    camp_b = st.selectbox("Select Variant B (Treatment)", options=campaigns, index=1 if len(campaigns) > 1 else 0)

col_metric, col_alpha = st.columns(2)
with col_metric:
    metric_choice = st.radio("Experiment Conversion Goal", options=["Open Rate", "Conversion Rate"], horizontal=True)
with col_alpha:
    alpha = st.select_slider("Significance Level (α)", options=[0.01, 0.05, 0.10], value=0.05)

# Extract counts from data
df_a = df[df["campaign_name"] == camp_a]
df_b = df[df["campaign_name"] == camp_b]

n1 = max(1, int((df_a["delivery_status"] == "Delivered").sum()))
n2 = max(1, int((df_b["delivery_status"] == "Delivered").sum()))

if metric_choice == "Open Rate":
    k1 = int(df_a["is_opened"].sum())
    k2 = int(df_b["is_opened"].sum())
else:
    k1 = int(df_a["is_converted"].sum())
    k2 = int(df_b["is_converted"].sum())

# Run Z-Test
z_res = two_proportion_z_test(k1=k1, n1=n1, k2=k2, n2=n2, alpha=alpha)

st.markdown("---")
st.subheader("📊 Statistical Test Results")

c1, c2, c3, c4 = st.columns(4)
with c1:
    render_kpi_card(f"Variant A ({metric_choice})", f"{z_res['variant_1_proportion']*100:.1f}%", f"{k1}/{n1} successes", "neutral")
with c2:
    render_kpi_card(f"Variant B ({metric_choice})", f"{z_res['variant_2_proportion']*100:.1f}%", f"{k2}/{n2} successes", "neutral")
with c3:
    render_kpi_card("Z-Score Statistic", f"{z_res['z_score']:.3f}", f"Critical: ±{stats.norm.ppf(1 - alpha/2):.2f}", "positive" if z_res['is_significant'] else "warning")
with c4:
    render_kpi_card("P-Value", f"{z_res['p_value']:.4f}", f"Threshold α = {alpha}", "positive" if z_res['is_significant'] else "negative")

# Decision Callout
if z_res["is_significant"]:
    st.success(f"🎉 **Statistically Significant Result (p = {z_res['p_value']:.4f} < {alpha})**: We reject the null hypothesis $H_0$. The observed performance delta of {abs(z_res['proportion_difference'])*100:.2f}% is statistically significant at the {(1-alpha)*100:.0f}% confidence level.")
else:
    st.info(f"⚖️ **Inconclusive Result (p = {z_res['p_value']:.4f} ≥ {alpha})**: We fail to reject the null hypothesis $H_0$. The observed delta of {abs(z_res['proportion_difference'])*100:.2f}% could be attributed to random sampling variation. Additional sample size is recommended.")

st.markdown("---")

# Bell Curve Distribution
st.subheader("🔔 Standard Normal Distribution & Critical Rejection Regions")
st.caption("Visualizing the test statistic against the standard Gaussian bell curve.")

x = np.linspace(-4, 4, 500)
y = stats.norm.pdf(x, 0, 1)
z_crit = stats.norm.ppf(1 - alpha / 2)

fig_bell = go.Figure()

# Base bell curve
fig_bell.add_trace(go.Scatter(x=x, y=y, mode="lines", line=dict(color="#1E3A8A", width=2.5), name="N(0, 1) Distribution"))

# Left Rejection Region
x_left = x[x <= -z_crit]
y_left = y[x <= -z_crit]
fig_bell.add_trace(go.Scatter(x=np.concatenate([[x_left[0]], x_left, [x_left[-1]]]),
                              y=np.concatenate([[0], y_left, [0]]),
                              fill="toself", fillcolor="rgba(239, 68, 68, 0.3)",
                              line=dict(color="rgba(239, 68, 68, 0)"), name="Rejection Zone (α/2)"))

# Right Rejection Region
x_right = x[x >= z_crit]
y_right = y[x >= z_crit]
fig_bell.add_trace(go.Scatter(x=np.concatenate([[x_right[0]], x_right, [x_right[-1]]]),
                               y=np.concatenate([[0], y_right, [0]]),
                               fill="toself", fillcolor="rgba(239, 68, 68, 0.3)",
                               line=dict(color="rgba(239, 68, 68, 0)"), showlegend=False))

# Observed Z line
fig_bell.add_vline(x=z_res["z_score"], line_dash="dash", line_color="#10B981" if z_res["is_significant"] else "#F59E0B",
                   annotation_text=f"Observed Z = {z_res['z_score']:.2f}", annotation_position="top")

fig_bell.update_layout(
    margin=dict(l=20, r=20, t=20, b=20),
    height=340,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(title="Z-Score (Standard Deviations)", range=[-4, 4]),
    yaxis=dict(title="Probability Density", showgrid=False),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)
st.plotly_chart(fig_bell, use_container_width=True)

st.markdown("---")
render_insight_box(
    title="A/B Testing Methodological Standard",
    message=f"95% Confidence Interval for True Difference: [{z_res['ci_lower']*100:.2f}%, {z_res['ci_upper']*100:.2f}%]. Sample size check: {'Sufficient (n >= 30 per group)' if z_res['is_valid_sample'] else 'Warning: Sample size underpowered'}. Experiments should reach at least 100 dispatches per variant before finalizing commercial budget allocations.",
    level="info"
)
