from kivy.metrics import dp # type: ignore
from kivymd.app import MDApp # type: ignore
from kivymd.uix.screen import Screen # type: ignore
from kivymd.uix.boxlayout import MDBoxLayout # type: ignore
from kivymd.uix.button import MDFlatButton # type: ignore
from kivymd.uix.textfield import MDTextField # type: ignore
from kivymd.uix.label import MDLabel # type: ignore
from kivy.graphics import Color, RoundedRectangle # type: ignore
from kivy.uix.image import Image # type: ignore
from kivy.uix.popup import Popup # type: ignore
import requests
import datetime

class NEXUS(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
    
    def build(self):
        self.screen = Screen()
        self.layout = MDBoxLayout(orientation='vertical')

        self.logo = MDLabel(text='NEXUS', halign='center', font_style='H4', font_size=dp(16))
        self.layout.add_widget(self.logo)

        self.app_name = MDLabel(text='Weather Report App', halign='center', font_style='Body1')
        self.layout.add_widget(self.app_name)

        self.city_input = MDTextField(hint_text='Enter city name', pos_hint={'center_x': 0.5}, size_hint_x=None, width=300)
        self.layout.add_widget(self.city_input)

        self.search_button = MDFlatButton(text='Search', pos_hint={'center_x': 0.5}, on_release=self.get_weather, size_hint=(None, None), size=(150, 50))
        self.search_button.md_bg_color = (1, 1, 1, 0)
        self.search_button.text_color = self.theme_cls.primary_color
        self.search_button.bind(size=self.update_rect, pos=self.update_rect)
        self.layout.add_widget(self.search_button)

        self.result_layout = MDBoxLayout(orientation='horizontal')
        self.result_label_today = MDLabel(halign='center', valign='middle', size_hint=(0.5, 1))
        self.result_layout.add_widget(self.result_label_today)
        self.result_label_tomorrow = MDLabel(halign='center', valign='middle', size_hint=(0.5, 1))
        self.result_layout.add_widget(self.result_label_tomorrow)
        self.layout.add_widget(self.result_layout)
        
        # Adding image widget to display weather icon
        self.weather_image_today = Image(size_hint=(None, None), size=(100, 100), pos_hint={'center_x': 0.5})
        self.layout.add_widget(self.weather_image_today)
        
        self.weather_image_tomorrow = Image(size_hint=(None, None), size=(100, 100), pos_hint={'center_x': 0.5})
        self.layout.add_widget(self.weather_image_tomorrow)

        self.screen.add_widget(self.layout)
        return self.screen
    
    def update_rect(self, instance, value):
        self.search_button.canvas.before.clear()
        with self.search_button.canvas.before:
            Color(*self.theme_cls.primary_color[:3], 0.6)
            RoundedRectangle(pos=instance.pos, size=instance.size, radius=[15, ])

    def get_weather(self, *args):
        city = self.city_input.text.strip()

        # Easter egg code check
        if city == "911":
            self.trigger_easter_egg()
            return

        if not city:
            self.result_label_today.text = "Please enter a city name."
            self.result_label_tomorrow.text = ""
            self.weather_image_today.source = ''
            self.weather_image_tomorrow.source = ''
            return

        api_key = "3dbc5e85851bf73cb00b2387ba02af90"  # OpenWeatherMap API key

        #for fetching today's weather data
        today_weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        try:
            today_response = requests.get(today_weather_url)
            today_data = today_response.json()
            if today_data.get("cod") == 200:
                today_weather_description = today_data["weather"][0]["description"]
                today_temperature = today_data["main"]["temp"]
                today_humidity = today_data["main"]["humidity"]
                today_wind_speed = today_data["wind"]["speed"]
                today_info = (f"Weather in {city} today:\nDescription: {today_weather_description}\nTemperature: {today_temperature}°C\nHumidity: {today_humidity}%\nWind Speed: {today_wind_speed}m/s")
                self.result_label_today.text = today_info
                self.weather_image_today.source = self.get_weather_image(today_weather_description)
            else:
                self.result_label_today.text = "City not found. Please try again."
                self.weather_image_today.source = ''

            #for fetching tomorrow's weather data
            tomorrow_date = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
            tomorrow_weather_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
            tomorrow_response = requests.get(tomorrow_weather_url)
            tomorrow_data = tomorrow_response.json()
            if tomorrow_data.get("cod") == "200":
                for item in tomorrow_data['list']:
                    if item['dt_txt'].split(' ')[0] == tomorrow_date:
                        tomorrow_weather_description = item['weather'][0]['description']
                        tomorrow_temperature = item['main']['temp']
                        tomorrow_info = (f"Weather in {city} tomorrow:\nDescription: {tomorrow_weather_description}\nTemperature: {tomorrow_temperature}°C")
                        self.result_label_tomorrow.text = tomorrow_info
                        self.weather_image_tomorrow.source = self.get_weather_image(tomorrow_weather_description)
                        break
            else:
                self.result_label_tomorrow.text = "City not found. Please try again."
                self.weather_image_tomorrow.source = ''
        except requests.exceptions.RequestException as e:
            self.result_label_today.text = f"Error fetching weather data: {e}"
            self.result_label_tomorrow.text = ""
            self.weather_image_today.source = ''
            self.weather_image_tomorrow.source = ''

    def get_weather_image(self, description):
        weather_images = {
            'clear sky': 'sunny.png',
            'few clouds': 'cloudy.png',
            'scattered clouds': 'cloudy.png',
            'broken clouds': 'cloudy.png',
            'shower rain': 'rainy.png',
            'rain': 'rainy.png',
            'thunderstorm': 'storm.png',
            'snow': 'snowy.png',
            'mist': 'foggy.png'
        }
        return weather_images.get(description, 'default.png')

    def trigger_easter_egg(self):
        self.result_label_today.text = ""
        self.result_label_tomorrow.text = ""
        self.weather_image_today.source = ''
        self.weather_image_tomorrow.source = ''
        
        easter_egg_popup = Popup(title='Easter Egg',
                                 content=Image(source='images.jpeg'),
                                 size_hint=(None, None), size=(400, 400))
        easter_egg_popup.open()

if __name__ == '__main__':
    NEXUS().run()
