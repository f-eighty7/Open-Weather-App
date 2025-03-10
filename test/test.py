import pytest
from unittest.mock import patch, MagicMock
from src.main import (
    kelvin_to_celsius_fahrenheit,
    extract_weather_details,
    format_weather_report,
    get_temperature_unit,
    fetch_weather_data,
    main
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


@pytest.mark.parametrize("mock_input, expected", [
    ("C", "C"),
    ("F", "F")
])
def test_get_temperature_unit_valid(monkeypatch, mock_input, expected):
    """
    Test user input for selecting temperature unit using monkeypatch (valid input).
    """
    monkeypatch.setattr("builtins.input", lambda _: mock_input)
    assert get_temperature_unit() == expected


def test_get_temperature_unit_invalid(monkeypatch, capsys):
    """
    Test user input for invalid cases to ensure loop retries.
    """
    inputs = iter(["X", "Y", "C"])  # Simulate entering "X", then "Y", then finally "C"
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    result = get_temperature_unit()
    captured = capsys.readouterr()

    assert "Invalid choice" in captured.out
    assert result == "C"


@pytest.mark.parametrize("status_code, expected", [
    (200, {"name": "Stockholm", "main": {"humidity": 70}, "weather": [{"description": "clear sky"}]}),
    (401, {"error": "Invalid API key"}),
    (404, {"error": "Country/City not found"}),
    (500, {"error": "An unexpected error occurred"})
])
@patch("requests.get")
def test_fetch_weather_data(mock_get, status_code, expected):
    """
    Test API fetch function under various conditions.
    """
    mock_response = MagicMock()
    mock_response.status_code = status_code
    mock_response.ok = status_code == 200
    mock_response.json.return_value = expected if status_code == 200 else {}

    mock_get.return_value = mock_response

    result = fetch_weather_data("Stockholm")
    assert result == expected


# ✅ Mocking the Full `main()` Execution
@patch("builtins.input", side_effect=["Stockholm", "C"])  # Simulate user entering "Stockholm" then "C"
@patch("builtins.print")  # Mock print to capture output
@patch("src.main.fetch_weather_data")
def test_main(mock_fetch, mock_print, mock_input):
    """
    Test the main function with mocked input and output.
    """
    # Mock successful API response
    mock_fetch.return_value = {
        "name": "Stockholm",
        "main": {"temp": 293.15, "feels_like": 290.15, "humidity": 75},
        "weather": [{"description": "partly cloudy"}]
    }

    main()  # Run main()

    # Ensure the expected print statement was called
    expected_output = """
🌍 Weather in Stockholm: partly cloudy
🌡️ Temperature: 20.0°C
🤔 Feels like: 17.0°C
💧 Humidity: 75%
    """.strip()  # Strip leading/trailing spaces to match actual output

    # Convert mock print call args to string
    actual_calls = "\n".join([call.args[0] for call in mock_print.call_args_list])

    # Assert that expected output exists within actual print calls
    assert expected_output in actual_calls
