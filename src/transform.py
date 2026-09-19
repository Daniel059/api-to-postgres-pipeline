import pandas as pd


def transform_weather_data(raw_records: list) -> pd.DataFrame:
    """
    Transforms raw, nested API JSON payloads into a clean, normalized Pandas DataFrame.
    Performs field flattening, column renaming, timestamp parsing, and strict schema enforcement.
    
    Args:
        raw_records (list): List of enriched API JSON payloads returned from extract module.
        
    Returns:
        pd.DataFrame: Structured, typed tabular dataset ready for database loading.
    """
    # Guard clause against empty input lists
    if not raw_records:
        print("[WARNING] No records provided for transformation.")
        return pd.DataFrame()

    extracted_rows = []

    # Flatten nested JSON objects into a single flat dictionary per location
    for item in raw_records:
        # Extract the nested 'current_weather' sub-dictionary safely using .get()
        current = item.get("current_weather", {})

        row = {
            # Metadata fields from payload root
            "country": item.get("country"),
            "city": item.get("city"),
            "latitude": item.get("latitude"),
            "longitude": item.get("longitude"),
            "elevation_meters": item.get("elevation"),
            
            # Metrics un-nested from 'current_weather' dictionary with descriptive unit names
            "recorded_at": current.get("time"),
            "temperature_celsius": current.get("temperature"),
            "windspeed_kmh": current.get("windspeed"),
            "wind_direction_degrees": current.get("winddirection"),
            "is_day": bool(current.get("is_day")),  # Convert binary flag (0/1) to boolean
            "weather_code": current.get("weathercode"),
        }
        extracted_rows.append(row)

    # Instantiate Pandas DataFrame from the list of normalized row dictionaries
    df = pd.DataFrame(extracted_rows)

    # Parse ISO-8601 string timestamps into native pandas datetime objects for SQL TIMESTAMP compatibility
    df["recorded_at"] = pd.to_datetime(df["recorded_at"])

    # Explicitly enforce SQL-compatible data types to prevent runtime loading errors
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
    # Integration test combining extraction and transformation modules locally
    from extract import extract_all_east_africa

    print("[INFO] Running Extraction...")
    raw_data = extract_all_east_africa()

    print("\n[INFO] Running Transformation...")
    df_clean = transform_weather_data(raw_data)

    print("\n[INFO] Transformed DataFrame Schema & Output:")
    print(df_clean.info())
    print("\n", df_clean)