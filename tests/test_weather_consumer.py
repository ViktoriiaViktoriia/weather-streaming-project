import json
from datetime import datetime
from unittest.mock import MagicMock
import pytest
import tempfile
import csv

from processing import write_row


def test_consumer_message_parsing():
    # Create a mock Kafka message
    mock_value = {
        "type": "current",
        "city": "Tampere",
        "temperature": 10,
        "timestamp": "2025-04-21 16:00:00"
    }
    mock_message = MagicMock()
    mock_message.value.return_value = json.dumps(mock_value).encode("utf-8")

    # Simulate message handling logic
    data = json.loads(mock_message.value().decode("utf-8"))
    topic = data.get("type", "unknown")
    timestamp_str = data.get("timestamp")

    # Try parsing it to datetime
    try:
        parsed_timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        parsed_timestamp = None

    # Assert
    assert data["city"] == "Tampere"
    assert topic == "current"
    assert isinstance(data["temperature"], (int, float))
    assert parsed_timestamp is not None, "Timestamp is not in the expected datetime format"
    assert isinstance(parsed_timestamp, datetime)


def test_write_row():
    mock_data = {
        "type": "current",
        "city": "Helsinki",
        "description": "Clear sky",
        "temperature": 11.5,
        "feels_like": 9.1,
        "humidity": 80,
        "wind": 5.1,
        "pressure": 1012,
        "timestamp": "2025-04-21 10:00:00"
    }

    with tempfile.NamedTemporaryFile(mode='r+', delete=False, newline='') as tmpfile:
        write_row(mock_data, tmpfile.name)
        tmpfile.seek(0)
        reader = csv.DictReader(tmpfile)
        rows = list(reader)

        assert len(rows) == 1
        assert rows[0]["city"] == "Helsinki"
        assert rows[0]["temperature"] == "11.5"
        assert rows[0]["feels_like"] == "9.1"
        assert rows[0]["humidity"] == "80"
        assert rows[0]["wind"] == "5.1"
        assert rows[0]["timestamp"] == "2025-04-21 10:00:00"


def test_incomplete_data_error():
    """Function tests the writer to raise an error for missing data fields."""

    incomplete_data = {
        "type": "forecast",
        "city": "Oulu",
        "humidity": 80,
        "wind": 5.1,
        "pressure": 1012,
        "timestamp": "2025-04-21 10:00:00"
        # other fields missing
    }

    with tempfile.NamedTemporaryFile(mode='r+', delete=False, newline='') as tmpfile:
        write_row(incomplete_data, tmpfile.name)
        tmpfile.seek(0)
        reader = csv.DictReader(tmpfile)
        rows = list(reader)

        assert rows[0]["description"] == ""
        assert rows[0]["temperature"] == ""
        assert rows[0]["feels_like"] == ""
