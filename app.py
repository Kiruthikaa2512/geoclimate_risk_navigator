import os
import random
from datetime import date
from typing import Dict, Any

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

try:
    import google.generativeai as genai
except Exception:
    genai = None


# ============================================================
# GEOCLIMATE AI COMMAND CENTER - STABLE UI VERSION
# No raw HTML leakage in KPI cards
# ============================================================

st.set_page_config(
    page_title="GeoClimate AI Command Center",
    layout="wide",
    page_icon="🌐",
    initial_sidebar_state="expanded",
)


# ============================================================
# 1. GLOBAL CSS
# ============================================================

st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Sora:wght@700;800&family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(120deg, #E0F2FE 0%, #F0FDF4 48%, #FFFBEB 100%) !important;
        background-attachment: fixed;
        font-family: 'Inter', sans-serif;
        color: #0F172A;
    }

    .main .block-container {
        padding-top: 1.3rem;
        padding-left: 2.2rem;
        padding-right: 2.2rem;
        max-width: 1500px;
    }

    h1, h2, h3 {
        font-family: 'Sora', sans-serif !important;
        letter-spacing: -0.03em;
        color: #0F172A !important;
    }

    p, li, label, textarea, input, select {
        font-size: 1rem !important;
        line-height: 1.45 !important;
    }

    label, [data-testid="stWidgetLabel"] p {
        font-weight: 750 !important;
        color: #1E293B !important;
        font-size: 1rem !important;
    }

    input, textarea, [data-baseweb="select"] {
        font-size: 1rem !important;
        border-radius: 12px !important;
    }

    section[data-testid="stSidebar"] {
        background: rgba(255,255,255,0.76);
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        font-size: 1.2rem !important;
        line-height: 1.2 !important;
    }

    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] span {
        font-size: 0.92rem !important;
        line-height: 1.45 !important;
    }

    .gc-hero {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        padding: 32px 38px;
        border-radius: 24px;
        margin-bottom: 24px;
        box-shadow: 0 18px 38px rgba(30, 41, 59, 0.18);
        border-bottom: 5px solid #3B82F6;
    }

    .gc-hero h1 {
        font-size: 2.75rem !important;
        font-weight: 800;
        color: #FFFFFF !important;
        margin: 0 0 6px 0;
        line-height: 1.05 !important;
    }

    .gc-hero p {
        color: #BFDBFE !important;
        font-weight: 650;
        font-size: 1.08rem !important;
        max-width: 980px;
        margin: 0;
    }

    .gc-card {
        background: rgba(255, 255, 255, 0.92) !important;
        border: 1px solid rgba(226, 232, 240, 0.95) !important;
        border-radius: 22px !important;
        padding: 26px !important;
        margin-bottom: 22px;
        box-shadow: 0 12px 22px rgba(15, 23, 42, 0.07);
    }

    .gc-section-title {
        font-family: 'Sora', sans-serif;
        font-size: 1.35rem !important;
        font-weight: 800;
        color: #0F172A;
        margin-bottom: 18px;
        line-height: 1.2 !important;
    }

    .gc-note {
        background: #EFF6FF;
        border-left: 5px solid #2563EB;
        padding: 14px 16px;
        border-radius: 13px;
        color: #1E3A8A;
        font-weight: 600;
        margin: 14px 0 4px 0;
        font-size: 0.98rem !important;
        line-height: 1.45 !important;
    }

    .gc-success {
        background: #ECFDF5;
        border-left: 5px solid #10B981;
        padding: 14px 16px;
        border-radius: 13px;
        color: #065F46;
        font-weight: 650;
        margin: 14px 0 0 0;
        font-size: 0.98rem !important;
    }

    .gc-warning {
        background: #FFFBEB;
        border-left: 5px solid #F59E0B;
        padding: 14px 16px;
        border-radius: 13px;
        color: #92400E;
        font-weight: 650;
        margin: 14px 0 0 0;
        font-size: 0.98rem !important;
    }

    .kpi-card {
        background: #FFFFFF;
        border: 1px solid #DCE3EE;
        border-radius: 18px;
        padding: 16px 14px;
        box-shadow: 0 8px 16px rgba(15, 23, 42, 0.06);
        min-height: 112px;
        margin-bottom: 10px;
    }

    .kpi-label {
        color: #475569;
        font-size: 0.86rem !important;
        font-weight: 800;
        line-height: 1.18 !important;
        margin-bottom: 8px;
    }

    .kpi-value {
        color: #0F172A;
        font-size: 1.85rem !important;
        font-weight: 900;
        line-height: 1 !important;
    }

    .kpi-status-low {
        color: #15803D;
        font-size: 0.76rem !important;
        font-weight: 800;
        margin-top: 8px;
    }

    .kpi-status-moderate {
        color: #B45309;
        font-size: 0.76rem !important;
        font-weight: 800;
        margin-top: 8px;
    }

    .kpi-status-high {
        color: #B91C1C;
        font-size: 0.76rem !important;
        font-weight: 800;
        margin-top: 8px;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        flex-wrap: wrap;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255, 255, 255, 0.82) !important;
        border-radius: 13px !important;
        padding: 12px 18px !important;
        border: 1px solid #CBD5E1 !important;
        min-height: 48px;
    }

    .stTabs [data-baseweb="tab"] p {
        font-size: 1rem !important;
        font-weight: 800 !important;
        color: #334155 !important;
    }

    .stTabs [aria-selected="true"] {
        background: #2563EB !important;
        box-shadow: 0 8px 18px rgba(37, 99, 235, 0.24);
    }

    .stTabs [aria-selected="true"] p {
        color: #FFFFFF !important;
    }

    .stButton > button, .stDownloadButton > button {
        background: linear-gradient(90deg, #2563EB, #3B82F6) !important;
        border: none !important;
        border-radius: 13px !important;
        color: white !important;
        font-size: 0.98rem !important;
        font-weight: 800 !important;
        padding: 0.64rem 1rem !important;
        box-shadow: 0 8px 18px rgba(37, 99, 235, 0.18);
    }

    [data-testid="stAlert"] {
        border-radius: 14px !important;
    }

    .dataframe, .stDataFrame, [data-testid="stTable"] {
        font-size: 0.98rem !important;
    }
</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# 2. DATA + SCORING LOGIC
# ============================================================

COUNTRY_ISO = {
    "Germany": "DEU",
    "Canada": "CAN",
    "United States": "USA",
    "China": "CHN",
    "India": "IND",
    "Japan": "JPN",
    "Mexico": "MEX",
    "Brazil": "BRA",
    "United Kingdom": "GBR",
    "Netherlands": "NLD",
    "Singapore": "SGP",
    "Vietnam": "VNM",
    "Taiwan": "TWN",
    "South Korea": "KOR",
    "France": "FRA",
    "Australia": "AUS",
}

BASE_RISK = {
    "Germany": 28,
    "Canada": 20,
    "United States": 24,
    "China": 66,
    "India": 46,
    "Japan": 30,
    "Mexico": 52,
    "Brazil": 58,
    "United Kingdom": 32,
    "Netherlands": 26,
    "Singapore": 22,
    "Vietnam": 48,
    "Taiwan": 56,
    "South Korea": 38,
    "France": 34,
    "Australia": 36,
}

MODE_ADJUSTMENT = {
    "Ocean": {"cost": 24, "speed": 42, "emissions": 35, "disruption": 52},
    "Air": {"cost": 78, "speed": 88, "emissions": 82, "disruption": 34},
    "Rail": {"cost": 45, "speed": 58, "emissions": 28, "disruption": 38},
    "Road": {"cost": 52, "speed": 62, "emissions": 55, "disruption": 46},
}


def clamp(value: int, low: int = 5, high: int = 95) -> int:
    return max(low, min(high, int(value)))


def build_seed(origin: str, dest: str, mode: str, cargo_priority: str) -> int:
    return abs(hash(f"{origin}|{dest}|{mode}|{cargo_priority}")) % (10**8)


def calculate_risks(origin: str, dest: str, mode: str, cargo_priority: str) -> Dict[str, int]:
    random.seed(build_seed(origin, dest, mode, cargo_priority))

    origin_base = BASE_RISK.get(origin, 45)
    dest_base = BASE_RISK.get(dest, 45)
    mode_data = MODE_ADJUSTMENT[mode]

    geopolitical = clamp((origin_base + dest_base) / 2 + random.randint(-8, 8))
    climate = clamp((mode_data["emissions"] * 0.45) + (dest_base * 0.55) + random.randint(-7, 9))
    logistics = clamp((mode_data["disruption"] * 0.55) + (origin_base * 0.20) + (dest_base * 0.25) + random.randint(-6, 8))

    if cargo_priority == "Fast delivery":
        operational = clamp((logistics * 0.55) + (mode_data["speed"] * 0.20) + (mode_data["cost"] * 0.25))
    elif cargo_priority == "Low cost":
        operational = clamp((logistics * 0.45) + (mode_data["cost"] * 0.45) + (mode_data["speed"] * 0.10))
    elif cargo_priority == "Low emissions":
        operational = clamp((logistics * 0.35) + (climate * 0.45) + (mode_data["emissions"] * 0.20))
    else:
        operational = clamp((logistics * 0.42) + (climate * 0.38) + (mode_data["emissions"] * 0.20))

    overall = clamp((geopolitical * 0.30) + (climate * 0.25) + (logistics * 0.25) + (operational * 0.20))
    random.seed(None)

    return {
        "geopolitical": geopolitical,
        "climate": climate,
        "logistics": logistics,
        "operational": operational,
        "overall": overall,
    }


def risk_label(score: int) -> str:
    if score >= 70:
        return "High"
    if score >= 45:
        return "Moderate"
    return "Low"


def risk_status_class(score: int) -> str:
    if score >= 70:
        return "kpi-status-high"
    if score >= 45:
        return "kpi-status-moderate"
    return "kpi-status-low"


def initialize_demo_state() -> None:
    if "last_route" not in st.session_state or "last_risks" not in st.session_state:
        origin = "Germany"
        dest = "Canada"
        mode = "Ocean"
        priority = "Balanced"
        st.session_state["last_route"] = {
            "origin": origin,
            "dest": dest,
            "mode": mode,
            "priority": priority,
            "date": str(date.today()),
        }
        st.session_state["last_risks"] = calculate_risks(origin, dest, mode, priority)


def kpi_card(label: str, value: int) -> None:
    st.markdown(
        f"""
<div class="kpi-card">
  <div class="kpi-label">{label}</div>
  <div class="kpi-value">{value}%</div>
  <div class="{risk_status_class(value)}">{risk_label(value)} exposure</div>
</div>
""",
        unsafe_allow_html=True,
    )


def render_kpi_cards(risks: Dict[str, int]) -> None:
    cols = st.columns(5, gap="small")
    metrics = [
        ("Geopolitical Risk", risks["geopolitical"]),
        ("Climate Risk", risks["climate"]),
        ("Logistics Risk", risks["logistics"]),
        ("Operational Risk", risks["operational"]),
        ("Overall Risk Index", risks["overall"]),
    ]

    for col, (label, value) in zip(cols, metrics):
        with col:
            kpi_card(label, value)


def generate_route_alternatives(route: Dict[str, Any], risks: Dict[str, int]) -> pd.DataFrame:
    origin = route.get("origin", "Germany")
    dest = route.get("dest", "Canada")
    mode = route.get("mode", "Ocean")
    priority = route.get("priority", "Balanced")

    seed = build_seed(origin, dest, mode, priority)
    random.seed(seed)

    baseline = risks["overall"]
    risk_drop_1 = random.randint(8, 16)
    risk_drop_2 = random.randint(3, 10)
    risk_drop_3 = random.randint(10, 20)

    options = [
        {
            "Alternative": f"{mode} Baseline",
            "Recommended Use": "Current plan",
            "Risk Score": baseline,
            "Risk Delta": "0%",
            "Cost Impact": "Baseline",
            "Transit Impact": "Baseline",
            "Executive Note": "Current route remains usable but should be monitored.",
        },
        {
            "Alternative": "Resilient Hub Reroute",
            "Recommended Use": "Risk reduction",
            "Risk Score": clamp(baseline - risk_drop_1),
            "Risk Delta": f"-{risk_drop_1}%",
            "Cost Impact": "+6% to +12%",
            "Transit Impact": "+1 to +3 days",
            "Executive Note": "Best when stability matters more than speed.",
        },
        {
            "Alternative": "Expedited Air Bridge",
            "Recommended Use": "Time-sensitive cargo",
            "Risk Score": clamp(baseline - risk_drop_2),
            "Risk Delta": f"-{risk_drop_2}%",
            "Cost Impact": "+25% to +40%",
            "Transit Impact": "-4 to -8 days",
            "Executive Note": "Useful for urgent shipments, but cost and emissions increase.",
        },
        {
            "Alternative": "Supplier Buffer Strategy",
            "Recommended Use": "Inventory protection",
            "Risk Score": clamp(baseline - risk_drop_3),
            "Risk Delta": f"-{risk_drop_3}%",
            "Cost Impact": "+4% to +9%",
            "Transit Impact": "No major change",
            "Executive Note": "Reduces disruption impact using backup allocation.",
        },
    ]

    random.seed(None)
    return pd.DataFrame(options).sort_values("Risk Score").reset_index(drop=True)


def build_report_text() -> str:
    r = st.session_state["last_route"]
    rs = st.session_state["last_risks"]
    alternatives = generate_route_alternatives(r, rs)
    best = alternatives.iloc[0]

    return f"""
GEOCLIMATE AI COMMAND CENTER - STRATEGIC AUDIT
================================================

Date:
{r['date']}

Lane:
{r['origin']} to {r['dest']}

Freight Mode:
{r['mode']}

Cargo Priority:
{r['priority']}

Risk Profile:
- Geopolitical Risk: {rs['geopolitical']}% ({risk_label(rs['geopolitical'])})
- Climate Risk: {rs['climate']}% ({risk_label(rs['climate'])})
- Logistics Risk: {rs['logistics']}% ({risk_label(rs['logistics'])})
- Operational Risk: {rs['operational']}% ({risk_label(rs['operational'])})
- Aggregate Risk Index: {rs['overall']}% ({risk_label(rs['overall'])})

Recommended Action:
{best['Alternative']}

Reason:
{best['Executive Note']}

Business Interpretation:
This is a transparent rules-based demonstration model designed to show how
geopolitical, climate, logistics, and operational indicators can be combined
into an executive supply chain risk view. For production use, this model should
connect to validated real-time logistics, weather, supplier, and geopolitical
datasets.

Prepared by:
GeoClimate AI Command Center
"""


# ============================================================
# 3. AI CONNECTOR
# ============================================================

def get_google_api_key():
    try:
        if "GOOGLE_API_KEY" in st.secrets:
            return st.secrets["GOOGLE_API_KEY"]
        if "GEMINI_API_KEY" in st.secrets:
            return st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass

    return os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")


def fallback_advisory(user_prompt: str) -> str:
    route = st.session_state.get("last_route", {})
    risks = st.session_state.get("last_risks", {})

    overall = risks.get("overall", 50)
    highest_risk = max(
        [
            ("Geopolitical", risks.get("geopolitical", 0)),
            ("Climate", risks.get("climate", 0)),
            ("Logistics", risks.get("logistics", 0)),
            ("Operational", risks.get("operational", 0)),
        ],
        key=lambda x: x[1],
    )

    if overall >= 70:
        tone = "This lane should be treated as high-risk and should not rely on a single routing option."
    elif overall >= 45:
        tone = "This lane is moderately exposed and should be supported with backup routing and supplier buffers."
    else:
        tone = "This lane appears relatively stable, but periodic monitoring is still recommended."

    return f"""
### Demo Advisory

{tone}

**Current lane:** {route.get('origin', 'Global')} to {route.get('dest', 'Global')} by {route.get('mode', 'selected mode')}  
**Overall risk:** {overall}%  
**Highest risk driver:** {highest_risk[0]} risk at {highest_risk[1]}%

**Recommended actions**
1. Prepare a backup route before shipment release.
2. Add supplier or inventory buffer if this is a critical shipment.
3. Monitor weather, customs, port congestion, and geopolitical disruption signals.
4. Escalate if the risk index crosses 70%.

**Note:** Add `GOOGLE_API_KEY` or `GEMINI_API_KEY` in Streamlit secrets to enable live Gemini advisory.
"""


def ai_call(user_prompt: str):
    if not user_prompt.strip():
        return "Please enter a question or choose one of the suggested advisory prompts."

    api_key = get_google_api_key()

    if not api_key:
        return fallback_advisory(user_prompt)

    if genai is None:
        return fallback_advisory(user_prompt) + "\n\nGoogle Generative AI package is not installed."

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-3.1-flash-lite")

        route = st.session_state.get("last_route", {})
        risks = st.session_state.get("last_risks", {})

        context = f"""
You are an executive supply chain risk advisor.

Route:
- Origin: {route.get('origin', 'Global')}
- Destination: {route.get('dest', 'Global')}
- Mode: {route.get('mode', 'Unknown')}
- Cargo Priority: {route.get('priority', 'Balanced')}

Risk Profile:
- Geopolitical: {risks.get('geopolitical', 'N/A')}%
- Climate: {risks.get('climate', 'N/A')}%
- Logistics: {risks.get('logistics', 'N/A')}%
- Operational: {risks.get('operational', 'N/A')}%
- Overall: {risks.get('overall', 'N/A')}%

Answer in concise executive language with:
1. Situation assessment
2. Business risk
3. Recommended action
4. Monitoring trigger
"""

        response = model.generate_content(f"{context}\n\nUser question: {user_prompt}")
        return response.text

    except Exception:
        return fallback_advisory(user_prompt)


# ============================================================
# 4. APP SCREENS
# ============================================================

def render_route_analyzer():
    col1, col2 = st.columns([0.9, 1.9], gap="large")

    with col1:
        st.markdown('<div class="gc-card">', unsafe_allow_html=True)
        st.markdown('<div class="gc-section-title">📍 Lane Configuration</div>', unsafe_allow_html=True)

        countries = sorted(COUNTRY_ISO.keys())
        current = st.session_state["last_route"]

        origin = st.selectbox(
            "Origin Hub",
            countries,
            index=countries.index(current.get("origin", "Germany")) if current.get("origin", "Germany") in countries else 0,
        )
        dest = st.selectbox(
            "Destination Hub",
            countries,
            index=countries.index(current.get("dest", "Canada")) if current.get("dest", "Canada") in countries else 0,
        )
        mode = st.selectbox(
            "Freight Mode",
            ["Ocean", "Air", "Rail", "Road"],
            index=["Ocean", "Air", "Rail", "Road"].index(current.get("mode", "Ocean")),
        )
        priority = st.selectbox(
            "Cargo Priority",
            ["Balanced", "Fast delivery", "Low cost", "Low emissions"],
            index=["Balanced", "Fast delivery", "Low cost", "Low emissions"].index(current.get("priority", "Balanced")),
        )

        if st.button("Generate Intelligence", use_container_width=True):
            st.session_state["last_route"] = {
                "origin": origin,
                "dest": dest,
                "mode": mode,
                "priority": priority,
                "date": str(date.today()),
            }
            st.session_state["last_risks"] = calculate_risks(origin, dest, mode, priority)
            st.rerun()

        st.markdown(
            '<div class="gc-note">Demo model: transparent rules-based scoring. Production version can connect to real-time supplier, weather, logistics, and geopolitical feeds.</div>',
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="gc-card">', unsafe_allow_html=True)
        st.markdown('<div class="gc-section-title">Risk Intelligence Dashboard</div>', unsafe_allow_html=True)

        r = st.session_state["last_risks"]
        render_kpi_cards(r)

        fig = go.Figure(
            data=go.Scatterpolar(
                r=[
                    r["geopolitical"],
                    r["climate"],
                    r["logistics"],
                    r["operational"],
                    r["geopolitical"],
                ],
                theta=["Geopolitical", "Climate", "Logistics", "Operational", "Geopolitical"],
                fill="toself",
                line_color="#2563EB",
                name="Risk Exposure",
            )
        )
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100], tickfont=dict(size=12)),
                angularaxis=dict(tickfont=dict(size=13)),
            ),
            height=390,
            margin=dict(t=28, b=22, l=35, r=35),
            showlegend=False,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown(
            f'<div class="gc-success">Executive readout: This lane is classified as <b>{risk_label(r["overall"])}</b> risk with an aggregate score of <b>{r["overall"]}%</b>.</div>',
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)


