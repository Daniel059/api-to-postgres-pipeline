import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL


# loading key-value pairs ffrom the .env into memory
load_dotenv()
def get_db_engine():
    """
    Constructs a SQLAlchemy database connection URL using environment variables for security. 
    
    The engine manages connection pooling and handles communication between 
    python and the postgresql database driver (psycopg2). The connection URL is constructed using the following environment variables:
    - DB_USER: The username for the database connection.
    """
    # URL.create security builds tthe connection string 
    connection_url = URL.create(
    drivername="postgresql+psycopg2",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    database=os.getenv("DB_NAME"),
)
# returning the engine object to be used for database operations
    return create_engine(connection_url)



# Writing to postgresql db
def load_to_postgres(df: pd.DataFrame, table_name: str = "east_africa_weather") -> None:
    """Args:
        df (pd.DataFrame): _description_
        table_name (str, optional): _description_. Defaults to "east_africa_weather".
    """
    # Stop execution if there is no data to load
    if df.empty:
        print("[WARNING] DataFrame is empty. Skipping database load.")
        return 
    try:
        # ontaining connection engine
        engine = get_db_engine()
        
        # to_sql handles table creation(if missing) and blunk row insertion
        df.to_sql(
            name=table_name,
            con=engine,
            if_exists="append",
            index=False,
        )
        print(f"[INFO] Succesfully loaded {len(df)} rows into table '{table_name}'.")
    except Exception as e:
        # catch and log database execution errors (e.g., Connection refused, bad credentials)
        print(f"[Error] Database load Failed: {e}")
        raise

if __name__ == "__main__":
    # Integration test for the Complete ETL
    from extract import extract_all_east_africa
    from transform import transform_weather_data
    
    print("[INFO] Intiationg End-to-End Local Pipeline Test...")
    
    # 1: Extract 
    raw_data = extract_all_east_africa()
    
    # 2: Transormation
    transformed_df = transform_weather_data(raw_data)
    
    # 3: Load
    load_to_postgres(transformed_df)
    