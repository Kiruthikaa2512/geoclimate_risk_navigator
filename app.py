# ===============================
# GeoClimate AI Command Center
# FULL FIXED SCRIPT — OPENAI FIXED FOR sk-proj KEYS
# ===============================

import os
import random
from datetime import date
from io import BytesIO
from typing import Optional, Dict, Any, List
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import requests


# ============================================
# UNIVERSAL OPENAI CLIENT — FIXED FOR sk-proj
# ============================================

# ============================================
# FREE AI PROVIDERS - NO API KEYS NEEDED
# ============================================

# ============================================
# FREE AI PROVIDERS - NO API KEYS NEEDED
# ============================================

def ai_call(system_prompt: str, user_prompt: str, temperature: float = 0.4):
    """
    Free AI using smart mock responses - no API keys required
    """
    return generate_mock_response(system_prompt, user_prompt)

def generate_mock_response(system_prompt: str, user_prompt: str) -> str:
    """
    Heuristic / rule-based 'AI' brain for the app.
    - Uses session_state context when available
    - Handles route explanations, scenarios, optimizer, and free-form strategy Q&A
    - No external API calls
    """
    lower = user_prompt.lower()

    # ---- Pull context from the app ----
    route = st.session_state.get("last_route")
    risks = st.session_state.get("last_risks")
    scenario = st.session_state.get("scenario")
    options = st.session_state.get("optimizer_options")

    context_block = ""
    if route and risks:
        context_block += (
            f"\n\n**Current lane in tool:** "
            f"{route['origin']} → {route['dest']} via {route['mode'].upper()} "
            f"(overall risk {risks['overall']}/100)"
        )
    if scenario:
        context_block += "\n\n**Scenario context:** " + str(scenario)
    if options:
        context_block += f"\n\n**Network options configured:** {len(options)} alternatives."

    # ---- Helpers ----
    def detect_countries(text: str):
        t = text.lower()
        hits = []
        for c in COUNTRY_LIST:
            if c.lower() in t:
                hits.append(c)
        # preserve order, unique
        return list(dict.fromkeys(hits))

    def describe_dominant_risks(r: dict) -> list[str]:
        dims = [
            ("Geopolitics", r["geopolitical"]),
            ("Climate", r["climate"]),
            ("Logistics", r["logistics"]),
            ("Cyber", r["cyber"]),
        ]
        dims.sort(key=lambda x: x[1], reverse=True)
        lines = []
        for name, val in dims[:3]:
            if name == "Geopolitics":
                driver = "geopolitical tensions, regulatory shifts or sanctions exposure"
            elif name == "Climate":
                driver = "weather volatility, storms, flooding and seasonal disruption"
            elif name == "Logistics":
                driver = "port congestion, infrastructure bottlenecks and capacity constraints"
            else:
                driver = "data security, ransomware and technology dependencies"
            lines.append(f"- **{name} ({val}/100)** — driven by {driver}.")
        return lines

    # ---- 1) EXPLAIN ROUTE (used by Route Analyzer 'Explain with AI') ----
    if "route:" in lower and "scores:" in lower and route and risks:
        lines = []
        lines.append(
            f"**🌍 Lane Intelligence: {route['origin']} → {route['dest']} ({route['mode'].upper()})**"
        )
        lines.append("")
        lines.append(
            f"- **Overall risk:** **{risks['overall']}/100** "
            f"({risk_level(risks['overall'])} band)"
        )
        lines.append(
            f"- **Breakdown:** Geo {risks['geopolitical']}, "
            f"Climate {risks['climate']}, Logistics {risks['logistics']}, "
            f"Cyber {risks['cyber']}."
        )
        lines.append("")

        lines.append("**Top risk drivers for this lane:**")
        lines.extend(describe_dominant_risks(risks))
        lines.append("")

        # Mode-specific commentary
        mode = route["mode"]
        if mode == "sea":
            lines.append(
                "- **Sea freight notes:** Sensitive to port congestion, maritime chokepoints "
                "(e.g. Suez, Red Sea) and seasonal storms along the route."
            )
        elif mode == "air":
            lines.append(
                "- **Air freight notes:** Reduces logistics and climate exposure but increases cost; "
                "capacity and belly-space constraints can still create volatility."
            )
        elif mode == "road":
            lines.append(
                "- **Road freight notes:** Flexible rerouting is possible, but vulnerable to "
                "border queues, regulatory checks and road infrastructure quality."
            )
        elif mode == "rail":
            lines.append(
                "- **Rail notes:** Typically stable schedules and lower weather sensitivity, "
                "but slower to reroute during disruption."
            )

        # Mitigation guidance
        lines.append("")
        lines.append("**Mitigation playbook:**")
        lines.append("- Design a **primary lane** and at least one **pre-agreed fallback route**.")
        lines.append("- Align **incoterms, SLAs and insurance** with the current risk level.")
        lines.append("- Implement **lane-level monitoring** (ports, borders, weather, cyber).")
        lines.append(
            "- Use **multi-modal combinations** (e.g. sea + air, rail + truck) for critical flows."
        )

        if context_block:
            lines.append(context_block)

        return "\n".join(lines)

    # ---- 2) SAFEST MODE BETWEEN TWO COUNTRIES (e.g. India ↔ USA) ----
    countries_mentioned = detect_countries(user_prompt)
    origin = dest = None
    if len(countries_mentioned) >= 2:
        origin, dest = countries_mentioned[0], countries_mentioned[1]
    elif route:
        origin, dest = route["origin"], route["dest"]

    safe_words = ["safe", "safest", "lower risk", "least risk", "secure"]
    mode_words = ["mode", "air", "sea", "ocean", "ship", "road", "truck", "rail", "freight"]

    is_safety_question = any(w in lower for w in safe_words) and any(
        w in lower for w in mode_words
    )

    if is_safety_question and origin and dest:
        # Compare modes using your risk model
        today = date.today()
        mode_results = []
        for m in ["sea", "air", "road", "rail"]:
            r = compute_route_risk(origin, dest, m, today, "Balanced", True)
            mode_results.append((m, r["overall"], r))

        mode_results.sort(key=lambda x: x[1])  # lower = safer
        best_mode, best_score, best_risks = mode_results[0]

        lines = []
        lines.append(f"**🧭 Safety-Focused Mode Comparison: {origin} → {dest}**")
        lines.append("")
        lines.append("**Mode ranking (lower score = safer):**")
        for m, score, r in mode_results:
            lines.append(
                f"- **{m.upper()}** → overall risk **{score}/100** "
                f"(Geo {r['geopolitical']}, Climate {r['climate']}, "
                f"Logistics {r['logistics']}, Cyber {r['cyber']})"
            )

        lines.append("")
        lines.append(
            f"**Recommended primary mode for safety:** **{best_mode.upper()}** "
            f"with modeled risk **{best_score}/100**."
        )

        # Reasoning by mode
        reason = []
        if best_mode == "air":
            reason.append("avoids the most volatile maritime chokepoints and port queues")
            reason.append("reduces exposure to multi-week ocean storms and congestion")
            reason.append("offers tighter transit-time control for critical cargo")
        elif best_mode == "sea":
            reason.append("is cost-efficient for large volumes, enabling diversified routings")
            reason.append("can be shifted across different ports and carriers when disruption hits")
        elif best_mode == "road":
            reason.append("works best for regional corridors with flexible rerouting options")
        elif best_mode == "rail":
            reason.append("benefits from relatively stable timetables and lower weather sensitivity")

        if reason:
            lines.append("**Why this mode wins for safety:**")
            lines.extend([f"- {r}" for r in reason])

        lines.append("")
        lines.append("**Practical playbook:**")
        lines.append("- Use the safest mode for high-value or time-critical flows.")
        lines.append("- Keep a secondary mode contracted as a contingency option.")
        lines.append("- Align insurance, SLAs and monitoring with the chosen risk profile.")

        if context_block:
            lines.append(context_block)

        return "\n".join(lines)

    # ---- 3) SCENARIO LAB EXPLANATION (Base=..., Stressed=...) ----
    if "base=" in lower and "stressed=" in lower:
        lines = []
        lines.append("**📊 Scenario Lab – Stress Test Interpretation**")
        lines.append("")
        lines.append(
            "- The stressed scenario increases one or more risk dimensions versus the base case."
        )
        lines.append(
            "- Focus on where the **percentage change** is greatest (often Climate or Logistics)."
        )
        lines.append("")
        lines.append("**How to read it:**")
        lines.append(
            "- If **Climate** jumps strongly, treat the lane as more sensitive to storms, floods "
            "or heatwaves — adjust schedules and inventory buffers accordingly."
        )
        lines.append(
            "- If **Logistics** spikes, assume port, terminal or carrier disruptions — prepare "
            "alternative routings and backup capacity."
        )
        lines.append(
            "- If **Geopolitics** rises, revisit sanctions, export controls and regulatory checks."
        )
        lines.append(
            "- If **Cyber** rises, review TMS/WMS, partners’ security posture and incident response."
        )
        lines.append("")
        lines.append("**Resilience actions under stress:**")
        lines.append("- Build in additional lead-time for the stressed scenario.")
        lines.append("- Increase safety stock or strategic buffers at key nodes.")
        lines.append("- Pre-negotiate alternative carriers, ports and modes.")
        lines.append("- Run playbooks for extreme but plausible disruptions.")

        if context_block:
            lines.append(context_block)

        return "\n".join(lines)

    # ---- 4) ROUTE COMPARISON (Compare these routes: ...) ----
    if "compare these routes" in lower or "lane" in lower and "overall" in lower:
        lines = []
        lines.append("**🔄 Multi-Route Comparison & Recommendation**")
        lines.append("")
        lines.append(
            "- Prefer lanes with **lower overall risk** where service and cost are acceptable."
        )
        lines.append(
            "- When routes have similar overall risk, choose the one with **lower Logistics and "
            "Climate scores**, as these tend to drive day-to-day disruption."
        )
        lines.append("")
        lines.append("**Typical trade-off logic:**")
        lines.append("- Air vs Sea: air is safer for time-critical freight; sea wins on cost.")
        lines.append(
            "- Europe vs Asia origin: European origins often bring lower geopolitical volatility "
            "but may have longer transit and higher cost."
        )
        lines.append(
            "- Singapore / Netherlands hubs: frequently provide more resilient infrastructure and "
            "cyber posture than regional alternatives."
        )
        lines.append("")
        lines.append(
            "Use low-risk routes for your **core, high-volume flows**, and keep a small share on "
            "alternative lanes to preserve agility."
        )

        if context_block:
            lines.append(context_block)

        return "\n".join(lines)

    # ---- 5) NETWORK OPTIMIZER EXPLANATION (Options=..., Advise best choice) ----
    if "options=" in lower and "advise best choice" in lower:
        lines = []
        lines.append("**🎯 Network Optimizer – Recommended Configuration**")
        lines.append("")
        lines.append(
            "- Select as your **primary option** the lane with the **lowest overall risk** that "
            "still meets service and cost constraints."
        )
        lines.append(
            "- Use the **second-best option** as a formal, contracted contingency with "
            "pre-defined triggers (e.g. corridor closure, war-risk premiums, major port outage)."
        )
        lines.append("")
        lines.append("**Design principles:**")
        lines.append("- Avoid concentration in a single corridor or single port cluster.")
        lines.append("- Mix geographies (e.g. Europe + Asia hubs) to diversify geopolitical risk.")
        lines.append("- Combine modes (sea + air, rail + truck) for strategic SKUs.")
        lines.append("- Align your sourcing strategy with the chosen network lanes.")

        if context_block:
            lines.append(context_block)

        return "\n".join(lines)

    # ---- 6) GENERAL STRATEGY QUESTIONS (AI Strategy Room) ----
    if "?" in user_prompt or "strategy" in lower or "plan" in lower:
        lines = []
        lines.append("**🤖 Strategic Advisory Response**")
        lines.append("")
        lines.append("**1. Situation framing**")
        if origin and dest:
            lines.append(
                f"- You are moving freight between **{origin}** and **{dest}**, combining "
                "geopolitical, climate, logistics and cyber risks."
            )
        else:
            lines.append(
                "- You are balancing service, cost and risk across a multi-country supply network."
            )
        if route and risks:
            lines.append(
                f"- Current lane in focus: **{route['origin']} → {route['dest']} "
                f"({route['mode'].upper()})**, overall risk **{risks['overall']}/100**."
            )

        lines.append("")
        lines.append("**2. Immediate priorities (0–3 months)**")
        lines.append("- Identify your **top 5 critical lanes** by value and service sensitivity.")
        lines.append("- For each, define a **primary route** and at least one **fallback lane**.")
        lines.append("- Tighten **cyber hygiene** for core logistics systems and partners.")
        lines.append(
            "- Adjust **sailing / flight windows** around known climate seasons (monsoon, hurricanes, typhoons)."
        )

        lines.append("")
        lines.append("**3. Medium-term moves (3–12 months)**")
        lines.append("- Stand up a **lane risk dashboard** with monthly geo/climate/logistics signals.")
        lines.append("- Build a **playbook library** for disruptions (port closure, strike, corridor conflict).")
        lines.append("- Pilot **multi-sourcing** and **multi-hub** strategies for key SKUs.")
        lines.append("- Introduce **predictive ETA and capacity monitoring** for high-risk lanes.")

        lines.append("")
        lines.append("**4. Long-term design (12+ months)**")
        lines.append("- Develop a **digital twin** of your end-to-end network for scenario simulation.")
        lines.append("- Align **sustainability, cost and resilience** targets per lane.")
        lines.append(
            "- Institutionalize a **cross-functional risk council** (Supply Chain, Finance, Risk, Commercial)."
        )

        if context_block:
            lines.append(context_block)

        return "\n".join(lines)

    # ---- 7) DEFAULT EXECUTIVE SUMMARY ----
    return """
**🌐 GeoClimate AI Command Center Analysis**

**Executive Summary**  
This assessment highlights multiple opportunities to improve resilience, cost and service across your global network. It considers geopolitics, climate, logistics and cyber risk as an integrated system.

**Key Insights**
- **Route diversification** can reduce disruption exposure by 25–40% on critical lanes.  
- **Climate-aware scheduling** (monsoon, hurricane, typhoon seasons) significantly improves on-time performance.  
- Strengthening **cyber security** for logistics platforms lowers the likelihood of high-impact outages.  

**Recommended Actions**
1. Identify your top risk-weighted lanes and define clear primary and backup routings.  
2. Use multi-modal options (sea + air, rail + truck) for high-value or time-critical flows.  
3. Implement monitoring of ports, corridors and weather to trigger pre-defined playbooks.  
4. Regularly review sourcing and network design as geopolitics and climate patterns evolve.  

Use the Route Analyzer, Scenario Lab and Network Optimizer together to turn this into a living,
adaptive supply chain design rather than a one-off study.
"""

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="GeoClimate AI – Command Center",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================
# THEME + FIXES
# ============================================================
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Sora:wght@600;700&display=swap');

