# 💨 BreatheAhead — Municipal Digital Twin for Urban Air Quality Operations

> **Proactive, ward-level air quality intelligence for Vadodara Municipal Corporation (VMC)**
> Forecast · Simulate · Advise · Attribute — all in one AI-driven Operations Center.

---

## 🌐 Overview

**BreatheAhead** is a real-time **Municipal Digital Twin Control** platform built for urban authorities to monitor, forecast, and act on air quality data at a hyperlocal, ward level. Designed specifically for **Vadodara, Gujarat**, the platform integrates time-series forecasting, an intervention impact simulator, a ranked policy-intervention engine, Gemini-powered multilingual health advisories, and heuristic source attribution — all delivered through the **BreatheAhead Operations Center**, a premium dark-themed Streamlit dashboard.

- **🔗 GitHub Repo:** https://github.com/25032007/BreatheAhead
- **🚀 Live Demo:** https://breatheahead-dgq8r2ynqf2qmcnxbrhf7y.streamlit.app/
- **🎥 Demo Video:** https://drive.google.com/file/d/1Zl53loqkBW2YXw98Z78W2wNtw7FcTij9/view?usp=sharing

---

## ✨ Key Features

| Module | Description |
|---|---|
| 🗺️ **Live AQI Map** | Interactive Folium heatmap of AQI readings across Vadodara wards, with AI Spatial Dispatch recommendations near critical exposure targets (hospitals, campuses, parks) |
| 🤖 **AI Forecast (Prophet)** | 72-hour AQI prediction using Meta's Prophet time-series model, benchmarked against a persistence baseline |
| ⚗️ **Intervention Simulator** | Policy "what-if" tool — tune traffic, construction, industry, and green-cover levers and see simulated AQI delta, estimated dust abatement, and health exposure risk |
| 📋 **Ranked Policy Interventions** | Auto-ranked municipal action plan (e.g. dust suppression, signal optimization, flue-gas control) scored by AQI impact, cost tier, and confidence, tagged to the responsible department |
| 💬 **Health Advisory (AI Coordinator Console)** | Gemini-powered bilingual (English + Gujarati) citizen advisories and formal municipal enforcement notices, presented as a live administrator ↔ AI assistant conversation |
| 🔍 **Source Attribution** | Proximity-heuristic scoring to identify the dominant pollution source per ward (traffic / construction / industrial) |
| ⚙️ **Settings Console** | Configure Gemini API endpoint, model version, temperature, and alert webhooks |

---

## 🏗️ Project Structure

```
BreatheAhead/
├── app/
│   ├── app.py                  # Main Streamlit application (~2000 lines)
│   ├── forecast_model.py       # Prophet model training, evaluation & simulator logic
│   ├── advisory_gemini.py      # Gemini REST API integration for health advisories
│   ├── attribution.py          # Heuristic proximity-based source attribution
│   ├── data_gen.py             # Synthetic AQI data generator
│   └── test_api.py             # API connectivity test utility
├── data/
│   ├── vadodara_aqi_history.csv    # Historical AQI data (Sayajigunj)
│   ├── forecast_output.json        # Prophet forecast results (72h)
│   ├── advisory_output.json        # Latest Gemini advisory output
│   └── attribution_output.json     # Latest source attribution result
├── models/                     # (Reserved for serialized model artifacts)
├── docs/                       # (Reserved for extended documentation)
├── demo/                       # Demo screenshots
├── ppt/                        # Presentation materials
└── requirements.txt
```

---

## 🧠 Architecture & Module Breakdown

### 1. AI Forecast — `forecast_model.py`
- Trains a **Facebook Prophet** model on historical daily AQI data for Vadodara (Sayajigunj ward)
- Evaluates against a 10-day held-out test set using **RMSE** vs a persistence baseline
- Produces a **72-hour forward forecast** saved to `data/forecast_output.json`
- Exposes `simulate_intervention(base_forecast, reduction_pct)` — a function that calculates a revised AQI forecast when activity levels are reduced (6% AQI drop per 10% activity reduction)

### 2. Intervention Simulator — `app.py`
- UI sliders for four intervention levers:
  - 🚦 **Traffic Reduction** (%)
  - 🏗️ **Construction Mitigation** (%)
  - 🏭 **Industrial Reduction** (%)
  - 🌿 **Green Cover Increase** (%)
- Computes combined simulated AQI curve vs baseline, rendered as an interactive **Plotly** chart (Peak AQI Delta, Est. Environmental Dust Abatement, Health Exposure Risk)
- Quantifies estimated "lives protected" and "hospitalizations prevented" from reduction scenarios

### 3. Ranked Policy Interventions — `app.py`
- Surfaces a prioritized list of municipal actions (e.g. Construction Site Dust Suppression, Smart Traffic Signal Optimization, Industrial Flue Gas Mitigation Control)
- Each entry is scored on **AQI impact, cost tier, and model confidence**, and tagged to the responsible department (VMC Environment Dept, VMC Traffic Police, GPCB Regulatory Board)
- Includes a "Simulate Abatement" action per intervention

### 4. Health Advisory — `advisory_gemini.py`
- Calls the **Gemini REST API** (`gemini-2.0-flash` and fallbacks) with a structured ward-level prompt
- Returns three structured outputs:
  - `EN_ADVISORY` — English citizen health advisory
  - `GU_ADVISORY` — Gujarati translation
  - `STAFF_NOTICE` — Formal VMC enforcement directive
