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
# 1. AI CONNECTOR (FIXED)
# ============================================================
def ai_call(user_prompt: str):
    try:
        # Check for API key in secrets or environment
        api_key = st.secrets.get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if not api_key:
            return "⚠️ API Key missing. Please add GOOGLE_API_KEY to your Streamlit Secrets."
        
        genai.configure(api_key=api_key)
        # Using gemini-1.5-flash for better stability and speed
        model = genai.GenerativeModel("gemini-1.5-flash")

        route = st.session_state.get("last_route", {})
        risks = st.session_state.get("last_risks", {})
        
        context = (
            f"You are a Senior Supply Chain Strategist. Context: {route.get('origin', 'Global')} to {route.get('dest', 'Global')}. "
            f"Calculated Risk Index: {risks.get('overall', 'N/A')}/100."
        )
        
        full_prompt = f"{context}\n\nUser Question: {user_prompt}\n\nProvide a concise, executive-level advisory."
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"⚠️ Connection Error: {str(e)}"

# ============================================================
# 2. PREMIUM UI ENHANCEMENTS (FIXED TABS & FONTS)
# ============================================================
st.set_page_config(page_title="GeoClimate AI Command Center", layout="wide", page_icon="🌐")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Sora:wght@700;800&family=Inter:wght@400;600;700;800&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(120deg, #E0F2FE 0%, #F8FAFC 100%) !important;
        font-family: 'Inter', sans-serif;
    }

    .gc-hero {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        padding: 40px;
        border-radius: 20px;
        margin-bottom: 30px;
        border-bottom: 4px solid #3B82F6;
    }
    
    .gc-hero h1 { 
        font-family: 'Sora', sans-serif; 
        color: white !important;
        font-size: 2.8rem !important;
        margin-bottom: 0;
    }

    /* FIXING TAB FONT SIZES */
    .stTabs [data-baseweb="tab-list"] button p {
        font-size: 1.2rem !important; /* Increased font size */
        font-weight: 700 !important;
        color: #475569;
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent !important;
    }

    .stTabs [aria-selected="true"] p {
        color: #2563EB !important; /* Brighter blue for active tab */
    }

    .gc-card {
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 25px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
    }

    [data-testid="stMetricValue"] { 
        font-size: 2.2rem !important;
        font-weight: 800 !important;
        color: #2563EB !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# 3. CORE LOGIC
# ============================================================

def render_route_analyzer():
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown('<div class="gc-card">', unsafe_allow_html=True)
        st.subheader("📍 Lane Configuration")
        origin = st.text_input("Origin Hub", "Germany")
        dest = st.text_input("Destination Hub", "Canada")
        mode = st.selectbox("Freight Mode", ["Ocean", "Air", "Rail", "Road"])
        
        if st.button("Generate Intelligence", use_container_width=True):
            # Seed based on input to keep values stable for the same route
            seed_val = abs(hash(f"{origin}{dest}{mode}")) % (10**8)
            random.seed(seed_val)
            
            st.session_state["last_route"] = {"origin": origin, "dest": dest, "mode": mode, "date": str(date.today())}
            st.session_state["last_risks"] = {
                "geopolitical": random.randint(30, 70), 
                "climate": random.randint(40, 85), 
                "logistics": random.randint(25, 60),
                "overall": random.randint(45, 68)
            }
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    if "last_risks" in st.session_state:
        with col2:
            st.markdown('<div class="gc-card">', unsafe_allow_html=True)
            r = st.session_state["last_risks"]
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Geopolitics", f"{r['geopolitical']}%")
            m2.metric("Climate", f"{r['climate']}%")
            m3.metric("Logistics", f"{r['logistics']}%")
            m4.metric("Risk Index", f"{r['overall']}%")
            
            fig = go.Figure(data=go.Scatterpolar(
                r=[r['geopolitical'], r['climate'], r['logistics'], r['overall'], r['geopolitical']],
                theta=['Geo', 'Climate', 'Logistics', 'Overall', 'Geo'],
                fill='toself', 
                fillcolor='rgba(59, 130, 246, 0.2)',
                line=dict(color='#3B82F6', width=3)
            ))
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 100])), 
                height=350, 
                margin=dict(t=30, b=30, l=30, r=30),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

def main():
    st.markdown('<div class="gc-hero"><h1>GeoClimate AI</h1><p>Supply Chain Integrity & Sustainability Command Center</p></div>', unsafe_allow_html=True)
    
    tabs = st.tabs(["📍 Route Analyzer", "📈 Network Optimizer", "🤖 AI Strategy", "🗺️ Risk Map", "📄 Report Center"])
    
    with tabs[0]:
        render_route_analyzer()
    
    with tabs[1]:
        st.markdown('<div class="gc-card">', unsafe_allow_html=True)
        st.subheader("📈 Network Resiliency Optimization")
        if "last_route" in st.session_state:
            st.info(f"Analyzing alternative nodes for {st.session_state['last_route']['origin']} hub...")
            df_opt = pd.DataFrame({
                "Alternative Route": ["Arctic Secondary", "Suez Bypass", "Cape Route"],
                "Risk Mitigation": ["-12%", "-18%", "+5%"],
                "Cost Impact": ["High", "Medium", "Low"]
            })
            st.table(df_opt)
        else:
            st.warning("Please run Route Analyzer first.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tabs[2]:
        st.markdown('<div class="gc-card">', unsafe_allow_html=True)
        st.subheader("🤖 Strategic AI Advisory")
        user_q = st.text_input("Ask GeoClimate AI for tactical mitigation advice:")
        if st.button("Consult AI", use_container_width=True):
            with st.spinner("Analyzing global risk vectors..."):
                response = ai_call(user_q)
                st.markdown(f"**Advisory:**\n\n{response}")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with tabs[3]:
        st.markdown('<div class="gc-card">', unsafe_allow_html=True)
        st.subheader("🗺️ Global Volatility Heatmap")
        # Sample data for global visualization
        map_df = pd.DataFrame({
            'ISO': ['DEU', 'CAN', 'USA', 'CHN', 'IND', 'BRA', 'AUS'],
            'Risk': [25, 15, 22, 68, 45, 40, 12]
        })
        fig_map = px.choropleth(map_df, locations="ISO", color="Risk", 
                               color_continuous_scale="Reds", range_color=[0,100])
        fig_map.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=500)
        st.plotly_chart(fig_map, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tabs[4]:
        st.markdown('<div class="gc-card">', unsafe_allow_html=True)
        st.subheader("📄 Executive Strategy Report")
        if "last_route" in st.session_state:
            r, rs = st.session_state["last_route"], st.session_state["last_risks"]
            report = f"AUDIT: {r['origin']} → {r['dest']} ({r['mode']})\nINDEX: {rs['overall']}%\nDATE: {r['date']}"
            st.code(report, language='text')
            st.download_button("Export Full Audit", report, file_name=f"GeoClimate_Report_{r['origin']}.txt")
        else:
            st.warning("Generate intelligence to view report.")
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()