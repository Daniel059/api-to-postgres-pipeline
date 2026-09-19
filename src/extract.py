import os
import requests
from dotenv import load_dotenv

# Load environment variables from the root .env file into memory
load_dotenv()

# Retrieve the base API URL configured in .env to prevent hardcoding endpoints
BASE_URL = os.getenv("API_BASE_URL")

# Static configuration list containing metadata and coordinates for East African capitals
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
    """
    Sends an HTTP GET request to the Open-Meteo REST API for a specific set of coordinates.
    
    Args:
        lat (float): Latitude of the target location.
        lon (float): Longitude of the target location.
        
    Returns:
        dict: Raw JSON response parsed as a Python dictionary, or empty dict on failure.
    """
    # Define query parameters required by the API endpoint
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": "true"  # Requests real-time observation metrics
    }
    
    try:
        # Issue HTTP GET request with a strict 10-second timeout to prevent hanging connections
        response = requests.get(BASE_URL, params=params, timeout=10)
        
        # Raise HTTPError exception if response code indicates failure (4xx or 5xx)
        response.raise_for_status()
        
        # Parse JSON response body into a Python dictionary
        return response.json()
        
    except requests.exceptions.RequestException as e:
        # Catch connection failures, timeouts, or bad HTTP status codes gracefully
        print(f"[ERROR] Failed to extract data for coordinates ({lat}, {lon}): {e}")
        return {}


def extract_all_east_africa() -> list:
    """
    Iterates through all predefined East African capitals, invokes the API fetch function,
    and enriches each response payload with country and city metadata.
    
    Returns:
        list: Collection of raw API dictionaries enriched with location metadata.
    """
    raw_records = []
    
    for loc in EAST_AFRICAN_CAPITALS:
        print(f"[INFO] Extracting weather data for {loc['city']}, {loc['country']}...")
        
        # Fetch weather data for current capital coordinates
        payload = fetch_weather_for_location(loc["latitude"], loc["longitude"])
        
        if payload:
            # Inject location context directly into payload prior to downstream ingestion
            payload["country"] = loc["country"]
            payload["city"] = loc["city"]
            raw_records.append(payload)
            
    return raw_records


if __name__ == "__main__":
    # Local execution block for module verification and sanity testing
    records = extract_all_east_africa()
    print(f"\n[INFO] Successfully extracted {len(records)} records across East Africa.")
    
    if records:
        print("[INFO] Sample extracted payload (First record):")
        print(records[0])