# Complete project details at https://RandomNerdTutorials.com/micropython-mqtt-publish-dht11-dht22-esp32-esp8266/

import time
from umqttsimple import MQTTClient
import ubinascii
import machine
import micropython
import network
import esp
from machine import Pin
import dht
#esp.osdebug(None)
import gc
#from machine import WDT
import WDT
from machine import Pin
gc.collect()
import mqtt_sens
#import mqtt_uptime
#import mqtt_dht
#import mqtt_switch

def connect_mqtt():
  global client_id, mqtt_server
  print(client_id, mqtt_server)
  client = MQTTClient(client_id, mqtt_server)
  #client = MQTTClient(client_id, mqtt_server, user=your_username, password=your_password)
  client.connect()
  print('Connected to %s MQTT broker' % (mqtt_server))
  return client

def restart_and_reconnect(msg: str):
  try:  
    print("%s, rebooting ..." % (msg))
    time.sleep(1)
  except:
    machine.reset()

  machine.reset()

time.sleep(3)
try:
    print('reset cause:', machine.reset_cause())
    wdtDebug = 0

    print("Reading wifi.dat")

    fid = open('wifi.dat')
    lines = fid.readlines()
    ssid = lines[0].strip()
    password = lines[1].strip()
    mqtt_server = lines[2].strip()
    nodename = lines[3].strip()
    message_interval = int(lines[4].strip())
    sensorlist = []
    if len(lines)>5:
      sensorlist = [lines[5].strip()]
      for line in range(6,len(lines)):
        sensorlist.append(lines[line].strip())
        
    sensors = mqtt_sens.parsesensorlist(sensorlist, nodename)
    print(sensors)

    fid.close()
    print(ssid)
    print(password)
    print(mqtt_server)
    print(nodename)
    print(message_interval)
    print('Sensors:')
    for line in range(0,len(sensors)):
      print(sensors[line])

    client_id = ubinascii.hexlify(machine.unique_id())
    print(client_id)
    
    topic_switch = b'switch'
    topic_switch2 = b'switch2'

    last_message = 0

    station = network.WLAN(network.STA_IF)
    #time.sleep(1)
    #if station.isconnected():
    station.active(False)
    #time.sleep(3)
    station.active(True)
    station.config(dhcp_hostname=nodename)
    #time.sleep(1)
    #time.sleep(1)
    station.connect(ssid, password)
    time.sleep(1)
    print(station.config('dhcp_hostname'))
    
    isconnectedCount = 0
    print("Waiting for connection")
    while station.isconnected() == False:
      station.connect(ssid, password)
      time.sleep(5)
      isconnectedCount += 1
      print('Connect attempt: ', isconnectedCount)
      if isconnectedCount > 10:
        restart_and_reconnect('Failed to connect to WiFi')
        
    print('Connection successful')
    print(station.ifconfig())

    try:
      print('connect_mqtt')
      client = connect_mqtt()
      print('connected')
      #client.set_callback(switch)
      #client.subscribe(topic_switch)
      #client.subscribe(topic_switch2)
    except OSError as e:
      restart_and_reconnect('Failed to connect to MQTT broker')

    if wdtDebug > 0:
      w = WDT.WDT(timeout=25)

    try:
      while True:
        client.check_msg()
        if (time.time() - last_message) >= message_interval:
          last_message = time.time()
          if wdtDebug > 0:
              print('feed')
              w.feed()
          for sens in sensors:
            #print(sens)
            if sens.read() < 0:
              print('Error Sensor read(),', sens)
              sensors[0].fault()
            else:
              sens.disp()
              if sens.publish(client) < 0:
                print('Error publising Sensor')
                sensors[0].fault()
          if sensors[0].get_faultCount() > 10:
            restart_and_reconnect('Error: Fault Count Limit Exceeded')
              
    except:
      restart_and_reconnect('Failed periodic cycle through sensors')
    finally:
      machine.reset()

except:
  restart_and_reconnect('Failed periodic cycle through sensors')
finally:
  machine.reset()