def render_network_optimizer():
    st.markdown('<div class="gc-card">', unsafe_allow_html=True)
    st.markdown('<div class="gc-section-title">📈 Network Optimizer</div>', unsafe_allow_html=True)

    route = st.session_state["last_route"]
    risks = st.session_state["last_risks"]

    st.markdown(
        f'<div class="gc-note">Optimizing route strategy for <b>{route["origin"]} → {route["dest"]}</b> using <b>{route["mode"]}</b> freight and <b>{route["priority"]}</b> priority.</div>',
        unsafe_allow_html=True,
    )

    alternatives = generate_route_alternatives(route, risks)
    best = alternatives.iloc[0]

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            f'<div class="kpi-card"><div class="kpi-label">Best Option</div><div class="kpi-value" style="font-size:1.18rem!important;line-height:1.18!important;">{best["Alternative"]}</div><div class="kpi-status-low">Recommended path</div></div>',
            unsafe_allow_html=True,
        )
    with c2:
        kpi_card("Best Risk Score", int(best["Risk Score"]))
    with c3:
        st.markdown(
            f'<div class="kpi-card"><div class="kpi-label">Expected Risk Change</div><div class="kpi-value">{best["Risk Delta"]}</div><div class="kpi-status-low">Compared with baseline</div></div>',
            unsafe_allow_html=True,
        )

    fig = px.bar(
        alternatives,
        x="Alternative",
        y="Risk Score",
        text="Risk Score",
        title="Route Alternative Risk Comparison",
    )
    fig.update_traces(texttemplate="%{text}%", textposition="outside")
    fig.update_layout(
        yaxis_range=[0, 100],
        height=420,
        font=dict(size=14),
        margin=dict(t=65, b=80, l=38, r=28),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.55)",
    )
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(alternatives, use_container_width=True, hide_index=True)

    st.markdown("</div>", unsafe_allow_html=True)


