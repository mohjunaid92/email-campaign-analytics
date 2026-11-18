"""
Tailwind UI Components Engine for Streamlit
Project: Email Campaign Effectiveness Analysis
Author: Moh Junaid (Roll: 250320140094), MCA 2nd Year (DA), ABES
Target: Embeds modern Tailwind CSS components inside Streamlit via sandboxed iframes.
"""

import streamlit.components.v1 as components

def render_hero_header(title: str, subtitle: str, badge_text: str = "Enterprise Live"):
    """
    Renders an executive hero header with Tailwind CSS gradients and pill badge.
    """
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            body {{ margin: 0; padding: 0; background-color: transparent; }}
        </style>
    </head>
    <body>
        <div class="px-6 py-5 bg-gradient-to-r from-blue-900 via-indigo-900 to-slate-900 rounded-2xl shadow-md text-white font-sans flex flex-col md:flex-row justify-between items-start md:items-center gap-3 border border-slate-700/50">
            <div>
                <div class="flex items-center gap-2">
                    <span class="inline-block w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse"></span>
                    <h1 class="text-xl md:text-2xl font-bold tracking-tight text-white">{title}</h1>
                </div>
                <p class="text-blue-200/90 text-xs md:text-sm mt-1">{subtitle}</p>
            </div>
            <div class="flex items-center gap-2">
                <span class="bg-blue-800/80 text-blue-200 text-xs px-3 py-1.5 rounded-full border border-blue-400/30 font-semibold tracking-wide">
                    {badge_text}
                </span>
            </div>
        </div>
    </body>
    </html>
    """
    components.html(html_code, height=95)

def render_tailwind_header(title: str, subtitle: str, badge_text: str = "Enterprise Live"):
    """Alias for render_hero_header matching BUILD-05 specifications."""
    render_hero_header(title, subtitle, badge_text)

def render_kpi_card(title: str, value: str, delta: str = None, status: str = "positive"):
    """
    Renders a modern executive metric card with status color pill and sub-text delta.
    status: 'positive', 'negative', 'neutral', 'warning'
    """
    status_colors = {
        "positive": ("text-emerald-700", "bg-emerald-50", "border-emerald-200", "▲"),
        "negative": ("text-rose-700", "bg-rose-50", "border-rose-200", "▼"),
        "warning": ("text-amber-700", "bg-amber-50", "border-amber-200", "●"),
        "neutral": ("text-blue-700", "bg-blue-50", "border-blue-200", "■")
    }
    
    txt_col, bg_col, bdr_col, icon = status_colors.get(status, status_colors["neutral"])
    delta_html = ""
    if delta:
        delta_html = f"""
        <div class="flex items-center gap-1.5 mt-2">
            <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-semibold {bg_col} {txt_col} border {bdr_col}">
                {icon} {delta}
            </span>
            <span class="text-xs text-slate-400">vs target</span>
        </div>
        """

    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            body {{ margin: 0; padding: 0; background-color: transparent; }}
        </style>
    </head>
    <body>
        <div class="p-4 bg-white rounded-xl shadow-sm border border-slate-200 font-sans hover:shadow-md transition-shadow duration-200">
            <p class="text-xs font-semibold tracking-wider text-slate-500 uppercase">{title}</p>
            <h2 class="text-2xl font-extrabold text-slate-900 mt-1 tracking-tight">{value}</h2>
            {delta_html}
        </div>
    </body>
    </html>
    """
    components.html(html_code, height=110)

def render_tailwind_kpi_card(title: str, value: str, change_pct: str = None, subtext: str = "vs benchmark", icon_name: str = "trend"):
    """
    Tailwind KPI card supporting explicit change percentage and subtext.
    """
    status = "positive"
    if change_pct:
        if str(change_pct).startswith("-"):
            status = "negative"
        elif str(change_pct).startswith("+") or str(change_pct).replace("%","").replace(".","").isdigit():
            status = "positive"
        else:
            status = "neutral"
    render_kpi_card(title=title, value=value, delta=change_pct, status=status)

def render_insight_box(title: str, message: str, level: str = "info"):
    """
    Renders an analytical insight callout banner.
    level: 'info', 'warning', 'success', 'tip'
    """
    palette = {
        "info": ("from-blue-50 to-indigo-50", "border-blue-300", "text-blue-900", "text-blue-700", "ℹ"),
        "tip": ("from-emerald-50 to-teal-50", "border-emerald-300", "text-emerald-900", "text-emerald-700", "💡"),
        "warning": ("from-amber-50 to-yellow-50", "border-amber-300", "text-amber-900", "text-amber-700", "⚠"),
        "success": ("from-emerald-50 to-green-50", "border-emerald-300", "text-emerald-900", "text-emerald-700", "✓")
    }
    bg, bdr, h_col, p_col, icon = palette.get(level, palette["info"])
    
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            body {{ margin: 0; padding: 0; background-color: transparent; }}
        </style>
    </head>
    <body>
        <div class="p-4 bg-gradient-to-r {bg} border-l-4 {bdr} rounded-r-xl shadow-sm font-sans">
            <div class="flex items-center gap-2">
                <span class="text-base font-bold">{icon}</span>
                <h4 class="text-sm font-bold {h_col}">{title}</h4>
            </div>
            <p class="text-xs {p_col} mt-1 leading-relaxed">{message}</p>
        </div>
    </body>
    </html>
    """
    components.html(html_code, height=90)

def render_insight_callout(text: str, kind: str = "tip"):
    """Alias for render_insight_box matching BUILD-05 specifications."""
    title_map = {"tip": "Actionable Marketing Recommendation", "warning": "Deliverability Risk Warning", "info": "Key Analytical Finding"}
    title = title_map.get(kind, "Insight Callout")
    render_insight_box(title, text, level=kind)
