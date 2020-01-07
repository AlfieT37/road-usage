import requests
import json

response = requests.get('http://api.openweathermap.org/data/2.5/weather?id=2172797&appid=72e0b2e97b92dddbffc7c27a785be510')
print(response.json())

weather_report = json.dumps(response.json(), sort_keys=True, indent=4)
weather_dict = response.json()

# Reports
main_rep = weather_dict['main']
weather_rep = weather_dict['weather']
weather_rep = weather_rep[0]

# Variables
status_now = weather_rep['main']
status_id_now = weather_rep['id']
temp_now = main_rep['temp']
humid_now = main_rep['humidity']

# Outputs
print('CODE %d!!!' % status_id_now)
print('%s outside' % status_now)
print('Current temperature = %d' % temp_now)
print('Current humidity = %d' % humid_now)


#with open('document.csv','a') as fd:
#    fd.write(myCsvRow)
