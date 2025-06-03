import requests
import json
from datetime import datetime

class WeatherDashboard:
    def __init__(self, api_key, history_file="weather_history.json"):
        self.api_key = api_key
        self.history_file = history_file
        self.history = self.load_history()

    def load_history(self):
        """Load the search history from the JSON file."""
        try:
            with open(self.history_file, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_history(self):
        """Save the search history to the JSON file."""
        with open(self.history_file, 'w') as file:
            json.dump(self.history, file, indent=4)

    def fetch_weather_data(self, city):
        """Fetch live weather data from OpenWeatherMap API."""
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}&units=metric"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise HTTPError for bad responses
            data = response.json()
            return data
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return None

    def show_weather(self, city):
        """Display the weather for a given city."""
        data = self.fetch_weather_data(city)
        if data:
            city_name = data["name"]
            country = data["sys"]["country"]
            temp = data["main"]["temp"]
            weather_description = data["weather"][0]["description"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]

            print(f"\nWeather for {city_name}, {country}:")
            print(f"Temperature: {temp}°C")
            print(f"Condition: {weather_description.capitalize()}")
            print(f"Humidity: {humidity}%")
            print(f"Wind Speed: {wind_speed} m/s")

            # Save the city to history
            self.history.append({"city": city_name, "timestamp": str(datetime.now())})
            self.save_history()
        else:
            print("Couldn't fetch weather data.")

    def show_history(self):
        """Display the search history."""
        if not self.history:
            print("No search history found.")
            return

        print("\nSearch History:")
        for entry in self.history:
            print(f"City: {entry['city']} | Searched on: {entry['timestamp']}")

    def run(self):
        """Run the weather dashboard CLI."""
        while True:
            print("\n--- Weather Dashboard ---")
            print("1. Get Weather for a City")
            print("2. View Search History")
            print("3. Exit")
            try:
                choice = int(input("Enter your choice: "))
                if choice == 1:
                    city = input("Enter city name: ")
                    self.show_weather(city)
                elif choice == 2:
                    self.show_history()
                elif choice == 3:
                    print("Exiting the system...")
                    break
                else:
                    print("Invalid choice, please try again.")
            except ValueError:
                print("Please enter a valid number.")

# Main Program
if __name__ == "__main__":
    api_key = "your_openweathermap_api_key_here"  # Replace with your OpenWeatherMap API key
    weather_dashboard = WeatherDashboard(api_key)
    weather_dashboard.run()
