
import time

class mqttUPTIME():

  def __init__(self, nodename: str, idpostfix = ''):
      self.nodename = nodename
      self.idpostfix = idpostfix
      self.tStart = time.time()
      pass

  def read(self):
    return 0
    pass

  def get_uptime(self):
    return time.time()-self.tStart

  def disp(self):
    print("%s/Uptime: %.1f" % (self.nodename, self.get_uptime()))
    return 0

  def publish(self, client):
    try:
      client.publish("%s/uptime" % (self.nodename), "%.1f" % self.get_uptime())
      return 0
    except:
      return -1
