import paho.mqtt.client as paho
import os
import socket
import ssl
import json
import RPi.GPIO as GPIO
import time

from time import sleep
from random import uniform

connflag = False
GPIO.setmode(GPIO.BCM)

GPIO_TRIGGER = 18
GPIO_ECHO = 24

GPIO.setup(GPIO_TRIGGER, GPIO.OUT)



GPIO.setup(GPIO_ECHO, GPIO.IN)


def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance

def on_connect(client, userdata, flags, rc):                # func for making connection
    global connflag
    print "Connected to AWS"
    connflag = True
    print("Connection returned result: " + str(rc) )

def on_message(client, userdata, msg):                      # Func for Sending msg
    print(msg.topic+" "+str(msg.payload))

#def on_log(client, userdata, level, buf):
#    print(msg.topic+" "+str(msg.payload))

mqttc = paho.Client()                                       # mqttc object
mqttc.on_connect = on_connect                               # assign on_connect func
mqttc.on_message = on_message                               # assign on_message func
#mqttc.on_log = on_log

#### Change following parameters ####
awshost = "<AWS HOST>"      # Endpoint
awsport = 8883                                              # Port no.
clientId = "myraspi"                                     # Thing_Name
thingName = "myraspi"                                    # Thing_Name
caPath = "root-CA.crt"                                      # Root_CA_Certificate_Name
certPath = "myraspi.cert.pem"                            # <Thing_Name>.cert.pem
keyPath = "myraspi.private.key"                          # <Thing_Name>.private.key

mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)  # pass parameters

mqttc.connect(awshost, awsport, keepalive=60)               # connect to aws server

mqttc.loop_start()                                          # Start the loop

while 1==1:
    sleep(5)
    if connflag == True:
		dist = distance()

                print ("Measured Distance = %.1f cm" % dist)
                time.sleep(1)
		data = {}
		data['data']=dist
		json_data = json.dumps(data)
		#tempreading = uniform(20.0,25.0)                        # Generating Temperature Readings
		mqttc.publish("ultrasonic", json_data, qos=1)        # topic: temperature # Publishing Temperature values
		print("msg sent: temperature " +  json_data ) # Print sent temperature msg on console
    else:

                print("waiting for connection...")