def render_ai_strategy():
    st.markdown('<div class="gc-card">', unsafe_allow_html=True)
    st.markdown('<div class="gc-section-title">🤖 Strategic AI Advisory</div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="gc-note">Ask the advisory engine for executive recommendations. If the API key fails or is missing, the app still produces a demo advisory instead of breaking.</div>',
        unsafe_allow_html=True,
    )

    suggestions = {
        "Suggest safer route": "Suggest the safest route strategy for this shipment.",
        "Explain risk score": "Explain the current risk score in simple executive language.",
        "Executive summary": "Create a short executive summary for leadership.",
        "Mitigation plan": "Give a practical mitigation plan for this route.",
    }

    s1, s2, s3, s4 = st.columns(4)
    selected_prompt = ""

    if s1.button("Suggest safer route", use_container_width=True):
        selected_prompt = suggestions["Suggest safer route"]
    if s2.button("Explain risk score", use_container_width=True):
        selected_prompt = suggestions["Explain risk score"]
    if s3.button("Executive summary", use_container_width=True):
        selected_prompt = suggestions["Executive summary"]
    if s4.button("Mitigation plan", use_container_width=True):
        selected_prompt = suggestions["Mitigation plan"]

    q = st.text_area(
        "Consult System",
        value=selected_prompt,
        placeholder="Example: What should leadership do if the climate risk increases next week?",
        height=120,
    )

    if st.button("Generate Advisory", use_container_width=True):
        with st.spinner("Generating advisory..."):
            st.markdown(ai_call(q))

    st.markdown("</div>", unsafe_allow_html=True)


