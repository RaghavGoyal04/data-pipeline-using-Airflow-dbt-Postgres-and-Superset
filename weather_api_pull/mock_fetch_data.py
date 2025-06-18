import json
data_str = """
    {
        "coord": {
            "lon": -0.1257,
            "lat": 51.5085
        },
        "weather": [
            {
                "id": 800,
                "main": "Clear",
                "description": "clear sky",
                "icon": "01d"
            }
        ],
        "base": "stations",
        "main": {
            "temp": 296.65,
            "feels_like": 296.33,
            "temp_min": 295.98,
            "temp_max": 297.6,
            "pressure": 1016,
            "humidity": 49,
            "sea_level": 1016,
            "grnd_level": 1012
        },
        "visibility": 10000,
        "wind": {
            "speed": 7.72,
            "deg": 210
        },
        "clouds": {
            "all": 2
        },
        "dt": 1749911792,
        "sys": {
            "type": 2,
            "id": 2075535,
            "country": "GB",
            "sunrise": 1749872575,
            "sunset": 1749932328
        },
        "timezone": 3600,
        "id": 2643743,
        "name": "London",
        "cod": 200
    }
    """


def mock_fetch_data():
    """
    Mock function to simulate fetching weather data.
    Returns a JSON string that mimics the structure of the actual API response.
    """
    return json.loads(data_str)