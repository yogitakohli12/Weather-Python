
import requests
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# Replace with your OpenWeatherMap API key
API_KEY = "47b95522253b614adfb1f3167f161654"
BASE_URL = "https://api.openweathermap.org/data/2.5/"

def get_weather_data(city):
    url = f"{BASE_URL}weather?q={city}&appid={API_KEY}&units=metric"
    
    forecast_url = f"{BASE_URL}forecast?q={city}&appid={API_KEY}&units=metric"
    try:
        weather_response = requests.get(url)
        forecast_response = requests.get(forecast_url)

        weather_data = weather_response.json()
        forecast_data = forecast_response.json()

        if weather_response.status_code != 200 or forecast_response.status_code != 200:
            messagebox.showerror("Error", weather_data.get("message", "Failed to fetch data"))
            return None, None

        return weather_data, forecast_data

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        return None, None

def display_weather():
    city = city_entry.get()
    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name")
        return

    weather_data, forecast_data = get_weather_data(city)

    if weather_data and forecast_data:
        # Display current weather
        current_temp = weather_data['main']['temp']
        weather_condition = weather_data['weather'][0]['description'].capitalize()
        humidity = weather_data['main']['humidity']
        pressure = weather_data['main']['pressure']
        sunrise = datetime.fromtimestamp(weather_data['sys']['sunrise']).strftime('%H PM:%M min')
        sunset = datetime.fromtimestamp(weather_data['sys']['sunset']).strftime('%H PM:%M min')

        current_weather_label.config(text=(
            f"~{current_temp}°C\n"
            f"City: ⛅{city}\n"
            f"Condition: 🌅 {weather_condition}\n"
            f"Humidity: 💧 {humidity}%\n"
            f"Pressure: 🕝 {pressure} hPa"
        ))

        sunriset_label.config(text=(
            f"{sunrise}                                  "
            f"{sunset}"
        ))

        

        # Clear existing cards
        for widget in forecast_frame.winfo_children():
            widget.destroy()

        # Extract forecasts grouped by day
        grouped_forecast = {}
        for entry in forecast_data['list']:
            date = entry['dt_txt'].split(' ')[0]
            if date not in grouped_forecast:
                grouped_forecast[date] = []
            grouped_forecast[date].append(entry)

        # Display next 5 days forecast as cards
        today = datetime.now().date()
        days_shown = 0
        for date_str, data_list in grouped_forecast.items():
            forecast_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            if forecast_date <= today:
                continue  # Skip today

            if days_shown >= 6:
                break

            # Get the average temperature and main condition
            avg_temp = sum(entry['main']['temp'] for entry in data_list) / len(data_list)
            main_condition = data_list[0]['weather'][0]['description'].capitalize()
            avg_humidity = sum(entry['main']['humidity'] for entry in data_list) / len(data_list)
            avg_pressure = sum(entry['main']['pressure'] for entry in data_list) / len(data_list)
            wind_speed = sum(entry['wind']['speed'] for entry in data_list) / len(data_list)
            day_name = forecast_date.strftime('%A')


# Determine the emoji based on the weather condition
            if "clear" in main_condition:
                emoji = "☀️"  # Sun for clear weather
            elif "cloud" in main_condition:
                emoji = "☁️"  # Cloud for cloudy weather
            elif "rain" in main_condition:
                emoji = "🌧️"  # Rain for rainy weather
            elif "snow" in main_condition:
                emoji = "❄️"  # Snow for snowy weather
            elif "storm" in main_condition:
                emoji = "🌩️"  # Storm for stormy weather
            else:
                emoji = "🌥️"  # Default for unknown weather


            # Create a card
            card_color = "black"
            card = tk.Frame(forecast_frame, bg=card_color, bd=1, relief="ridge", padx=50, pady=5)
            card.grid(row=days_shown // 3, column=days_shown % 3, padx=10, pady=10)

            fcfimg_label = tk.Label(card, text=emoji, font=("Arial", 25, "bold"),fg="white", bg=card_color)
            fcfimg_label.pack(pady=5)

            day_label = tk.Label(card, text=f"{day_name}", font=("Arial", 14, "bold"), fg="gold", bg=card_color)
            day_label.pack(pady=5)

            temp_label = tk.Label(card, text=f"~{avg_temp:.1f}°C", font=("Arial", 16), fg="white", bg=card_color)
            temp_label.pack(pady=5)

            condition_label = tk.Label(card, text=f"Condition: {main_condition}", font=("Arial", 10), fg="white", bg=card_color)
            condition_label.pack(pady=5)

            humidity_label = tk.Label(card, text=f"Humidity: {avg_humidity:.0f}%", font=("Arial", 10), fg="white", bg=card_color)
            humidity_label.pack(pady=5)

            pressure_label = tk.Label(card, text=f"Pressure: {avg_pressure:.0f} hPa", font=("Arial", 10), fg="white", bg=card_color)
            pressure_label.pack(pady=5)

            wind_label = tk.Label(card, text=f"Wind: {wind_speed:.1f} m/s", font=("Arial", 10), fg="white", bg=card_color)
            wind_label.pack(pady=5)

            days_shown += 1

# GUI Setup
root = tk.Tk()
root.title("Weather App")
root.geometry("1000x600")

# Left Panel
left_panel = tk.Frame(root, width=300, height=600, bg="black")
left_panel.pack(side="left", fill="y")

city_label = tk.Label(left_panel, text="Enter City", font=("Arial", 14), fg="white", bg="black")
city_label.pack(pady=10)

city_entry = tk.Entry(left_panel, width=20, font=("Arial", 14))
city_entry.pack(padx=3, pady=5)

fetch_button = tk.Button(left_panel, text="Fetch Weather", font=("Arial", 12, "bold"), command=display_weather, bg="#3498db", fg="white")
fetch_button.pack(pady=20)

weather = tk.Label(left_panel, text="Today's Weather",bg="black", font=("Arial", 16), fg="green", justify="center")
weather.pack(pady=5)

current_weather_label = tk.Label(left_panel, text="", bg="black", font=("Arial", 16), fg="lightblue", justify="center")
current_weather_label.pack(pady=50)


sunrise = tk.Label(left_panel, text="☀️——————>   ⛅", font=("Arial", 25, "bold"),fg="white", bg="black", justify="center")
sunrise.pack(pady=0)

sunrise = tk.Label(left_panel, text="Sunrise                     Sunset", font=("Arial", 25, "bold"),fg="orange", bg="black")
sunrise.pack(pady=5)

sunriset_label = tk.Label(left_panel, text="", font=("Arial", 14), fg="lightblue", bg="black", justify="left")
sunriset_label.pack(pady=5)

# Right Panel
right_panel = tk.Frame(root, bg="#2c3e50")
right_panel.pack(side="right", fill="both", expand=True)

# Heading for Forecast (this will be visible at the top)
forecast_heading = tk.Label(
            right_panel, 
            text="Next 5 Days Weather Forecast", 
            font=("Arial", 16, "bold"), 
            fg="orange", 
            bg="#2c3e50",
            justify="center"
        )
forecast_heading.pack(pady=0)


forecast_frame = tk.Frame(right_panel, bg="#2c3e50")
forecast_frame.pack(pady=20, fill="both", expand=True)


# Run the App
root.mainloop()

