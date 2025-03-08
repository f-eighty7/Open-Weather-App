import pytest

from src.main import (
    kelvin_to_celsius_fahrenheit,
    extract_weather_details,
    format_weather_report
)

def test_kelvin_to_celsius_fahrenheit():
    """
    Test temperature conversion function.
    """
    result = kelvin_to_celsius_fahrenheit(300)
    assert result["C"] == 26.85
    assert result["F"] == 80.33

def test_extract_weather_details():
    """
    Test extracting weather details from a sample API response.
    """
    sample_data = {
        "name": "Stockholm",
        "main": {"humidity": 70},
        "weather": [{"description": "clear sky"}]
    }
    city, humidity, description = extract_weather_details(sample_data)
    
    assert city == "Stockholm"
    assert humidity == 70
    assert description == "clear sky"

def test_format_weather_report():
    """
    Test formatting the weather report.
    """
    temperatures = {"temp": {"C": 20, "F": 68}, "feels_like": {"C": 18, "F": 64}}
    report = format_weather_report("Stockholm", 70, "clear sky", temperatures, "C")

    assert "Weather in Stockholm: clear sky" in report
    assert "Temperature: 20°C" in report
    assert "Feels like: 18°C" in report
    assert "Humidity: 70%" in report
