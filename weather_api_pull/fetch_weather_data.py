import requests
import os
import json
import sys
from datetime import datetime
# from dotenv import load_dotenv

# load_dotenv('/opt/airflow/.env')

def fetch_weather_data(city):
    api_key = os.environ.get("WEATHER_API_KEY")
    if not api_key:
        print("Error: WEATHER_API_KEY not found in environment variables.")
        sys.exit(1)
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data.get("cod") != 200:
            print(f"Error: {data.get('message')}")
            sys.exit(1)
        return data
    else:
        print(f"Error: Unable to fetch data for {city}. HTTP Status Code: {response.status_code}")
        sys.exit(1)
