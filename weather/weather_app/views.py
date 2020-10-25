import pandas as pd
import requests
from django.shortcuts import render


# Create your views here.

def index(request):
    data_frame = pd.read_csv(r'/home/devish/PycharmProjects/weather/worldcities.csv')
    if 'city' in request.GET:
        city = request.GET['city']
        if data_frame[data_frame['city_ascii'] == city]['city_ascii'].any():
            lat = data_frame[data_frame['city_ascii'] == city]['lat']
            lon = data_frame[data_frame['city_ascii'] == city]['lng']
            url = "https://climacell-microweather-v1.p.rapidapi.com/weather/realtime"
            querystring = {"unit_system": "us", "fields": ['precipitation', 'temp', 'cloud_cover',
                                                           'wind_speed', 'humidity', 'weather_code'], "lat": lat, "lon": lon}
            headers = {
                'x-rapidapi-host': "climacell-microweather-v1.p.rapidapi.com",
                'x-rapidapi-key': "257b7cd080msh7a47fcb73c2078dp1efdbcjsn92c7b293b820"
            }

            response = requests.request("GET", url, headers=headers, params=querystring).json()
            context = {'city_name': city, 'temp': response['temp']['value'],
                       'weather_code': response['weather_code']['value'],
                       'wind_speed': response['wind_speed']['value'],
                       'precipitation': response['precipitation']['value'],
                       'humidity': response['humidity']['value']
                       }
        else:
            context = None
    else:
        context = None
    return render(request, 'weather/index.html', context)
