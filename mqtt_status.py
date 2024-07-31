
import time
import machine

class mqttSTATUS():

  def __init__(self, nodename: str, idpostfix = ''):
      self.nodename = nodename
      self.idpostfix = idpostfix
      self.tStart = time.time()
      self.faultCount = 0
      pass

  def read(self):
    return 0
    pass

  def get_uptime(self):
    return time.time()-self.tStart

  def get_faultCount(self):
    return self.faultCount

  def fault(self):
    self.faultCount += 1

  def disp(self):
    print("%s/Status/Uptime: %.1f" % (self.nodename, self.get_uptime()))
    print("%s/Status/FaultCount: %.1f" % (self.nodename, self.get_faultCount()))
    print("%s/Status/resetCause: %d" % (self.nodename, machine.reset_cause()))
    return 0

  def publish(self, client):
    try:
      client.publish("%s/Status/uptime" % (self.nodename), "%.1f" % self.get_uptime())
      client.publish("%s/Status/faultCount" % (self.nodename), "%.1f" % self.get_faultCount())
      client.publish("%s/Status/resetCause" % (self.nodename), "%d" % machine.reset_cause())
      return 0
    except:
      return -1
