from google import genai
import re
import json
import os

import requests
import time

def get_breathe_ahead_notices(api_key, ward, aqi, category, vulnerable_locs, source, confidence):
    prompt = f"""
    You are the AI Air Quality Coordinator for Vadodara Municipal Corporation (VMC).
    Data for current intervention:
    - Ward: {ward}
    - Forecasted AQI: {aqi} ({category})
    - Vulnerable Locations Nearby: {', '.join(vulnerable_locs)}
    - Primary Pollution Source: {source} (Confidence: {confidence}%)
    Please generate the following three components:
    1. Citizen Health Advisory (English): 2-3 actionable sentences in plain English for residents of this ward. Mention the vulnerable locations.
    2. Citizen Health Advisory (Gujarati): A natural-sounding translation of the above advisory.
    3. Municipal Enforcement Notice: A short, formal 2-3 sentence internal directive for municipal staff to mitigate the {source} in {ward} based on the {confidence}% confidence level.
    Format the output as follows:
    EN_ADVISORY: [text]
    GU_ADVISORY: [text]
    STAFF_NOTICE: [text]
    """

    models_to_try = ["gemini-3.5-flash", "gemini-flash-latest", "gemini-2.0-flash"]

    for model_name in models_to_try:
        for attempt in range(3):
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
                payload = {
                    "contents": [{"parts": [{"text": prompt}]}]
                }
                headers = {"Content-Type": "application/json"}
                
                response = requests.post(url, json=payload, headers=headers)
                
                if response.status_code == 200:
                    data = response.json()
                    text = data['candidates'][0]['content']['parts'][0]['text']
                    print(f"Success with model: {model_name}")
                    return text
                else:
                    print(f"{model_name} attempt {attempt+1} failed with status {response.status_code}: {response.text}")
                    time.sleep(4)
            except Exception as e:
                print(f"{model_name} attempt {attempt+1} failed: {e}")
                time.sleep(4)

    raise Exception("All models/retries failed")

def parse_and_save(raw_text, ward):
    en = re.search(r'EN_ADVISORY:\s*(.*?)(?=GU_ADVISORY:|$)', raw_text, re.DOTALL)
    gu = re.search(r'GU_ADVISORY:\s*(.*?)(?=STAFF_NOTICE:|$)', raw_text, re.DOTALL)
    staff = re.search(r'STAFF_NOTICE:\s*(.*)', raw_text, re.DOTALL)

    result = {
        "ward": ward,
        "advisory_en": en.group(1).strip() if en else "",
        "advisory_gu": gu.group(1).strip() if gu else "",
        "enforcement_notice": staff.group(1).strip() if staff else ""
    }

    with open('../data/advisory_output.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result

# --- Example Usage ---
API_KEY = os.environ.get("GEMINI_API_KEY", "").strip().strip('"').strip("'")
if not API_KEY:
    print("WARNING: Set GEMINI_API_KEY environment variable before running")

ward_name = "Sayajigunj"
aqi_val = 157
aqi_cat = "Poor"
vulnerable = ["Sayaji Hospital", "M.S. University Campus", "Kamati Baug"]
pollutant_source = "construction dust"
conf_level = 78

output = get_breathe_ahead_notices(
    API_KEY, ward_name, aqi_val, aqi_cat, vulnerable, pollutant_source, conf_level
)
parse_and_save(output, ward_name)