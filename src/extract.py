import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("API_BASE_URL")

# Target locations across East Africa
EAST_AFRICAN_CAPITALS = [
    {"country": "Kenya", "city": "Nairobi", "latitude": -1.286389, "longitude": 36.817223},
    {"country": "Uganda", "city": "Kampala", "latitude": 0.313611, "longitude": 32.581111},
    {"country": "Tanzania", "city": "Dodoma", "latitude": -6.173056, "longitude": 35.741944},
    {"country": "Rwanda", "city": "Kigali", "latitude": -1.944072, "longitude": 30.061885},
    {"country": "Burundi", "city": "Gitega", "latitude": -3.42735, "longitude": 29.9246},
    {"country": "South Sudan", "city": "Juba", "latitude": 4.851667, "longitude": 31.5825},
    {"country": "DR Congo", "city": "Kinshasa", "latitude": -4.32758, "longitude": 15.31357},
    {"country": "Somalia", "city": "Mogadishu", "latitude": 2.046934, "longitude": 45.318161},
]


def fetch_weather_for_location(lat: float, lon: float) -> dict:
    """Fetches weather metrics for a specific coordinate set."""
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": "true"
    }
    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to extract data for coordinates ({lat}, {lon}): {e}")
        return {}


def extract_all_east_africa() -> list:
    """Iterates through all defined EA capitals and retrieves weather payloads."""
    raw_records = []
    
    for loc in EAST_AFRICAN_CAPITALS:
        print(f"[INFO] Extracting weather data for {loc['city']}, {loc['country']}...")
        payload = fetch_weather_for_location(loc["latitude"], loc["longitude"])
        
        if payload:
            # Inject regional context into raw metadata before downstream processing
            payload["country"] = loc["country"]
            payload["city"] = loc["city"]
            raw_records.append(payload)
            
    return raw_records


if __name__ == "__main__":
    records = extract_all_east_africa()
    print(f"\n[INFO] Successfully extracted {len(records)} records across East Africa.")
    if records:
        print("[INFO] Sample extracted payload (First record):")
        print(records[0])