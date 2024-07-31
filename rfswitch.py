p0 = Pin(2, Pin.OUT, Pin.PULL_UP)
rfmsg = 3
rfcode = 0b00001000010011111101

def switch(topic, msg):
  rfmsg = 3
  #rfcode = 0b00001000010011111101
  rfcode = 0b10101011010011101101
  try:
    #print('switch cb')
    if topic == b'switch':
      code = 1
    else:
      code = 2
    #print(topic, msg, code)
    if msg == b'true':
      #rfout(p0, 300, rfcode, 10)
      rfout(p0, 255, rfcode, code&7|8)
      print('on')
    else:
      rfout(p0, 255, rfcode, code&0xf)
      print('off')
      #rfout(p0, 300, rfcode, 2)

  except OSError as e:
    print('bad')
    return('Failed switch callback')
    
def rfpreamble(p0, t):
  p0.value(1)
  time.sleep_us(t-50)
  p0.value(0)
  time.sleep_us(t*31-100)
    
def rfbitout(p0, t1, t3, bit):
  dt = -40
  if (bit) > 0:
    p0.value(1)
    time.sleep_us(t3-dt)
    p0.value(0)
    time.sleep_us(t1+dt)
  else:
    p0.value(1)
    time.sleep_us(t1-dt)
    p0.value(0)
    time.sleep_us(t3+dt)
        
def rfoutx(p0, t, ccode, mmsg):
  for x in range(10):
    rfpreamble(p0, t)
    code = ccode
    msg = mmsg
    for x in range(20):
      rfbitout(p0, t, code&1)
      code >>= 1
    for x in range(4):
      rfbitout(p0, t, msg&1)
      msg >>= 1
      
def rfout(p0, t, ccode, mmsg):
  bits = ccode&0xfffff | ((mmsg&0xf) << 20)
  print("{0:24.24b}".format(bits))
  for x in range(10):
    rfpreamble(p0, t)
    bit = bits
    t3 = t+t+t
    for x in range(24):
      rfbitout(p0, t, t3, bit&1)
      bit >>= 1
    
