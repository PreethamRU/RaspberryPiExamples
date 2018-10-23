import paho.mqtt.client as paho
import os
import socket
import ssl
import json
from time import sleep
from random import uniform

connflag = False

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
awshost = "a3frrqauc90wmz.iot.us-west-2.amazonaws.com"      # Endpoint
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
		data = {}
		data['data']='saD'
		json_data = json.dumps(data)
		#tempreading = uniform(20.0,25.0)                        # Generating Temperature Readings
		mqttc.publish("ultrasonic", json_data, qos=1)        # topic: temperature # Publishing Temperature values
		print("msg sent: temperature " +  json_data ) # Print sent temperature msg on console
    else:

                print("waiting for connection...")
