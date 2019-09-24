from database import grab_data
import requests

data, DATABASE_URI = grab_data()
api_key = data['weather_api_key']

city = 'Raleigh,NC'
get_url = f"https://api.weatherbit.io/v2.0/current?city={city}&key={api_key}"
current_weather = requests.get(get_url).json().get('data')[0]
print(current_weather)
current_time = current_weather['timestamp_utc'].split('T')[1]
current_temp = current_weather.get('temp')
current_code = current_weather.get('weather').get('code')

print(f"current_time: {current_time}, current_temp: {current_temp}, current_code: {current_code}")

# code: 800 or 801 == good
# code: 200-624 or 900 == bad


forecast_url = f"https://api.weatherbit.io/v2.0/forecast/hourly?city={city}&key={api_key}&hours=24"
forecast = requests.get(forecast_url).json()['data']
next_day = [hour['timestamp_utc'].split('T')==current_time for hour in forecast][0]
print(next_day)

# print('\n')
# print(*response.items(), sep='\n')
# print()
# print(response.get('clouds'))
# print(response.get('weather'))  # code: 800 or 801 == good
#                                 # code: 200-624 or 900 == bad
# print(response.get('temp'))