def render_risk_map():
    st.markdown('<div class="gc-card">', unsafe_allow_html=True)
    st.markdown('<div class="gc-section-title">🗺️ Global Volatility Map</div>', unsafe_allow_html=True)

    route = st.session_state["last_route"]
    risks = st.session_state["last_risks"]

    map_rows = []
    for country, iso in COUNTRY_ISO.items():
        score = BASE_RISK.get(country, 45)
        if country == route["origin"]:
            score = max(score, risks["geopolitical"])
        if country == route["dest"]:
            score = max(score, risks["overall"])

        map_rows.append(
            {
                "Country": country,
                "ISO": iso,
                "Risk Score": clamp(score),
                "Role": "Origin" if country == route["origin"] else "Destination" if country == route["dest"] else "Reference Market",
            }
        )

    map_df = pd.DataFrame(map_rows)

    fig_map = px.choropleth(
        map_df,
        locations="ISO",
        color="Risk Score",
        hover_name="Country",
        hover_data={"Role": True, "ISO": False, "Risk Score": True},
        color_continuous_scale="YlOrRd",
        range_color=[0, 100],
        title=f"Route Exposure: {route['origin']} → {route['dest']}",
    )

    fig_map.update_layout(
        height=510,
        font=dict(size=14),
        margin=dict(t=58, b=18, l=18, r=18),
        paper_bgcolor="rgba(0,0,0,0)",
    )

    st.plotly_chart(fig_map, use_container_width=True)

    selected_points = map_df[map_df["Role"].isin(["Origin", "Destination"])]
    st.dataframe(selected_points, use_container_width=True, hide_index=True)

    st.markdown("</div>", unsafe_allow_html=True)


