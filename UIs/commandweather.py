import requests
import argparse
from gooey import Gooey, GooeyParser


def read_api_key():
    """Reads the API key from a hardcoded file path."""
    try:
        with open('commandweather.conf', 'r') as file:
            return file.readline().strip(
            )  # Read the first line and strip any extra whitespace
    except FileNotFoundError:
        return "API key file not found."
    except Exception as e:
        return str(e)


def get_weather(city, api_key):
    """Fetches the current weather for the specified city using OpenWeatherMap API."""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather = data['weather'][0]['description']
        temperature = data['main']['temp']
        return f"The current weather in {city} is {weather} with a temperature of {temperature}°C."
    else:
        return "Failed to retrieve weather data."

@Gooey
def main():
    #parser = argparse.ArgumentParser(description='Get the current weather for a city.')
    parser = GooeyParser(description='Get the current weather for a city.')

    parser.add_argument('city',
                        type=str,
                        help='Name of the city to fetch the weather for.')
    args = parser.parse_args()

    api_key = read_api_key()
    if api_key.startswith("API key"):
        print(api_key)  # Print error message if any
        return

    weather_report = get_weather(args.city, api_key)
    print(weather_report)


if __name__ == "__main__":
    main()
