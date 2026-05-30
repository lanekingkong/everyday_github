"""
Beautiful Terminal Weather App — ASCII art weather display.
Uses Open-Meteo API (free, no key required) for weather data.
"""
import json
import urllib.request
import urllib.parse
from datetime import datetime


WEATHER_CODES = {
    0: ("☀️  Clear sky", ""),
    1: ("🌤️  Mainly clear", ""),
    2: ("⛅ Partly cloudy", ""),
    3: ("☁️  Overcast", ""),
    45: ("🌫️  Foggy", ""),
    48: ("🌫️  Rime fog", ""),
    51: ("🌧️  Light drizzle", ""),
    53: ("🌧️  Moderate drizzle", ""),
    55: ("🌧️  Dense drizzle", ""),
    61: ("🌧️  Slight rain", ""),
    63: ("🌧️  Moderate rain", ""),
    65: ("🌧️  Heavy rain", ""),
    71: ("🌨️  Slight snow", ""),
    73: ("🌨️  Moderate snow", ""),
    75: ("🌨️  Heavy snow", ""),
    80: ("🌦️  Rain showers", ""),
    95: ("⛈️  Thunderstorm", ""),
}


def geocode(city: str) -> tuple:
    """Get coordinates for a city name using Open-Meteo geocoding API."""
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={urllib.parse.quote(city)}&count=1&language=en&format=json"
    try:
        with urllib.request.urlopen(url) as resp:
            data = json.loads(resp.read())
        if data.get("results"):
            r = data["results"][0]
            return r["latitude"], r["longitude"], r["name"], r.get("country", "")
    except Exception as e:
        print(f"Geocoding error: {e}")
    return None, None, city, ""


def fetch_weather(lat: float, lon: float) -> dict:
    """Fetch current + 5-day forecast from Open-Meteo."""
    params = urllib.parse.urlencode({
        "latitude": lat, "longitude": lon,
        "current": "temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m,wind_direction_10m",
        "daily": "temperature_2m_max,temperature_2m_min,weather_code,precipitation_sum",
        "timezone": "auto",
        "forecast_days": "5",
    })
    url = f"https://api.open-meteo.com/v1/forecast?{params}"
    with urllib.request.urlopen(url) as resp:
        return json.loads(resp.read())


def wind_direction_arrow(degrees: int) -> str:
    arrows = ["↓", "↙", "←", "↖", "↑", "↗", "→", "↘"]
    idx = round(degrees / 45) % 8
    return arrows[idx]


def display(data: dict, city: str, country: str):
    current = data["current"]
    daily = data["daily"]

    code = current["weather_code"]
    weather_desc, _ = WEATHER_CODES.get(code, (f"Code {code}", ""))

    # Current conditions box
    print(f"""
╔══════════════════════════════════════════════╗
║  🌍 {city}, {country}
║  📅 {datetime.now().strftime('%A, %B %d %Y  %H:%M')}
╠══════════════════════════════════════════════╣
║                                              ║
║     {weather_desc:<35}║
║     🌡️  Temperature:    {current['temperature_2m']:>5.1f}°C          ║
║     🥶 Feels like:      {current['apparent_temperature']:>5.1f}°C          ║
║     💧 Humidity:        {current['relative_humidity_2m']:>5}%           ║
║     💨 Wind:            {current['wind_speed_10m']:>5.1f} km/h {wind_direction_arrow(current['wind_direction_10m']):>3}     ║
║                                              ║
╚══════════════════════════════════════════════╝
""")

    # Forecast
    print("📅 5-Day Forecast:")
    print("─" * 55)
    print(f"{'Date':<14} {'High':>6} {'Low':>6} {'Rain':>6}  Condition")
    print("─" * 55)
    for i in range(5):
        date = daily["time"][i]
        high = daily["temperature_2m_max"][i]
        low = daily["temperature_2m_min"][i]
        rain = daily["precipitation_sum"][i]
        code = daily["weather_code"][i]
        desc, _ = WEATHER_CODES.get(code, ("?", ""))
        print(f"{date:<14} {high:>5.1f}° {low:>5.1f}° {rain:>5.1f}mm {desc}")
    print("─" * 55)
    print()


if __name__ == "__main__":
    import sys
    city = sys.argv[1] if len(sys.argv) > 1 else "Beijing"
    print(f"\n🔍 Searching for {city}...")
    lat, lon, city_name, country = geocode(city)
    if lat is None:
        print(f"❌ City not found: {city}")
        sys.exit(1)
    print(f"📍 Found: {city_name}, {country} ({lat:.2f}, {lon:.2f})")
    print("📡 Fetching weather data...")
    data = fetch_weather(lat, lon)
    display(data, city_name, country)
