import sys
from datetime import datetime
from dotenv import load_dotenv
from weather_api_pull.fetch_weather_data import fetch_weather_data
from weather_api_pull.insert_records import *

def main(city, drop_table=False) :
    
    weather_data = fetch_weather_data(city)
    print(f"Data fetched at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    try:
        if drop_table:
            print("Dropping existing 'weather_data' table if it exists...")
            drop_weather_table()
        # Connect to the database
        create_weather_table()
        # Insert the fetched data into the database
        insert_weather_data(weather_data)
    except Error as e:
        print(f"Error inserting data: {e}")
    finally:
        print("Data insertion completed.")
    