import requests
import requests_mock
import pytest
from unittest.mock import patch, call

from ingestion import fetch_weather, stream_weather_data


# Mock API response
MOCK_RESPONSE = {
    "weather": [{"description": "sunny"}],
    "main": {"temp": 3.5},
    "name": "Tampere",
}


def test_fetch_weather():
    """Test fetching current weather data. Function ensures the API call is made correctly and
    returns expected data."""

    city = "Tampere"
    url = "http://api.openweathermap.org/data/2.5/weather"

    with requests_mock.Mocker() as m:
        m.get(url, json=MOCK_RESPONSE, status_code=200)  # Simulate API response

        data = fetch_weather(url, city)  # Call function

        assert data is not None
        assert "weather" in data
        assert isinstance(data["weather"], list)
        assert "main" in data
        assert data["name"] == "Tampere"


@pytest.fixture
def mock_fetch_weather():
    with patch("ingestion.weather_producer.fetch_weather") as mock:
        mock.return_value = MOCK_RESPONSE
        yield mock


@patch("ingestion.weather_producer.time.sleep", return_value=None)
@patch("config.config.CITIES", ["Tampere"])
def test_stream_data_retries(mock_sleep, mock_fetch_weather):
    """  Test API failure and retry mechanism. Simulates a failed request and ensures retries work."""
    city = "Tampere"
    url = "http://api.openweathermap.org/data/2.5/weather"

    # Simulate failures first, then success
    mock_fetch_weather.side_effect = [
        requests.exceptions.RequestException("API Error")
    ] * 4 + [MOCK_RESPONSE]

    # Run stream function with the base URL
    stream_weather_data(url, city)

    # Expected calls: (url, city)
    expected_calls = [call(url, city)] * 5

    # Verify the actual calls match expected ones
    assert mock_fetch_weather.call_args_list == expected_calls
    assert mock_fetch_weather.call_count == 5
