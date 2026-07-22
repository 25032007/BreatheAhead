import json

def get_source_attribution(ward, dist_to_traffic_km, dist_to_construction_km, dist_to_industrial_km):
    sources = {
        "traffic": max(0, 100 - dist_to_traffic_km * 20),
        "construction": max(0, 100 - dist_to_construction_km * 25),
        "industrial": max(0, 100 - dist_to_industrial_km * 15)
    }
    dominant = max(sources, key=sources.get)
    confidence = round(sources[dominant])
    return {
        "ward": ward,
        "dominant_source": dominant,
        "confidence_score": confidence,
        "note": "Heuristic proximity-based scoring, not a trained ML model"
    }

# --- Example usage for Sayajigunj ---
# Distances are approximate — adjust based on real map estimates for your ward
result = get_source_attribution(
    ward="Sayajigunj",
    dist_to_traffic_km=1.5,
    dist_to_construction_km=0.9,
    dist_to_industrial_km=5.0
)

print(json.dumps(result, indent=2))

# Save output for Person B to use in the dashboard
with open('../data/attribution_output.json', 'w') as f:
    json.dump(result, f, indent=2)

print("\nSaved attribution_output.json")