:root {
    --primary: #4CAF7B;
    --primary-soft: #60C18C;
    --accent-warm: #F4A261;
    --accent-strong: #E76F51;
    --text: #1A1F25;
}

/* Background */
.stApp {
    background: linear-gradient(135deg,#F0FFF4 0%,#FFFFFF 55%,#FFECD1 100%);
    font-family: "Inter";
}

/* Card fix */
.gc-card {
    background: #fff;
    border-radius: 14px;
    border: 1px solid rgba(180,190,180,0.9);
    padding: 1rem 1.2rem;
    margin-bottom: .4rem;
    box-shadow: 0 12px 26px rgba(31,41,35,.12);
}

/* Fix blank bars */
.block-container > div:empty {
    display: none !important;
}

/* Fix metric cut-off */
div[data-testid="stMetric"]{
    padding:.6rem .8rem!important;
    background:#FFF!important;
    border-radius:12px!important;
    border:1px solid rgba(203,213,205,.95)!important;
    box-shadow:0 8px 18px rgba(148,163,154,.35)!important;
}

div[data-testid="stMetricLabel"]{font-size:.80rem!important; white-space:nowrap;}
div[data-testid="stMetricValue"]{font-size:1.10rem!important; white-space:nowrap;}

.gc-pill{
    display:inline-block;
    padding: .35rem 1.1rem;
    border-radius:999px;
    background:#FFF3E0;
    border:1px solid #F4A261;
    color:#9A3412;
    font-size:.78rem;
    letter-spacing:.14em;
    font-weight:600;
    white-space:nowrap;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# CONSTANTS
# ============================================================
PRIMARY = "#4CAF7B"
PRIMARY_SOFT = "#60C18C"
ACCENT = "#E76F51"
TEXT_MAIN = "#1F2933"
COLORWAY = [PRIMARY_SOFT, ACCENT, "#66BFBF", "#F4A261", "#2E7D32"]

# ============================================================
# RISK TABLES + COUNTRY DATA
# ============================================================

GEO_RISK = {
    "default": 35, "Ukraine": 90, "Russia": 85, "Israel": 80, "Gaza Strip": 92,
    "China": 60, "Taiwan": 70, "USA": 30, "Germany": 25,
    "UK": 25, "India": 40, "Brazil": 45, "South Africa": 40,
    "Australia": 35, "Bangladesh": 60, "Philippines": 60, "Pakistan": 55,
    "Singapore": 20, "Netherlands": 22, "Mexico": 45, "Canada": 20,
    "Japan": 25, "South Korea": 30,
}

CLIMATE_RISK = {
    "default": 40, "Bangladesh": 85, "Philippines": 80, "Pakistan": 75,
    "USA": 45, "India": 65, "Australia": 55, "Brazil": 50,
    "China": 45, "Japan": 40, "Mexico": 50,
}

LOGISTICS_RISK = {
    "default": 35, "USA": 50, "China": 55, "Singapore": 40,
    "Netherlands": 45, "Germany": 40, "UK": 45,
    "India": 50, "Brazil": 48, "South Africa": 50, "Mexico": 52,
}

CYBER_RISK = {
    "default": 40, "USA": 55, "European Union": 50, "China": 60,
    "India": 45, "Japan": 50, "Brazil": 42, "UK": 48,
}

COUNTRY_COORDS = {
    "USA": (37, -95), "China": (35, 103), "India": (21, 78), "Germany": (51, 10),
    "UK": (55, -3), "Brazil": (-10, -55), "South Africa": (-30, 25),
    "Australia": (-25, 133), "Bangladesh": (24, 90), "Philippines": (13, 122),
    "Pakistan": (30, 70), "Russia": (60, 90), "Ukraine": (49, 32),
    "Singapore": (1.3, 103.8), "Netherlands": (52.1, 5.3),
    "Israel": (31, 35), "Gaza Strip": (31.4, 34.3),
    "Mexico": (23, -102), "Canada": (56, -106),
    "Japan": (36.2, 138.2), "South Korea": (36.5, 127.8),
}

COUNTRY_LIST = sorted(COUNTRY_COORDS.keys())

CONFLICT_CORRIDORS = [
    {"name": "Red Sea / Gulf of Aden", "lat": 16.0, "lon": 43.0, "risk": 85},
    {"name": "Black Sea", "lat": 45.0, "lon": 35.0, "risk": 80},
    {"name": "Taiwan Strait", "lat": 24.0, "lon": 121.0, "risk": 75},
    {"name": "South China Sea", "lat": 12.0, "lon": 114.0, "risk": 70},
]

# ============================================================
# HELPERS
# ============================================================

def risk_level(s):
    if s < 25: return "Low"
    if s < 50: return "Moderate"
    if s < 75: return "High"
    return "Critical"

def risk_badge_class(s):
    lvl = risk_level(s)
    if lvl == "Low": return "risk-low"
    if lvl == "Moderate": return "risk-mod"
    return "risk-high"

def get_score(table, c):
    return table.get(c, table["default"])

def risk_color(score):
    score_norm = np.clip(score, 0, 100) / 100
    g = np.array([46,125,50])
    y = np.array([217,119,6])
    r = np.array([185,28,28])

    if score_norm < 0.5:
        t = score_norm * 2
        rgb = g + (y - g) * t
    else:
        t = (score_norm - 0.5) * 2
        rgb = y + (r - y) * t
    return f"rgb({int(rgb[0])},{int(rgb[1])},{int(rgb[2])})"


# ============================================================
# RISK COMPUTATION
# ============================================================

def compute_route_risk(origin, dest, mode, dep_date, weighting, include_conflict,
                       cargo_value=0.0, time_critical=False):

    if isinstance(dep_date, str):
        dep_date = date.fromisoformat(dep_date)

    g = (get_score(GEO_RISK, origin) + get_score(GEO_RISK, dest)) / 2
    c = (get_score(CLIMATE_RISK, origin) + get_score(CLIMATE_RISK, dest)) / 2
    l = (get_score(LOGISTICS_RISK, origin) + get_score(LOGISTICS_RISK, dest)) / 2
    cb = (get_score(CYBER_RISK, origin) + get_score(CYBER_RISK, dest)) / 2

    if mode == "sea":
        l *= 1.15
    elif mode == "air":
        l *= 0.9
        c *= 0.9
    elif mode == "road":
        l *= 1.1

    if dep_date.month in (6,7,8,9):
        c *= 1.15

    conflict_bump = 0
    if include_conflict and origin in {"Ukraine","Russia","Israel","Gaza Strip","Taiwan"}:
        conflict_bump = 10
        g *= 1.1

    if weighting == "Geo-heavy":
        w = [0.45,0.25,0.2,0.1]
    elif weighting == "Climate-heavy":
        w = [0.25,0.45,0.2,0.1]
    elif weighting == "Logistics-heavy":
        w = [0.25,0.2,0.45,0.1]
    else:
        w = [0.35,0.3,0.25,0.1]

    overall = g*w[0] + c*w[1] + l*w[2] + cb*w[3] + conflict_bump
    overall = float(np.clip(round(overall,1), 0, 100))

    return {
        "geopolitical": round(g,1),
        "climate": round(c,1),
        "logistics": round(l,1),
        "cyber": round(cb,1),
        "overall": overall,
        "conflict_bump": conflict_bump,
    }

# ============================================================
# VISUALS
# ============================================================

def style_fig(fig):
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#FFF",
        font=dict(color=TEXT_MAIN, family="Inter"),
        colorway=COLORWAY,
    )
    return fig

def build_route_map(origin, dest, overall, show_conflict):
    lat_o, lon_o = COUNTRY_COORDS[origin]
    lat_d, lon_d = COUNTRY_COORDS[dest]

    fig = go.Figure()
    fig.add_trace(go.Scattergeo(
        lon=[lon_o, lon_d], lat=[lat_o, lat_d],
        mode="lines", line=dict(width=4, color=risk_color(overall))
    ))
    fig.add_trace(go.Scattergeo(
        lon=[lon_o], lat=[lat_o],
        mode="markers+text", text=[origin], textposition="top center",
        marker=dict(size=11, color="#66BFBF")
    ))
    fig.add_trace(go.Scattergeo(
        lon=[lon_d], lat=[lat_d],
        mode="markers+text", text=[dest], textposition="bottom center",
        marker=dict(size=11, color="#B91C1C")
    ))

    if show_conflict:
        fig.add_trace(go.Scattergeo(
            lon=[c["lon"] for c in CONFLICT_CORRIDORS],
            lat=[c["lat"] for c in CONFLICT_CORRIDORS],
            mode="markers+text",
            text=[c["name"] for c in CONFLICT_CORRIDORS],
            marker=dict(color="red", symbol="triangle-up")
        ))

    fig.update_layout(
        geo=dict(
            projection_type="natural earth",
            showland=True, landcolor="#F4F5F7",
            showcountries=True, countrycolor="#999"
        ),
        margin=dict(l=0,r=0,t=0,b=0),
        height=420
    )
    return style_fig(fig)


def build_risk_radar(r):
    fig = go.Figure()
    labels = ["Geopolitics", "Climate", "Logistics", "Cyber"]
    values = [r["geopolitical"], r["climate"], r["logistics"], r["cyber"]]

    fig.add_trace(go.Scatterpolar(
        r=values+[values[0]],
        theta=labels+[labels[0]],
        fill="toself",
        line=dict(color=PRIMARY_SOFT)
    ))
    fig.update_layout(
        showlegend=False,
        margin=dict(l=30,r=30,t=20,b=20),
        height=360
    )
    return style_fig(fig)


def build_heatmap():
    rows = []
    for c in GEO_RISK:
        if c == "default": continue
        g = get_score(GEO_RISK, c)
        cl = get_score(CLIMATE_RISK, c)
        rows.append({"country": c, "risk": g*0.6 + cl*0.4})
    df = pd.DataFrame(rows)

    fig = px.choropleth(
        df, locations="country", locationmode="country names",
        color="risk", range_color=(0,100),
        color_continuous_scale=["#2E7D32","#D97706","#B91C1C"]
    )
    fig.update_layout(height=420, margin=dict(l=0,r=0,t=20,b=0))
    return style_fig(fig)

# ============================================================
# HERO
# ============================================================

def render_hero():
    st.markdown("""
    <div class="gc-hero gc-card">
        <div class="gc-hero-inner">
            <div class="gc-pill">GEOCLIMATE • SUPPLY CHAIN • COMMAND</div>
            <h1 style="margin-top:.7rem;margin-bottom:.3rem;">GeoClimate AI – Command Center</h1>
            <p style="font-size:.98rem;max-width:920px;margin-bottom:.2rem;color:#4B5563;">
                A nature-inspired control tower that scores global lanes across geopolitics,
                climate, logistics and cyber — then uses AI to simulate disruptions,
                compare alternatives and recommend network designs leaders can act on.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# CARD DECORATOR
# ============================================================

from contextlib import contextmanager

@contextmanager
def card(title=None):
    # Create a real Streamlit container
    container = st.container()
    with container:
        # Inject your styled card DIV
        st.markdown("<div class='gc-card'>", unsafe_allow_html=True)

        # Render the title if provided
        if title:
            st.markdown(f"<p class='tiny-label'>{title}</p>", unsafe_allow_html=True)

        # Create another internal container for widgets
        inner = st.container()
        with inner:
            yield  # ALL widgets live here (safe)

        # Close the HTML DIV
        st.markdown("</div>", unsafe_allow_html=True)




# ============================================================
# ROUTE ANALYZER
# ============================================================

def render_route_analyzer():
    col_left, col_right = st.columns([0.95,1.25])

    # -------------------- LEFT SIDE --------------------
    with col_left:
        with card("Route configuration"):
            origin = st.selectbox("Origin country", COUNTRY_LIST, index=COUNTRY_LIST.index("China"))
            dest = st.selectbox("Destination country", COUNTRY_LIST, index=COUNTRY_LIST.index("USA"))
            mode = st.selectbox("Mode", ["sea", "air", "road", "rail"])

            dep_date = st.date_input(
                "Departure date", value=date.today(),
                min_value=date(2020,1,1), max_value=date(2030,12,31)
            )

            with st.expander("Advanced", expanded=False):
                weighting = st.selectbox("Weighting", ["Balanced", "Geo-heavy", "Climate-heavy", "Logistics-heavy"])
                include_conflict = st.checkbox("Include conflict corridors", True)
                cargo_value = st.number_input("Cargo value (USD)", min_value=0.0, step=100000.0)
                time_critical = st.checkbox("Time-critical cargo", False)

            add_multi = st.checkbox("Add this lane to comparison basket", False)

            run = st.button("Run analysis", type="primary")

        if run:
            risks = compute_route_risk(origin, dest, mode, dep_date, weighting, include_conflict)

            st.session_state["last_route"] = {
                "origin": origin,
                "dest": dest,
                "mode": mode,
                "date": dep_date.isoformat(),
                "weighting": weighting,
                "conflict": include_conflict
            }
            st.session_state["last_risks"] = risks

            if add_multi:
                st.session_state.setdefault("multi_routes", []).append(
                    {**st.session_state["last_route"], "risks": risks}
                )

        with card("Lane snapshot"):
            r = st.session_state.get("last_route")
            rs = st.session_state.get("last_risks")

            if not r:
                st.info("Run a lane first.")
            else:
                c1, c2, c3 = st.columns(3)
                c1.metric("Lane", f"{r['origin']} → {r['dest']}")
                c2.metric("Mode", r["mode"].upper())
                c3.metric("Preset", r["weighting"])

                lvl = risk_level(rs["overall"])
                st.markdown(
                    f"<p>Overall risk: "
                    f"<span class='risk-badge {risk_badge_class(rs['overall'])}'>"
                    f"{lvl} ({rs['overall']})</span></p>",
                    unsafe_allow_html=True
                )

                colx, coly = st.columns(2)
                colx.metric("Geopolitics", rs["geopolitical"])
                coly.metric("Climate", rs["climate"])
                colx, coly = st.columns(2)
                colx.metric("Logistics", rs["logistics"])
                coly.metric("Cyber", rs["cyber"])

        with card():
            st.markdown('<div class="ai-badge">AI explanation</div>', unsafe_allow_html=True)
            r = st.session_state.get("last_route")
            rs = st.session_state.get("last_risks")

            if r and rs:
                if st.button("Explain with AI", key="explain_route"):
                    prompt = f"""
Route: {r["origin"]} → {r["dest"]} via {r["mode"].upper()}
Scores: Geo={rs['geopolitical']}, Climate={rs['climate']},
Logistics={rs['logistics']}, Cyber={rs['cyber']}, Overall={rs['overall']}
Explain top drivers and mitigations.
"""
                    st.markdown(ai_call("You are a supply chain advisor.", prompt))
            else:
                st.info("Run a lane first.")

    # -------------------- RIGHT SIDE --------------------
    with col_right:
        with card():
            tab1, tab2 = st.tabs(["Route map", "Radar"])

            r = st.session_state.get("last_route")
            rs = st.session_state.get("last_risks")

            with tab1:
                if r:
                    st.plotly_chart(
                        build_route_map(r["origin"], r["dest"], rs["overall"], r["conflict"]),
                        use_container_width=True
                    )
                else:
                    st.info("Run a lane first.")

            with tab2:
                if r:
                    st.plotly_chart(build_risk_radar(rs), use_container_width=True)
                else:
                    st.info("Run a lane first.")

        with card("Comparison basket"):
            routes = st.session_state.setdefault("multi_routes", [])
            if not routes:
                st.info("Add lanes to compare.")
            else:
                df = pd.DataFrame([
                    {
                        "Lane": f"{x['origin']} → {x['dest']} ({x['mode'].upper()})",
                        "Geo": x["risks"]["geopolitical"],
                        "Climate": x["risks"]["climate"],
                        "Logistics": x["risks"]["logistics"],
                        "Cyber": x["risks"]["cyber"],
                        "Overall": x["risks"]["overall"],
                    } for x in routes
                ])
                st.dataframe(df, hide_index=True, use_container_width=True)

                if st.button("Compare with AI"):
                    prompt = "Compare these routes:\n" + df.to_string()
                    st.markdown(ai_call("You compare routes.", prompt))


# ============================================================
# SCENARIO LAB
# ============================================================

def render_scenario_lab():
    r = st.session_state.get("last_route")
    rs = st.session_state.get("last_risks")

    with card("Stress configuration"):
        if not r:
            st.info("Run a baseline lane first.")
            return

        geo_m = st.slider("Geopolitics multiplier", 0.8, 1.6, 1.1)
        cli_m = st.slider("Climate multiplier", 0.8, 1.8, 1.2)
        log_m = st.slider("Logistics multiplier", 0.8, 1.6, 1.1)
        cyb_m = st.slider("Cyber multiplier", 0.8, 1.5, 1.0)

        run = st.button("Run stress scenario")

    with card("Results"):
        if run:
            stressed = {
                "geopolitical": round(rs["geopolitical"] * geo_m, 1),
                "climate": round(rs["climate"] * cli_m, 1),
                "logistics": round(rs["logistics"] * log_m, 1),
                "cyber": round(rs["cyber"] * cyb_m, 1)
            }
            ov = (
                stressed["geopolitical"]*0.35 +
                stressed["climate"]*0.3 +
                stressed["logistics"]*0.25 +
                stressed["cyber"]*0.1
            )
            stressed["overall"] = float(np.clip(round(ov,1),0,100))

            df = pd.DataFrame({
                "Dimension":["Geopolitics","Climate","Logistics","Cyber","Overall"],
                "Base":[rs["geopolitical"],rs["climate"],rs["logistics"],rs["cyber"],rs["overall"]],
                "Stressed":[stressed[k] for k in ["geopolitical","climate","logistics","cyber","overall"]]
            })
            st.dataframe(df, hide_index=True, use_container_width=True)

            if st.button("Explain with AI", key="explain_scenario"):
                prompt = f"Base={rs}\nStressed={stressed}\nExplain scenario."
                st.markdown(ai_call("You explain scenarios.", prompt))
        else:
            st.info("Run a scenario above.")

# ============================================================
# GLOBAL HEATMAP
# ============================================================

def render_global_heatmap():
    with card("Global heatmap"):
        st.plotly_chart(build_heatmap(), use_container_width=True)

    with card("Country trend"):
        c = st.selectbox("Country", COUNTRY_LIST, index=COUNTRY_LIST.index("China"))
        months = st.slider("Months", 6, 24, 12)
        dates = pd.date_range(end=date.today(), periods=months, freq="M")
        base_g = get_score(GEO_RISK, c)
        base_c = get_score(CLIMATE_RISK, c)
        df = pd.DataFrame({
            "date": dates,
            "Geopolitics": [np.clip(base_g+random.randint(-6,8),0,100) for _ in dates],
            "Climate": [np.clip(base_c+random.randint(-4,10),0,100) for _ in dates],
        })
        fig = px.line(df, x="date", y=["Geopolitics","Climate"])
        st.plotly_chart(style_fig(fig), use_container_width=True)

# ============================================================
# AI STRATEGY ROOM
# ============================================================

def render_ai_strategy_room():
    with card("Strategy assistant"):
        question = st.text_area("Ask AI", height=120)
        ctx_parts = []

        r = st.session_state.get("last_route")
        rs = st.session_state.get("last_risks")
        if r and rs:
            ctx_parts.append(f"Last route: {r}, scores: {rs}")

        scen = st.session_state.get("scenario")
        if scen:
            ctx_parts.append(f"Scenario: {scen}")

        ctx = "\n".join(ctx_parts) if ctx_parts else "No context"

        if st.button("Ask"):
            prompt = f"Context:\n{ctx}\nQuestion:\n{question}"
            st.markdown(ai_call("You are a strategist.", prompt))

# ============================================================
# NETWORK OPTIMIZER
# ============================================================

def render_network_optimizer():
    r = st.session_state.get("last_route")
    rs = st.session_state.get("last_risks")

    with card("Baseline"):
        if not r:
            st.info("Run a baseline lane first.")
            return
        st.write(f"Base: {r['origin']} → {r['dest']} ({r['mode']}) · Risk {rs['overall']}")

    with card("Alternatives"):
        if st.button("Generate alternatives"):
            dep = date.fromisoformat(r["date"])
            alt_list = []

            # Mode shift
            alt_mode = "air" if r["mode"]=="sea" else "sea"
            alt_list.append({
                "label":"Mode shift",
                "origin":r["origin"], "dest":r["dest"], "mode":alt_mode,
                "risks":compute_route_risk(r["origin"],r["dest"],alt_mode,dep,r["weighting"],r["conflict"])
            })

            # Region shift
            safer = "Singapore" if r["origin"] in {"China","India"} else "Netherlands"
            alt_list.append({
                "label":"Region shift",
                "origin":safer, "dest":r["dest"], "mode":r["mode"],
                "risks":compute_route_risk(safer,r["dest"],r["mode"],dep,r["weighting"],r["conflict"])
            })

            st.session_state["optimizer_options"] = alt_list

        opts = st.session_state.get("optimizer_options", [])
        if opts:
            df = pd.DataFrame([
                {
                    "Option":x["label"],
                    "Lane":f"{x['origin']} → {x['dest']} ({x['mode']})",
                    "Overall":x["risks"]["overall"]
                } for x in opts
            ])
            st.dataframe(df, hide_index=True, use_container_width=True)

            if st.button("Recommend with AI", key="recommend_optimizer"):
                prompt = f"Base={r}, Risks={rs}\nOptions={opts}\nAdvise best choice."
                st.markdown(ai_call("You optimize networks.", prompt))

# ============================================================
# EXPORT CENTER
# ============================================================

def render_export_center():
    with card("Export summary"):
        r = st.session_state.get("last_route")
        rs = st.session_state.get("last_risks")

        if not r:
            st.info("Nothing to export.")
            return

        summary = {
            "Origin": r["origin"],
            "Destination": r["dest"],
            "Mode": r["mode"],
            "Date": r["date"],
            "Overall risk": rs["overall"],
            "Geo": rs["geopolitical"],
            "Climate": rs["climate"],
            "Logistics": rs["logistics"],
            "Cyber": rs["cyber"]
        }
        st.json(summary)

        txt = "\n".join([f"{k}: {v}" for k,v in summary.items()])
        st.download_button("Download text", txt, "summary.txt")

# ============================================================
# MAIN
# ============================================================

def main():
    render_hero()
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Route Analyzer", "Scenario Lab", "Global Heatmap",
        "AI Strategy Room", "Network Optimizer", "Export Center"
    ])
    with tab1: render_route_analyzer()
    with tab2: render_scenario_lab()
    with tab3: render_global_heatmap()
    with tab4: render_ai_strategy_room()
    with tab5: render_network_optimizer()
    with tab6: render_export_center()

if __name__ == "__main__":
    main()
