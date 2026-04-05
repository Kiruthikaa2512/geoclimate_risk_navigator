import os
import random
from datetime import date
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import google.generativeai as genai

# ============================================================
# 1. AI CONNECTOR
# ============================================================
def ai_call(user_prompt: str):
    try:
        if "GOOGLE_API_KEY" not in st.secrets:
            return "⚠️ API Key missing in .streamlit/secrets.toml"
        
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        model = genai.GenerativeModel("gemini-3-flash-preview")

        route = st.session_state.get("last_route", {})
        risks = st.session_state.get("last_risks", {})
        
        context = (
            f"Logistics Context: {route.get('origin', 'Global')} to {route.get('dest', 'Global')}. "
            f"Overall Risk Score: {risks.get('overall', 'N/A')}/100."
        )
        
        response = model.generate_content(f"{context}\n\nQuestion: {user_prompt}")
        return response.text
    except Exception as e:
        return f"⚠️ Connection Error: {str(e)}"

# ============================================================
# 2. PREMIUM ENTERPRISE UI (Navy & Electric Blue)
# ============================================================
st.set_page_config(page_title="GeoClimate AI Command Center", layout="wide", page_icon="🌐")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Sora:wght@700;800&family=Inter:wght@400;600;700;800&display=swap');
    
    /* Milder Professional Background */
    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(180deg, #F1F5F9 0%, #E2E8F0 100%) !important;
        font-family: 'Inter', sans-serif;
    }

    /* Navy Hero Banner */
    .gc-hero {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        color: white;
        padding: 55px;
        border-radius: 24px;
        margin-bottom: 30px;
        box-shadow: 0 15px 30px rgba(15, 23, 42, 0.15);
        border-left: 10px solid #3B82F6;
    }
    .gc-hero h1 { 
        font-family: 'Sora', sans-serif; 
        font-size: 3.6rem !important; 
        font-weight: 800; 
        margin: 0; 
        letter-spacing: -2px;
    }

    /* Ultra-Bold High-Contrast Tabs */
    .stTabs [data-baseweb="tab-list"] { gap: 15px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #CBD5E1;
        border-radius: 12px;
        padding: 18px 35px !important;
        font-size: 1.3rem !important;
        color: #0F172A !important; /* Dark text for contrast */
        font-weight: 800 !important; /* Maximum Boldness */
        border: 2px solid #94A3B8;
        white-space: nowrap;
        transition: all 0.3s ease;
    }
    .stTabs [aria-selected="true"] {
        background: #1E293B !important;
        color: #3B82F6 !important; /* Electric Blue Highlight */
        border-color: #3B82F6 !important;
        transform: translateY(-2px);
    }

    /* Metric Styling */
    [data-testid="stMetricValue"] { 
        font-family: 'Sora', sans-serif !important; 
        font-size: 3.8rem !important; 
        font-weight: 800 !important; 
        color: #1E293B !important; 
    }
    [data-testid="stMetricLabel"] { 
        font-size: 1.2rem !important; 
        font-weight: 800 !important; 
        color: #475569 !important; 
    }

    .gc-card {
        background: white !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 20px !important;
        padding: 35px !important;
        margin-bottom: 20px;
    }

    .stButton > button {
        background-color: #3B82F6 !important;
        color: white !important;
        font-weight: 800 !important;
        font-size: 1.3rem !important;
        border-radius: 12px !important;
        padding: 15px 30px !important;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# 3. COMPONENT FUNCTIONS
# ============================================================

def render_route_analyzer():
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown('<div class="gc-card">', unsafe_allow_html=True)
        st.subheader("📍 Lane Configuration")
        origin = st.text_input("Origin Hub", "Germany")
        dest = st.text_input("Destination Hub", "Canada")
        mode = st.selectbox("Freight Mode", ["Ocean", "Air", "Rail", "Road"])
        
        if st.button("Generate Intelligence"):
            # STABILITY LOGIC: Seed the random generator using input strings
            # This ensures the values stay the same unless the input changes.
            seed_val = hash(f"{origin}{dest}{mode}")
            random.seed(seed_val)
            
            st.session_state["last_route"] = {"origin": origin, "dest": dest, "mode": mode, "date": str(date.today())}
            st.session_state["last_risks"] = {
                "geopolitical": random.randint(30, 70), 
                "climate": random.randint(40, 85), 
                "logistics": random.randint(25, 60),
                "overall": random.randint(45, 68)
            }
            random.seed(None) # Reset seed
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    if "last_risks" in st.session_state:
        with col2:
            st.markdown('<div class="gc-card">', unsafe_allow_html=True)
            r = st.session_state["last_risks"]
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Geo-Politics", f"{r['geopolitical']}%")
            m2.metric("Climate", f"{r['climate']}%")
            m3.metric("Logistics", f"{r['logistics']}%")
            m4.metric("Risk Index", f"{r['overall']}%")
            
            fig = go.Figure(data=go.Scatterpolar(
                r=[r['geopolitical'], r['climate'], r['logistics'], r['overall'], r['geopolitical']],
                theta=['Geo', 'Climate', 'Logistics', 'Operational', 'Geo'],
                fill='toself', line_color='#3B82F6'
            ))
            fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), height=380, margin=dict(t=20, b=20))
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

