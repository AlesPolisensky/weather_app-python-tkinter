from tkinter import *
from tkinter import messagebox
from configparser import ConfigParser
from typing import final
import requests
from PIL import ImageTk
import PIL.Image

app = Tk()
app.title("Weather forecast")
app.geometry("400x350")

url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid={}"

config_file = "config.ini"
config = ConfigParser()
config.read("config.ini")
api_key= config["api_key"]["key"]
print(api_key)

def weather(city):
    result = requests.get(url.format(city, api_key))
    if result:
        json = result.json()
        city = json["name"]
        country = json["sys"]["country"]
        temp_kelv = json["main"]["temp"]
        temp_cels = temp_kelv - 273.15
        icon = json["weather"][0]["icon"]
        weather = json["weather"][0]["main"]
        wind = json["wind"]["speed"]
        wind_km_h = wind * 3.6
        final_weather = (city, country, temp_cels, icon, weather, wind_km_h)
        return final_weather
        
    else:
        return None
print(weather("London"))
    
def search():
    global img
    city = search_text.get()
    get_weather = weather(city)
    if get_weather:
        location["text"] = "{}, {}".format(get_weather[0], get_weather[1])
        img["file"] = "icons/{}.png".format(get_weather[3])
        temperature["text"] = "{:.1f}°C".format(get_weather[2])
        weather_lbl["text"] = get_weather[4]
        wind_speed["text"] = "{:.1f}km/h".format(get_weather[5])
        
    else:
        messagebox.showerror("Error", "Couldn't find the city {}".format(city))

search_text = StringVar()
search_bar = Entry(app, textvariable=search_text)
search_bar.pack()

button = Button(app, text="Search", width = 12, command = search)
button.pack()

location = Label(app, text="", font= ("bold", 20))
location.pack()

img = PhotoImage(file="")
image = Label(app, image=img)
image.pack()

temperature = Label(app, text="")
temperature.pack()

wind_speed = Label(app, text="")
wind_speed.pack()

weather_lbl = Label(app, text = "")
weather_lbl.pack()





app.mainloop()