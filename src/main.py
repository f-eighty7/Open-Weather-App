"""
Weather App - Fetches weather data from OpenWeatherMap API and displays it.
"""
import os
import textwrap
from dotenv import load_dotenv
import requests

load_dotenv()
API = os.getenv("WEATHER_API_KEY")

def fetch_weather_data(country):
    """
    Fetch weather data from OpenWeatherMap API.

    Args:
        country (str): The name of the country or city to get the weather for.

    Returns:
        dict: Weather data if the request is successful.
        dict: Error message if the request fails (Invalid API key or City not found).
    """
    response = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q={country}&appid={API}",
        timeout=5)

    if response.ok:
        return response.json()
    if response.status_code == 401:
        return {"error": "Invalid API key"}
    if response.status_code == 404:
        return {"error": "Country/City not found"}
    return {"error": "An unexpected error occurred"}


def get_temperature_unit():
    """
    Prompt the user to select a temperature unit (Celsius or Fahrenheit).

    Returns:
        str: "C" for Celsius or "F" for Fahrenheit.
    """
    while True:
        temp_unit_choice = input(
            "Celsius or Fahrenheit? (Enter C or F): ").upper()
        if temp_unit_choice in ["C", "F"]:
            return temp_unit_choice
        print("Invalid choice, Please enter 'C' or 'F'. Try again")


def kelvin_to_celsius_fahrenheit(kelvin):
    """
    Convert temperature from Kelvin to Celsius and Fahrenheit.

    Args:
        kelvin (float): Temperature in Kelvin.

    Returns:
        dict: A dictionary with converted temperature values in Celsius and Fahrenheit.
    """
    return {
        "C": round(kelvin - 273.15, 2),
        "F": round((kelvin - 273.15) * 9 / 5 + 32, 2)
    }


def extract_weather_details(weather_data):
    """
    Extract key weather details from API response.

    Args:
        weather_data (dict): The weather data dictionary returned from the API.

    Returns:
        tuple: A tuple containing the city name (str), humidity (int),
        and weather description (str).
    """
    city_name = weather_data["name"]
    humidity_level = weather_data["main"]["humidity"]
    weather_desc = weather_data["weather"][0]["description"]
    return city_name, humidity_level, weather_desc


def format_weather_report(
        city_name,
        humidity_level,
        weather_desc,
        temperatures,
        temp_unit_choice):
    """
    Format the weather details into a readable report.

    Args:
        city_name (str): The name of the city.
        humidity_level (int): The humidity percentage.
        weather_desc (str): Short description of the weather conditions.
        temperatures (dict): A dictionary containing temperature values in Celsius and Fahrenheit.
        temp_unit_choice (str): "C" for Celsius, "F" for Fahrenheit.

    Returns:
        str: A formatted weather report as a string.
    """
    return textwrap.dedent(f"""
        🌍 Weather in {city_name}: {weather_desc}
        🌡️ Temperature: {temperatures['temp'][temp_unit_choice]}°{temp_unit_choice}
        🤔 Feels like: {temperatures['feels_like'][temp_unit_choice]}°{temp_unit_choice}
        💧 Humidity: {humidity_level}%
    """)


def main():
    """
    Main function to execute the weather application.
    """
    while True:
        location = fetch_weather_data(input("Enter Country or City: "))

        if "error" in location:
            print(location["error"])
            continue

        city_name, humidity_level, weather_desc = extract_weather_details(
            location)

        temperatures = {
            "temp": kelvin_to_celsius_fahrenheit(
                location["main"]["temp"]), "feels_like": kelvin_to_celsius_fahrenheit(
                location["main"]["feels_like"])}

        temp_unit_choice = get_temperature_unit()

        print(
            format_weather_report(
                city_name,
                humidity_level,
                weather_desc,
                temperatures,
                temp_unit_choice))

        break

if __name__ == "__main__":
    main()
