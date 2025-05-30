# -*- coding: utf-8 -*-
"""
Created on Wed May 28 13:40:41 2024

@author: Vikas Meena
"""

import tkinter as tk
from tkinter import messagebox
import requests
from datetime import datetime

API_KEY = "4a3e595dfcab67cd5afca9107134d348"  # Replace with your OpenWeatherMap API key

def kelvin_to_celsius(temp_k):
    return round(temp_k - 273.15, 2)

def get_weather():
    city = city_entry.get()
    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name.")
        return

    try:
        # Current Weather
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
        weather_data = requests.get(weather_url).json()

        if weather_data.get("cod") != 200:
            raise ValueError(weather_data.get("message", "Error fetching data"))

        temp = kelvin_to_celsius(weather_data["main"]["temp"])
        condition = weather_data["weather"][0]["description"].capitalize()
        humidity = weather_data["main"]["humidity"]
        wind_speed = weather_data["wind"]["speed"]

        current_weather.set(f"🌡 Temp: {temp}°C\n☁️ Condition: {condition}\n💧 Humidity: {humidity}%\n💨 Wind: {wind_speed} m/s")

        # Forecast
        forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}"
        forecast_data = requests.get(forecast_url).json()

        forecast_list = forecast_data["list"]
        daily_forecast = {}

        for entry in forecast_list:
            date = entry["dt_txt"].split(" ")[0]
            if date not in daily_forecast:
                temp = kelvin_to_celsius(entry["main"]["temp"])
                desc = entry["weather"][0]["description"].capitalize()
                daily_forecast[date] = f"{date}: {temp}°C, {desc}"

        forecast_text = "\n".join(daily_forecast.values())
        forecast_label.config(text=forecast_text)

    except Exception as e:
        messagebox.showerror("Error", str(e))


# === GUI Setup ===
root = tk.Tk()
root.title("Weather App")
root.geometry("400x500")

tk.Label(root, text="Enter City Name:", font=("Arial", 14)).pack(pady=10)
city_entry = tk.Entry(root, width=30, font=("Arial", 14))
city_entry.pack()

tk.Button(root, text="Get Weather", command=get_weather, font=("Arial", 12), bg="#007ACC", fg="white").pack(pady=10)

current_weather = tk.StringVar()
tk.Label(root, textvariable=current_weather, font=("Arial", 12), justify="left").pack(pady=10)

tk.Label(root, text="5-Day Forecast", font=("Arial", 14, "bold")).pack(pady=5)
forecast_label = tk.Label(root, text="", font=("Arial", 11), justify="left")
forecast_label.pack()

root.mainloop()
