

import mqtt_status
import mqtt_dht
import mqtt_switch
import mqtt_bme280

def parsesensorlist(sensorlist, nodename: str):
  numdht = 0
  numbme280 = 0
  numswtch = 0
  sensors = [mqtt_status.mqttSTATUS("%s" % nodename, '0')]
  for line in sensorlist:
    line = line.strip()
    print('<',line,'>')
    if len(line) > 0 and line[0] != "#" :
        parts = line.split()
        #print(parts)
        nameParts = parts[0].split('/')
        #print(nameParts)
        if nameParts[0].lower() == 'bme280':
            pin1 = int(parts[1])
            pin2 = int(parts[2])
            if len(nameParts) > 1:
              idpostfix = nameParts[1]
            else:
              idpostfix = str(numbme280)
            sensors.append(mqtt_bme280.mqttBME280(nodename, pin1, pin2, idpostfix))
            numbme280 += 1
        if nameParts[0].lower() == 'dht22':
            pin = int(parts[1])
            if len(nameParts) > 1:
              idpostfix = nameParts[1]
            else:
              idpostfix = str(numdht)
            sensors.append(mqtt_dht.mqttDHT(nodename, pin, idpostfix))
            numdht += 1
        if nameParts[0].lower() == 'swtch':
            pin = int(parts[1])
            #print(pin)
            if len(nameParts) > 1:
              idpostfix = nameParts[1]
            else:
              idpostfix = str(numdht)
            sensors.append(mqtt_switch.mqttSWITCH(nodename, pin, idpostfix))
            numdht += 1
        
  return sensors
