
import dht
from machine import Pin

class mqttDHT():

  def __init__(self, nodename: str, pin: int, idpostfix = ''):
      self.nodename = nodename
      self.idpostfix = idpostfix
      self.sensor = dht.DHT22(Pin(pin))
      pass

  def read(self):
    try:
      self.sensor.measure()
      self.tempc = self.sensor.temperature()
      self.hum = self.sensor.humidity()
      if (type(self.tempc) != float) or (type(self.hum) != float):
        self.tempc = -999.9
        self.hum = -99.9
      return 0 
    except OSError as e:
      return -1

  def get_tempc(self):
    return self.tempc

  def get_tempf(self):
    return 32.0 + self.tempc*9.0/5.0

  def get_hum(self):
    return self.hum

  def disp(self):
    print("%s/DHT%s/tempc: %4.1f" % (self.nodename, self.idpostfix, self.get_tempc()))
    print("%s/DHT%s/tempf: %4.1f" % (self.nodename, self.idpostfix, self.get_tempf()))
    print("%s/DHT%s/hum:   %4.1f" % (self.nodename, self.idpostfix, self.get_hum()))
    return 0

  def publish(self, client):
    try:
      client.publish("%s/DHT%s/tempc" % (self.nodename, self.idpostfix), "%.1f" % self.get_tempc())
      client.publish("%s/DHT%s/tempf" % (self.nodename, self.idpostfix), "%.1f" % self.get_tempf())
      client.publish("%s/DHT%s/hum" % (self.nodename, self.idpostfix), "%.1f" % self.get_hum())
      return 0
    except:
      return -1