- Outputs parsed and saved to `data/advisory_output.json`
- In the dashboard: shown as the **AI Coordinator Console**, a chat-style flow (Municipal Administrator request → Gemini Operations Assistant → Public Safety Advisory) with Copy and Broadcast actions, plus enforcement buffer zones and emergency contact info in the side panel

### 5. Source Attribution — `attribution.py`
- Scores three source categories (**traffic**, **construction**, **industrial**) using inverse-distance weighting from approximate ward coordinates
- Identifies `dominant_source` and a `confidence_score` (0–100%)
- **Note:** this is a heuristic proximity-based score, not a trained ML classifier — the dashboard surfaces this distinction directly to keep the attribution transparent
- Result saved to `data/attribution_output.json` and consumed live by the Advisory and Dashboard pages

### 6. Live AQI Map — `app.py`
- Renders a **Folium** interactive map centered on Vadodara
- Ward markers color-coded by AQI category (Good → Hazardous)
- **HeatMap layer** showing PM2.5 concentration intensity
- **AI Spatial Dispatch** panel flagging high particulate density near critical exposure targets (e.g. hospitals) with suppression recommendations
- Ward-level popups showing AQI value, category, and dominant source

### 7. Dashboard — `app.py`
- KPI cards: current AQI, 24-hour peak forecast, exposed population, AI model confidence
- Public Risk Index and forecast horizon (+72 hours, with RMSE-based accuracy)
- 30-day AQI history trend chart (Plotly)
- Pollution source breakdown donut chart
- Live weather widget with temperature, humidity, wind, PM2.5, NO₂ readouts

---

## 📸 Screenshots

| Dashboard | Ranked Interventions |
|---|---|
| Municipal Digital Twin Control — live KPIs, risk index, forecast horizon | Cost/impact/confidence-ranked municipal action plan |

| Live AQI Map | AI Forecast |
|---|---|
| Heatmap + AI Spatial Dispatch near critical exposure zones | Prophet forecast vs persistence baseline, with model error telemetry |

| Intervention Simulator | Health Advisory (AI Coordinator Console) |
|---|---|
| Live-adjustable sliders for traffic/construction/industry/green cover | Gemini-generated bilingual advisories and enforcement notices |

*(Add screenshots from `demo/` here before final submission.)*

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- A **Gemini API key** (for the Health Advisory module)

### 1. Clone the repository
```bash
git clone https://github.com/25032007/BreatheAhead.git
cd BreatheAhead
```

### 2. Create a virtual environment
```bash
python -m venv app/venv
# Windows
app\venv\Scripts\activate
# macOS / Linux
source app/venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set the Gemini API key
```bash
# Windows (PowerShell)
$env:GEMINI_API_KEY = "your_api_key_here"

# macOS / Linux
export GEMINI_API_KEY="your_api_key_here"
```

### 5. (Optional) Pre-generate forecast & advisory data
```bash
# Run the forecast model to regenerate forecast_output.json
python app/forecast_model.py

# Run source attribution for Sayajigunj
python app/attribution.py

# Run Gemini advisory generation (requires GEMINI_API_KEY)
python app/advisory_gemini.py
```

### 6. Launch the app
```bash
streamlit run app/app.py
```

The app will open at **http://localhost:8501**.

---

## 📦 Dependencies

| Package | Purpose |
|---|---|
| `streamlit` | Web application framework |
| `pandas` | Data manipulation |
| `numpy` | Numerical computing |
| `prophet` | Time-series forecasting |
| `plotly` | Interactive charts |
| `folium` | Interactive maps |
| `streamlit-folium` | Folium ↔ Streamlit bridge |
| `google-genai` | Gemini AI SDK |
| `requests` | REST API calls (Gemini fallback) |

---

## 🗺️ Supported Wards

The platform currently covers the following Vadodara wards with ward-specific data:

| Ward | AQI Profile | Dominant Source |
|---|---|---|
| Sayajigunj | Poor (157) | Construction |
| Alkapuri | Moderate (98) | Traffic |
| Fatehgunj | Satisfactory (72) | Mixed |
| Manjalpur | Good (48) | — |
| Waghodia Road | Moderate (115) | Industrial |

---

## 🔑 Environment Variables

| Variable | Description | Required |
|---|---|---|
| `GEMINI_API_KEY` | Google Gemini API key for advisory generation | Yes (for Advisory module) |

---

## 🧪 Model Performance

The Prophet forecast model is benchmarked against a simple persistence baseline (tomorrow = today) on a 10-day held-out test set:

| Metric | AI Prophet Model | Persistence Baseline |
|---|---|---|
| RMSE | **4.33** | 28.94 |

Lower RMSE confirms high prediction trust relative to the naive baseline. Metrics are printed to console on each run of `forecast_model.py` and displayed live on the AI Forecast page (Model Error Telemetry panel) of the dashboard.

---

## 🤝 Team & Credits

Built for **Vadodara Municipal Corporation (VMC)** as part of an AI-powered Smart City initiative.

- **Anjali Mulchandani** — Team Leader
- **Deepikaben Jinabhai Vala** — Team Member
- **Janvi Yadav** — Team Member

**Stack**: Python · Streamlit · Prophet · Gemini AI · Folium · Plotly
**Target City**: Vadodara, Gujarat, India
**Data Source**: Historical AQI records — Sayajigunj monitoring station

---
