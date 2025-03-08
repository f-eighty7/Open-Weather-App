# 🌦️ Weather App

A simple Python command-line application that fetches real-time weather data from OpenWeatherMap API and displays it in a user-friendly format.

## 🚀 Features
- Fetches live weather data for any city/country.
- Converts temperature between **Celsius** and **Fahrenheit**.
- Displays weather **description, temperature, and humidity**.
- Uses **environment variables** to secure API keys.
- Implements **error handling** for missing API keys or incorrect locations.

## 📌 Prerequisites
Ensure you have Python **3.x** installed.

Install required dependencies:
```sh
pip install -r requirements.txt
```

## 🔧 Setup & Configuration
1️⃣ **Create a `.env` file** in the project root:
```
WEATHER_API_KEY=your_actual_api_key_here
```

2️⃣ **Ensure `.env` is ignored by Git** (in `.gitignore`):
```
.env
```

3️⃣ **Run the application**:
```sh
python src/main.py
```

## 🛠️ How It Works
1. Prompts the user to enter a **city or country**.
2. Fetches weather data from OpenWeatherMap API.
3. Asks the user to choose between **Celsius (C) or Fahrenheit (F)**.
4. Displays a formatted weather report:
```
🌍 Weather in Stockholm: Clear Sky
🌡️ Temperature: 8.9°C
🤔 Feels like: 6.85°C
💧 Humidity: 73%
```

## ✅ Testing
Run **pytest** to test the application:
```sh
pytest --cov=src.main --cov-report=html
```
Check the **HTML coverage report**:
```sh
open htmlcov/index.html
```

## 🔍 Linting & Code Quality
Ensure clean, well-formatted code with:
```sh
pylint src/main.py
```
To auto-format using `autopep8`:
```sh
autopep8 --in-place --aggressive --aggressive src/main.py
```

## 📌 Technologies Used
- **Python 3.x**
- **Requests** (API calls)
- **dotenv** (environment variable management)
- **pytest** (unit testing & coverage)
- **pylint & autopep8** (code quality & formatting)

## ⚡ Future Improvements
- Add **GUI or Web Interface** using Flask or Tkinter.
- Support for **hourly & weekly weather forecasts**.
- Integration with **multiple weather APIs**.

---

Made with ❤️ by **F-Eighty7** 🚀

