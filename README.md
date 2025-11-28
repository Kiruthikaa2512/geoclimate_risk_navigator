# GeoClimate AI – Command Center

**A nature-inspired control tower for global supply chain risk, resilience, and network design.**

GeoClimate AI scores global transportation lanes across **Geopolitics, Climate, Logistics, and Cyber**, simulates disruptions, compares network options, and generates strategic insights — powered entirely by a **mock AI engine** (no API keys required).

This makes it ideal for demos, prototyping, teaching, or secure on-prem setups where external API calls are restricted.

---

# Features

### **1. Route Analyzer**

* Score any lane between 30+ countries
* Multi-dimensional risk model (Geo / Climate / Logistics / Cyber)
* Conflict-aware scoring (Red Sea, Taiwan Strait, Black Sea, etc.)
* Visuals:

  * **Geo map**
  * **Risk radar**
* “Explain with AI” powered by the rule-based AI engine
* Add lanes to comparison basket

---

### **2. Scenario Lab**

Stress-test a lane by modifying:

* Geopolitical factor
* Climate exposure
* Logistics volatility
* Cyber posture

AI explains:

* Sensitivity
* What changed
* Implications
* Recommended actions

---

### **3. Global Heatmap**

World risk heatmap based on aggregated Geo/Climate scoring
Country risk-trend timeline for last 6–24 months

---

### **4. AI Strategy Room**

A tailored strategy assistant that:

* Recognizes countries and lanes in your question
* Distinguishes supply-chain vs. off-topic questions
* Provides structured executive guidance
* **Never leaks last_route context unless explicitly asked**

---

### **5. Network Optimizer**

Auto-generates routing alternatives:

* Mode shift (Sea ↔ Air)
* Region shift (Singapore / Netherlands hubs)
* AI recommends best option

---

### **6. Export Center**

Export a clean JSON summary of:

* Route
* Risk scores
* Metadata

Download as `.txt`.

---

# AI Layer (Mock Engine — No Keys Needed)

This project uses a custom **heuristic AI engine** instead of OpenAI/Anthropic:

✔ Works offline
✔ Zero cost
✔ No API keys
✔ Fully predictable
✔ Perfect for demos & prototyping

It emulates:

* Safety-mode selection
* Route explanations
* Scenario narratives
* Supply-chain strategy answers

while preventing the “overwriting everything with last route” bug.

---

# UI & Styling

### **Custom Styles Include:**

* Soft pastel lemon background
* Card UI components
* Improved spacing + shadow effects
* Google Fonts (Inter + Sora)
* Tabs, metrics, badge components

All styling is handled through injected CSS inside Streamlit.

---

# Installation

### **1. Clone repo**

```bash
git clone https://github.com/yourusername/geoclimate-ai
cd geoclimate-ai
```

### **2. Create environment**

```bash
python -m venv venv
source venv/bin/activate       # Linux/Mac
venv\Scripts\activate          # Windows
```

### **3. Install requirements**

```bash
pip install -r requirements.txt
```

---

# Run the app

```bash
streamlit run app.py
```

App runs at:

```
http://localhost:8501
```

---

# 🗂️ Project Structure

```
📦 geoclimate_risk_navigator
 ┣ 📄 app.py               # Main Streamlit app
 ┣ 📄 config.toml          # Theme overrides
 ┣ 📄 requirements.txt     # Dependencies
 ┣ 📄 LICENSE
 ┣ 📄 README.md
 
```

---

#  Tech Stack

* **Python 3.9+**
* **Streamlit**
* **Plotly**
* **Pandas / NumPy**
* **Custom Mock AI engine (rule-based NLP)**

---

# Roadmap 

* Add real LLM support (OpenAI, Anthropic, Groq)
* Multi-hop network routing
* Weather-driven modeling (NOAA, ECMWF APIs)
* Add CO₂ scoring
* ML-based disruption forecasting
* AzureAD/Okta authentication

---

# License

MIT License — free for commercial and personal use.

---

# Acknowledgements

Designed with the principles of supply-chain network engineering, climate analytics, and real-time geopolitical risk modeling.

---

