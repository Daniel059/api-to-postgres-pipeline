import time
from src.extract import extract_all_east_africa
from src.transform import transform_weather_data
from src.load import load_to_postgres

def run_pipeline():
    """
    Executes the end to end East Africa Waether ETL pipeline:
    1. Extarct raw weather data from Open-Meteo API across 8 East African countries/Capitals
    2. Transforms and normalizes raw JSON into a structured Pandas DataFrame
    3. Loads the transformed data into a PostgreSQL database
    """
    print("="*60)
    print("STARTING EAST AFRICA WEATHER ETL PIPELINE")
    print("="*60)

    start_time = time.time()
    
    # 1: Extraction
    print("\n[PHASE 1/3] Extracting raw waether data...")
    raw_records = extract_all_east_africa()
    
    if not raw_records:
        print("[CRITICAL] Extraction failed to retrieve records. Terminating pipeline.")
        return
    
    # 2: Transformation
    print("\n[PHASE 2/3] Transforming and normalizing dataset...")
    cleaned_df = transform_weather_data(raw_records)
    
    if cleaned_df.empty:
        print("[CRITICAL] Transformation resulted in an empty DataFrame. Terminating pipeline.")
        return
    
    # 3: Loading
    print("\n[PHASE 3/3] Loading transformed data into PostgreSQL database")
    load_to_postgres(cleaned_df)
    elapsed_time = round(time.time() - start_time, 2)
    print("\n"+ "="*60)
    print(f"ETL PIPELINE EXECUTION TIME: {elapsed_time} seconds.")
    print("="*60)

if __name__ == "__main__":
    run_pipeline()