import streamlit as st
import pandas as pd
import json
import folium
import os
from streamlit_folium import st_folium

st.set_page_config(page_title="BreatheAhead", layout="wide")

st.title("BreatheAhead")
st.header("Vadodara AQI Dashboard")
st.caption("A hackathon project for predicting and managing air quality in Vadodara.")

# Dummy function for intervention simulation
def simulate_intervention(forecast_data, reduction_percent):
    # Simply reduce the forecast values by the given percentage
    reduced = [val * (1 - reduction_percent/100.0) for val in forecast_data]
    return reduced

# Load Data
@st.cache_data
def load_data():
    try:
        # Load from the new relative path: ../data/forecast_output.json
        data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'forecast_output.json')
        with open(data_path, 'r') as f:
            data = json.load(f)
            # handle both single dictionary (from real model) or list of dictionaries
            if isinstance(data, dict):
                return {data.get("ward", "Unknown"): data}
            elif isinstance(data, list):
                return {item["ward"]: item for item in data}
            return {}
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return {}

data_dict = load_data()
wards = list(data_dict.keys()) if data_dict else ["Sayajigunj", "Alkapuri"]

# Sidebar
st.sidebar.header("Settings")
selected_ward = st.sidebar.selectbox("Select Ward", wards)

if selected_ward in data_dict and data_dict[selected_ward]["forecast_aqi"]:
    current_aqi = data_dict[selected_ward]["forecast_aqi"][0]
    st.sidebar.info(f"Current AQI in {selected_ward}: **{current_aqi}**")

# Main Content Tabs
tab1, tab2, tab3, tab4 = st.tabs(["🗺️ Map", "📈 Forecast", "🛠️ Intervention Simulator", "⚠️ Advisory"])

# --- TAB 1: MAP ---
with tab1:
    st.header("AQI Map")
    # Centered on Vadodara
    m = folium.Map(location=[22.3072, 73.1812], zoom_start=13)
    
    # Ward coordinates
    ward_coords = {
        "Sayajigunj": [22.3106, 73.1818],
        "Alkapuri": [22.3045, 73.1678]
    }
    
    # Dummy current AQI logic to color markers
    def get_color(aqi):
        if aqi <= 50: return 'green'
        elif aqi <= 100: return 'lightgreen'
        elif aqi <= 200: return 'orange'
        elif aqi <= 300: return 'red'
        else: return 'darkred'

    for ward_name, coords in ward_coords.items():
        # Get first forecast point as current AQI if available
        if ward_name in data_dict and data_dict[ward_name]["forecast_aqi"]:
            aqi = data_dict[ward_name]["forecast_aqi"][0]
        else:
            aqi = 100 # Default fallback
            
        folium.Marker(
            location=coords,
            popup=f"{ward_name}: {aqi} AQI",
            tooltip=ward_name,
            icon=folium.Icon(color=get_color(aqi))
        ).add_to(m)

    st_folium(m, width=800, height=500)

# --- TAB 2: FORECAST ---
with tab2:
    st.header(f"AQI Forecast for {selected_ward}")
    
    if selected_ward in data_dict:
        ward_data = data_dict[selected_ward]
        
        # Metric Cards
        col1, col2, col3 = st.columns(3)
        col1.metric("Model RMSE", f"{ward_data.get('rmse_model', 0):.2f}")
        col2.metric("Baseline RMSE", f"{ward_data.get('rmse_baseline', 0):.2f}")
        col3.metric("Current AQI", f"{ward_data['forecast_aqi'][0]}")
        
        # Line Chart
        df = pd.DataFrame({
            "Time": pd.to_datetime(ward_data["timestamps"]),
            "Forecast AQI": ward_data["forecast_aqi"],
            "Baseline AQI": ward_data["baseline_aqi"]
        }).set_index("Time")
        
        st.line_chart(df)
    else:
        st.warning("Data not available for this ward.")

# --- TAB 3: INTERVENTION Simulator ---
with tab3:
    st.header("Intervention Simulator")
    st.write("Simulate the impact of reducing traffic or construction activity.")
    
    reduction_percent = st.slider("Activity Reduction (%)", min_value=0, max_value=100, value=20, step=5)
    
    if selected_ward in data_dict:
        ward_data = data_dict[selected_ward]
        simulated_forecast = simulate_intervention(ward_data["forecast_aqi"], reduction_percent)
        
        df_sim = pd.DataFrame({
            "Time": pd.to_datetime(ward_data["timestamps"]),
            "Original Forecast": ward_data["forecast_aqi"],
            "Simulated Forecast": simulated_forecast
        }).set_index("Time")
        
        st.line_chart(df_sim)
        st.success(f"Simulating a {reduction_percent}% reduction in emissions.")
    else:
        st.warning("Data not available.")

# --- TAB 4: ADVISORY ---
with tab4:
    st.header("Health Advisory")
    
    # Determine risk level based on current AQI
    if selected_ward in data_dict and data_dict[selected_ward]["forecast_aqi"]:
        aqi = data_dict[selected_ward]["forecast_aqi"][0]
    else:
        aqi = 100
        
    def get_aqi_badge(aqi_val):
        if aqi_val <= 50:
            return f'<span style="background-color: #28a745; color: white; padding: 0.2em 0.6em; border-radius: 0.25rem; font-weight: bold;">{aqi_val} - Good</span>'
        elif aqi_val <= 100:
            return f'<span style="background-color: #ffc107; color: black; padding: 0.2em 0.6em; border-radius: 0.25rem; font-weight: bold;">{aqi_val} - Moderate</span>'
        elif aqi_val <= 150:
            return f'<span style="background-color: #fd7e14; color: white; padding: 0.2em 0.6em; border-radius: 0.25rem; font-weight: bold;">{aqi_val} - Unhealthy for Sensitive Groups</span>'
        elif aqi_val <= 200:
            return f'<span style="background-color: #dc3545; color: white; padding: 0.2em 0.6em; border-radius: 0.25rem; font-weight: bold;">{aqi_val} - Unhealthy</span>'
        elif aqi_val <= 300:
            return f'<span style="background-color: #6f42c1; color: white; padding: 0.2em 0.6em; border-radius: 0.25rem; font-weight: bold;">{aqi_val} - Very Unhealthy</span>'
        else:
            return f'<span style="background-color: #721c24; color: white; padding: 0.2em 0.6em; border-radius: 0.25rem; font-weight: bold;">{aqi_val} - Hazardous</span>'

    badge_html = get_aqi_badge(aqi)
    st.markdown(f"### Risk Level: {badge_html}", unsafe_allow_html=True)
    
    st.subheader("English Advisory (Placeholder)")
    st.info("The air quality is currently at a level where it is advised to limit prolonged outdoor exertion if you have respiratory issues. Keep windows closed during peak traffic hours.")
    
    st.subheader("ગુજરાતી સલાહ (Placeholder)")
    st.info("હાલમાં હવાની ગુણવત્તા એવા સ્તરે છે કે જો તમને શ્વસનની સમસ્યા હોય તો લાંબા સમય સુધી બહાર રહેવાનું ટાળવાની સલાહ આપવામાં આવે છે. ટ્રાફિકના સમયે બારીઓ બંધ રાખો.")
