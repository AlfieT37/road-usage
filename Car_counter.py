import RPi.GPIO as GPIO
import datetime
import time
from picamera import PiCamera
import csv
from random import seed
from random import randint
from random import choices
import requests
import json

camera = PiCamera()
#camera.start_preview()
#sleep(5)
#camera.stop_preview()
#camera.rotation = 180
#camera.capture('home/pi/Documents/image%s.jpg' % datetime_object)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(27,GPIO.OUT)
GPIO.setup(22,GPIO.OUT)
GPIO.setup(23,GPIO.OUT)

GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#datetime
#datetime_now = datetime.datetime.now()
#print (datetime_now)

# datetime_object = datetime.datetime.now()
# datetime_object = str(datetime_object)
# print (datetime_object)

#raspistill -o Documents/image.jpg
#camera.capture('home/pi/Documents/image%s.jpg' % i)

#Random mic sensor data
pop = [0,1]
prob = [0.4,0.6]

def weather():
    try:
        response = requests.get('http://api.openweathermap.org/data/2.5/weather?id=2172797&appid=72e0b2e97b92dddbffc7c27a785be510')
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
        report = [status_now,status_id_now,temp_now,humid_now]
        return(report)
    except:
         report = ['NaN','NaN','Nan','Nan']

try:
    while True:
        time.sleep(0.25)
        mot = GPIO.input(4)
        if mot == 1:
            datetime_object = datetime.datetime.now()
            camera.capture('/home/pi/rpi-sync/Photos/%s.jpg' % datetime_object)
            print ('motion detected')
            #mic = GPIO.input(17)
            mic = choices(pop,prob)
            if mic == 1:
                mic_ana = randint(100,256)
            else:
                mic_ana = randint(0,100)
            report = weather()
            append = [datetime_object,mic,mic_ana,report]
            with open('/home/pi/rpi-sync/Data/data.csv', 'a') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(append)
            csvFile.close()
            time.sleep (2)
            print('ready')

except KeyboardInterrupt:
    GPIO.cleanup()
    print("")