def render_report_center():
    st.markdown('<div class="gc-card">', unsafe_allow_html=True)
    st.markdown('<div class="gc-section-title">📄 Executive Strategy Report</div>', unsafe_allow_html=True)

    report_text = build_report_text()

    st.text_area("Live Report Preview", report_text, height=420)

    file_name = f"GeoClimate_{st.session_state['last_route']['origin']}_{st.session_state['last_route']['dest']}_Audit.txt".replace(" ", "_")

    st.download_button(
        "Download TXT Audit Report",
        report_text,
        file_name=file_name,
        mime="text/plain",
        use_container_width=True,
    )

    st.markdown(
        '<div class="gc-warning">PDF export can be added later. Current version correctly downloads a clean TXT executive audit report.</div>',
        unsafe_allow_html=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)


def render_sidebar():
    with st.sidebar:
        st.markdown("## GeoClimate AI")
        st.markdown("### Demo Controls")

        api_key = get_google_api_key()

        if api_key:
            st.success("AI key detected. Live Gemini advisory enabled.")
        else:
            st.warning("No API key found. Demo advisory fallback enabled.")

        st.markdown("---")
        st.markdown("### App Version")
        st.markdown("**v3.2 stable UI**")
        st.markdown(
            """
- Fixed raw HTML issue
- Fixed cropped KPI labels
- Cleaner sidebar
- AI fallback retained
- Dynamic route dashboard
"""
        )


# ============================================================
# 5. MAIN APP
# ============================================================

def main():
    initialize_demo_state()
    render_sidebar()

    st.markdown(
        """
<div class="gc-hero">
    <h1>GeoClimate AI Command Center</h1>
    <p>Executive logistics intelligence platform for route risk, climate exposure, network resilience, and AI-assisted supply chain decisions.</p>
</div>
""",
        unsafe_allow_html=True,
    )

    tabs = st.tabs(
        [
            "📍 Route Analyzer",
            "📈 Network Optimizer",
            "🤖 AI Strategy",
            "🗺️ Risk Map",
            "📄 Report Center",
        ]
    )

    with tabs[0]:
        render_route_analyzer()

    with tabs[1]:
        render_network_optimizer()

    with tabs[2]:
        render_ai_strategy()

    with tabs[3]:
        render_risk_map()

    with tabs[4]:
        render_report_center()


if __name__ == "__main__":
    main()
