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
# 1. UNIVERSAL AI CONNECTOR (Finalized for Gemini 3)
# ============================================================
def ai_call(user_prompt: str):
    try:
        if "GOOGLE_API_KEY" not in st.secrets:
            return "⚠️ API Key missing in .streamlit/secrets.toml"
        
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        
        # Using the specific verified model from your environment list
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
        return f"⚠️ Strategic AI Error: {str(e)}\n\nPlease ensure your API key is enabled for Gemini 3 models."

# ============================================================
# 2. ARCTIC EMERALD UI (Updated for 2026 Streamlit Syntax)
# ============================================================
st.set_page_config(page_title="GeoClimate AI Command Center", layout="wide", page_icon="🌐")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Sora:wght@600;700&family=Inter:wght@400;500;600&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #F3F4F6 !important;
        color: #1F2937 !important;
        font-family: 'Inter', sans-serif;
    }

    .gc-hero {
        background: linear-gradient(90deg, #064E3B 0%, #059669 100%);
        color: white;
        padding: 40px;
        border-radius: 15px;
        margin-bottom: 25px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }

    .gc-card {
        background: white !important;
        border: 1px solid #E5E7EB !important;
        border-radius: 12px !important;
        padding: 24px !important;
        margin-bottom: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #E5E7EB;
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
        color: #374151 !important;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #059669 !important;
        color: white !important;
    }

    div[data-testid="stMetric"] {
        background: #F9FAFB !important;
        border: 1px solid #10B981 !important;
        border-radius: 10px !important;
        padding: 15px !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# 3. TAB CONTENT FUNCTIONS
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
            # STABILITY FIX: Create a unique 'seed' based on your text inputs
            # This makes the "random" numbers stay the same for the same route
            data_seed = f"{origin.lower()}{dest.lower()}{mode.lower()}"
            random.seed(data_seed) 
            
            risks = {
                "geopolitical": random.randint(35, 65), 
                "climate": random.randint(25, 80), 
                "logistics": random.randint(40, 70), 
                "cyber": random.randint(30, 60)
            }
            risks["overall"] = sum(risks.values()) // 4
            
            # Store data in session
            st.session_state["last_route"] = {"origin": origin, "dest": dest, "mode": mode, "date": str(date.today())}
            st.session_state["last_risks"] = risks
            
            # Reset the random seed for the rest of the app so other things stay random
            random.seed(None)
            
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    if "last_risks" in st.session_state:
        with col2:
            st.markdown('<div class="gc-card">', unsafe_allow_html=True)
            r = st.session_state["last_risks"]
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Geopolitics", r['geopolitical'])
            m2.metric("Climate", r['climate'])
            m3.metric("Logistics", r['logistics'])
            m4.metric("Risk Index", r['overall'])
            
            fig = go.Figure(data=go.Scatterpolar(
                r=[r['geopolitical'], r['climate'], r['logistics'], r['cyber'], r['geopolitical']],
                theta=['Geo', 'Climate', 'Logistics', 'Cyber', 'Geo'],
                fill='toself', line_color='#059669'
            ))
            fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=False)
            # 2026 Fix: width='stretch' instead of use_container_width
            st.plotly_chart(fig, width='stretch')
            st.markdown('</div>', unsafe_allow_html=True)

def render_network_optimizer():
    st.markdown('<div class="gc-card">', unsafe_allow_html=True)
    st.subheader("📈 Network Optimizer")
    if "last_route" in st.session_state:
        st.write(f"Optimizing routes for **{st.session_state['last_route']['origin']}** lane...")
        df = pd.DataFrame({
            "Alternative Route": ["Northern Sea Route", "Suez Canal Bypass", "Trans-Pacific Air"],
            "Resilience Score": [88, 74, 91],
            "Cost Efficiency": ["High", "Medium", "Low"]
        })
        st.table(df)
    else:
        st.info("Run a Route Analysis to unlock optimization insights.")
    st.markdown('</div>', unsafe_allow_html=True)

def render_export_center():
    st.markdown('<div class="gc-card">', unsafe_allow_html=True)
    st.subheader("📄 Executive Report Export")
    if "last_route" in st.session_state:
        r, rs = st.session_state["last_route"], st.session_state["last_risks"]
        report = f"""
        GEOCLIMATE AI STRATEGIC REPORT
        Generated: {r['date']}
        -------------------------------------------
        LANE: {r['origin']} to {r['dest']}
        MODE: {r['mode']}
        
        RISK SCORECARD:
        Overall: {rs['overall']}/100
        Geopolitical: {rs['geopolitical']}
        Climate: {rs['climate']}
        Logistics: {rs['logistics']}
        
        ADVISORY: Based on current indicators, we recommend 
        increasing safety stock by 12% at destination hubs.
        """
        st.text_area("Report Preview", report, height=200)
        st.download_button("Download Full Report", report, file_name="GeoClimate_Strategy.txt")
    else:
        st.info("No data available for export.")
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# MAIN APPLICATION
# ============================================================
def main():
    st.markdown('<div class="gc-hero"><h1>GeoClimate AI Command Center</h1><p>Predictive Intelligence for Global Logistics (v2026.1)</p></div>', unsafe_allow_html=True)
    
    tabs = st.tabs(["Route Analyzer", "Network Optimizer", "AI Strategy", "Global Heatmap", "Export Center"])
    
    with tabs[0]: render_route_analyzer()
    with tabs[1]: render_network_optimizer()
    with tabs[2]: 
        st.markdown('<div class="gc-card">', unsafe_allow_html=True)
        st.subheader("🤖 AI Strategy Assistant")
        q = st.text_input("Enter Query (e.g., How does the Suez bottleneck affect this route?)")
        if st.button("Consult AI"):
            with st.spinner("Analyzing signals..."):
                st.markdown("---")
                st.markdown(ai_call(q))
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tabs[3]:
        st.markdown('<div class="gc-card">', unsafe_allow_html=True)
        st.subheader("🗺️ Global Volatility Map")
        # Fix: Using ISO-3 Codes and width='stretch'
        df_map = pd.DataFrame({
            'ISO_Code': ['DEU', 'CAN', 'MEX', 'CHN', 'EGY'], 
            'Risk': [20, 15, 55, 75, 80],
            'Country': ['Germany', 'Canada', 'Mexico', 'China', 'Egypt']
        })
        fig = px.choropleth(
            df_map, 
            locations="ISO_Code", 
            locationmode='ISO-3', 
            color="Risk", 
            hover_name="Country",
            color_continuous_scale="RdYlGn_r"
        )
        st.plotly_chart(fig, width='stretch')
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tabs[4]: render_export_center()

if __name__ == "__main__":
    main()