def render_report_center():
    st.markdown('<div class="gc-card">', unsafe_allow_html=True)
    st.subheader("📄 Executive Strategy Report")
    if "last_route" in st.session_state:
        r = st.session_state["last_route"]
        rs = st.session_state["last_risks"]
        report_text = f"""
        GEOCLIMATE STRATEGIC AUDIT
        --------------------------
        DATE: {r['date']}
        LANE: {r['origin']} TO {r['dest']}
        MODE: {r['mode']}
        
        RISK PROFILE:
        - Geopolitical Stability: {rs['geopolitical']}%
        - Climate Resilience: {rs['climate']}%
        - Logistics Integrity: {rs['logistics']}%
        - AGGREGATE RISK INDEX: {rs['overall']}%
        """
        st.text_area("Live Report Preview", report_text, height=250)
        st.download_button("Download Full Audit (PDF/TXT)", report_text, file_name=f"GeoClimate_{r['origin']}_Report.txt")
    else:
        st.warning("⚠️ No Data: Generate intelligence to compile report.")
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# MAIN
# ============================================================
def main():
    st.markdown('<div class="gc-hero"><h1>GeoClimate AI Command Center</h1><p>Executive Logistics Intelligence Platform (v2.6)</p></div>', unsafe_allow_html=True)
    
    tabs = st.tabs(["📍 Route Analyzer", "📈 Network Optimizer", "🤖 AI Strategy", "🗺️ Risk Map", "📄 Report Center"])
    
    with tabs[0]: render_route_analyzer()
    with tabs[1]:
        st.markdown('<div class="gc-card">', unsafe_allow_html=True)
        st.subheader("📈 Network Optimizer")
        if "last_route" in st.session_state:
            st.info(f"Optimizing node resiliency for {st.session_state['last_route']['origin']}...")
            st.table(pd.DataFrame({"Alternative": ["Arctic Lane", "Cape Bypass"], "Risk Delta": ["-12%", "+15%"], "Cost": ["High", "Medium"]}))
        else: st.warning("Analysis required.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tabs[2]:
        st.markdown('<div class="gc-card">', unsafe_allow_html=True)
        st.subheader("🤖 Strategic AI")
        q = st.text_input("Consult System")
        if st.button("Generate Advisory"): st.write(ai_call(q))
        st.markdown('</div>', unsafe_allow_html=True)
        
    with tabs[3]:
        st.markdown('<div class="gc-card">', unsafe_allow_html=True)
        st.subheader("🗺️ Global Volatility")
        fig_map = px.choropleth(pd.DataFrame({'ISO':['DEU','CAN','USA','CHN'], 'R':[25,15,20,70]}), locations="ISO", color="R", color_continuous_scale="YlOrRd")
        st.plotly_chart(fig_map, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tabs[4]: render_report_center()

if __name__ == "__main__":
    main()