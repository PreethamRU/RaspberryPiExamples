import paho.mqtt.client as paho
import os
import socket
import ssl
import RPi.GPIO as GPIO
import time
import json


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(2,GPIO.OUT)

def on_connect(client, userdata, flags, rc):                # func for making connection
    print("Connection returned result: " + str(rc) )
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("ultrasonic1" , 1 )                              # Subscribe to all topics

def on_message(client, userdata, msg):                      # Func for receiving msgs
	print(msg.topic+" "+str(msg.payload))
	if msg.payload=='on':
		GPIO.output(2,GPIO.HIGH)
        else:

               GPIO.output(2,GPIO.LOW) 


 
#def on_log(client, userdata, level, msg):
#    print(msg.topic+" "+str(msg.payload))
 
mqttc = paho.Client()                                       # mqttc object
mqttc.on_connect = on_connect                               # assign on_connect func
mqttc.on_message = on_message                               # assign on_message func
#mqttc.on_log = on_log

#### Change following parameters ####  
awshost = "a3frrqauc90wmz.iot.us-west-2.amazonaws.com"      # Endpoint
awsport = 8883                                              # Port no.   
clientId = "myraspi"                                     # Thing_Name
thingName = "myraspi"                                    # Thing_Name
caPath = "root-CA.crt"                                      # Root_CA_Certificate_Name
certPath = "myraspi.cert.pem"                            # <Thing_Name>.cert.pem
keyPath = "myraspi.private.key"                          # <Thing_Name>.private.key
 
mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)      # pass parameters
 
mqttc.connect(awshost, awsport, keepalive=60)               # connect to aws server
 
mqttc.loop_forever() 














