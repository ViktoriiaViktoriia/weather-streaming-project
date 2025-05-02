import pandas as pd

from processing import process_weather_data, insert_weather_data


def test_data_cleaning():
    """Function tests city name cleaned using .strip() and .title(), duplicates removal,
    Kelvin to Celsius conversion."""

    df = pd.DataFrame({
        "city": ["  helsinki", "  helsinki", "TAMPERE  ", "oulu "],
        "type": ["weather_current", "weather_current", "weather_current", "weather_current"],
        "timestamp": ["2024-01-01 12:00", "2024-01-01 12:00", 1713203988, "1713203987"],
        "temperature": [285, 285, 295, 290],   # Kelvin
        "feels_like": [280, 280, 285, 280]  # Kelvin
    })

    result = process_weather_data(df)
    print(result)

    assert result["city"].tolist() == ["Helsinki", "Tampere", "Oulu"]
    assert result.shape[0] == 3
    assert result["temperature"].round(2).tolist() == [11.85, 21.85, 16.85]
    assert result["feels_like"].round(2).tolist() == [6.85, 11.85, 6.85]


def test_insert_weather_data():
    df = pd.DataFrame({
        "type": ["weather_current", "weather_forecast"],
        "city": ["Helsinki", "Tampere"],
        "description": ["clear sky", "cloudy"],
        "temperature": [285.15, 280.32],
        "feels_like": [283.00, 279.00],
        "humidity": [60, 70],
        "wind": [3.2, 4.5],
        "pressure": [1012, 1015],
        "timestamp": ["2024-01-01 12:00:00", "2024-01-01 13:00:00"]
    })

    success = insert_weather_data(df)

    assert success is True
