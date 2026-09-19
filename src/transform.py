import pandas as pd


def transform_weather_data(raw_records: list) -> pd.DataFrame:
    """Transforms raw API JSON payloads into a clean, normalized Pandas DataFrame."""
    if not raw_records:
        print("[WARNING] No records provided for transformation.")
        return pd.DataFrame()

    extracted_rows = []

    for item in raw_records:
        # Extract the nested 'current_weather' sub-dictionary
        current = item.get("current_weather", {})

        row = {
            "country": item.get("country"),
            "city": item.get("city"),
            "latitude": item.get("latitude"),
            "longitude": item.get("longitude"),
            "elevation_meters": item.get("elevation"),
            "recorded_at": current.get("time"),
            "temperature_celsius": current.get("temperature"),
            "windspeed_kmh": current.get("windspeed"),
            "wind_direction_degrees": current.get("winddirection"),
            "is_day": bool(current.get("is_day")),
            "weather_code": current.get("weathercode"),
        }
        extracted_rows.append(row)

    # Convert list of structured dictionaries into a DataFrame
    df = pd.DataFrame(extracted_rows)

    # Convert timestamp string to native pandas datetime
    df["recorded_at"] = pd.to_datetime(df["recorded_at"])

    # Ensure explicit schema types for analytical precision
    df = df.astype(
        {
            "country": "string",
            "city": "string",
            "latitude": "float64",
            "longitude": "float64",
            "elevation_meters": "float64",
            "temperature_celsius": "float64",
            "windspeed_kmh": "float64",
            "wind_direction_degrees": "int64",
            "is_day": "bool",
            "weather_code": "int64",
        }
    )

    return df


if __name__ == "__main__":
    # Integration test combining Extract and Transform locally
    from extract import extract_all_east_africa

    print("[INFO] Running Extraction...")
    raw_data = extract_all_east_africa()

    print("\n[INFO] Running Transformation...")
    df_clean = transform_weather_data(raw_data)

    print("\n[INFO] Transformed DataFrame Schema & Output:")
    print(df_clean.info())
    print("\n", df_clean)