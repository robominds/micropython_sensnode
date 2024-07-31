
import bme280
from machine import Pin, I2C

class mqttBME280():

  def __init__(self, nodename: str, pin1: int, pin2: int, idpostfix = ''):
      self.nodename = nodename
      self.idpostfix = idpostfix
      self.sensor = I2C(scl=Pin(pin1), sda=Pin(pin2), freq=10000)
      pass

  def read(self):
    try:
      bme = BME280.BME280(i2c=self.sensor)
      self.tempc = bme.temperature
      self.hum = bme.humidity
      self.pres = bme.pressure
      if (type(self.tempc) != float) or (type(self.hum) != float):
        self.tempc = -999.9
        self.hum = -99.9
        self.press = -99.9
      return 0 
    except OSError as e:
      return -1

  def get_tempc(self):
    return self.tempc

  def get_tempf(self):
    return 32.0 + self.tempc*9.0/5.0

  def get_hum(self):
    return self.hum

  def get_press(self):
    return self.press

  def disp(self):
    print("%s/BME%s/tempc: %4.1f" % (self.nodename, self.idpostfix, self.get_tempc()))
    print("%s/BME%s/tempf: %4.1f" % (self.nodename, self.idpostfix, self.get_tempf()))
    print("%s/BME%s/hum:   %4.1f" % (self.nodename, self.idpostfix, self.get_hum()))
    print("%s/BME%s/press:   %4.1f" % (self.nodename, self.idpostfix, self.get_press()))
    return 0

  def publish(self, client):
    try:
      client.publish("%s/BME%s/tempc" % (self.nodename, self.idpostfix), "%.1f" % self.get_tempc())
      client.publish("%s/BME%s/tempf" % (self.nodename, self.idpostfix), "%.1f" % self.get_tempf())
      client.publish("%s/BME%s/hum" % (self.nodename, self.idpostfix), "%.1f" % self.get_hum())
      client.publish("%s/BME%s/press" % (self.nodename, self.idpostfix), "%.1f" % self.get_press())
      return 0
    except:
      return -1
