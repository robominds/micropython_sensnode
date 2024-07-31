
from machine import Pin

class mqttSWITCH():

  def __init__(self, nodename: str, pin: int, idpostfix = ''):
      self.nodename = nodename
      self.idpostfix = idpostfix
      self.switch = Pin(pin, Pin.IN, Pin.PULL_UP)
      pass

  def read(self):
      return 0
      pass

  def get_state(self):
    return self.switch.value()

  def disp(self):
    print("%s/SW%s/state: %d" % (self.nodename, self.idpostfix, self.get_state()))
    return 0

  def publish(self, client):
    try:
      client.publish("%s/switch/state" % (self.nodename), "%d" % self.get_state())
      return 0
    except:
      return -1
