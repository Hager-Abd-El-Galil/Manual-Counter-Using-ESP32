from machine import Pin,Timer
from time import sleep
#------------------------- Inputs ------------------------------#
inc_bt = Pin(13,Pin.IN) #increament button
dec_bt = Pin(14,Pin.IN) #decreament button
reset = Pin(15,Pin.IN) #reset button

#--------------------------Output------------------------------------# 
a = Pin(26,Pin.OUT)
b = Pin(27,Pin.OUT)
c = Pin(18,Pin.OUT)
d = Pin(19,Pin.OUT)
e = Pin(21,Pin.OUT)
f = Pin(33,Pin.OUT)
g = Pin(23,Pin.OUT)

#----------------------------- Dispaly --------------------#
def display_segment(i):
  if i==0:
    a.value(1), b.value(1), c.value(1),d.value(1),  e.value(1), f.value(1), g.value(0) 
  if i==1:
    a.value(0), b.value(1), c.value(1),d.value(0),  e.value(0), f.value(0), g.value(0) 
  if i==2:
    a.value(1), b.value(1), c.value(0),d.value(1),  e.value(1), f.value(0), g.value(1) 
  if i==3:
    a.value(1), b.value(1), c.value(1),d.value(1),  e.value(0), f.value(0), g.value(1) 
  if i==4:
    a.value(0), b.value(1), c.value(1),d.value(0),  e.value(0), f.value(1), g.value(1) 
  if i==5:
    a.value(1), b.value(0), c.value(1),d.value(1),  e.value(0), f.value(1), g.value(1) 
  if i==6:
    a.value(1), b.value(0), c.value(1),d.value(1),  e.value(1), f.value(1), g.value(1) 
  if i==7:
    a.value(1), b.value(1), c.value(1),d.value(0),  e.value(0), f.value(0), g.value(0) 
  if i==8:
    a.value(1), b.value(1), c.value(1),d.value(1),  e.value(1), f.value(1), g.value(1) 
  if i==9: 
    a.value(1), b.value(1), c.value(1),d.value(1),  e.value(0), f.value(1), g.value(1)  
  sleep(0.3)

#------------------------------ Access Point ------------------------------------------#
try:
  import usocket as socket
except:
  import socket
import network
ssid='Esp32_AP'
password='123456789'
ap = network.WLAN(network.AP_IF) 
ap.active(True)
ap.config(essid=ssid, password=password)
while not ap.active():
    pass
print('network config:', ap.ifconfig())  
#------------------------------- Initialization------------------------------------#
i = 0
#---------------------------------------Interrupt-------------------------------------#
  #------------- increament section -------------#
def handle_inc(timer):
  global i
  if i == 9:
    i=0
  else:
    i=i+1
  display_segment(i)
def debounce_inc(pin):
  # Start or replace a timer for 200ms, and trigger handle_inc.
    timer.init(mode=Timer.ONE_SHOT, period=200, callback=handle_inc)
  
# Register an interrupt on rising button input.
inc_bt.irq(trigger=Pin.IRQ_RISING, handler=debounce_inc)
#------------- Decreament section -------------#
def handle_dec(timer):
    global i
    if i == 0:
      i=9
    else:
      i=i-1
    display_segment(i)
def debounce_dec(pin):
   # Start or replace a timer for 200ms, and trigger handle_dec.
    timer.init(mode=Timer.ONE_SHOT, period=200, callback=handle_dec)
  
# Register an interrupt on rising button input.
dec_bt.irq(trigger=Pin.IRQ_RISING, handler=debounce_dec)
#------------ Reset section ----------#
def handle_reset(timer):
   global i
   i = 0
   display_segment(i)

def debounce_reset(pin):
    # Start or replace a timer for 200ms, and trigger handle_reset.
    timer.init(mode=Timer.ONE_SHOT, period=200, callback=handle_reset)
  
# Register an interrupt on rising button input.
reset.irq(trigger=Pin.IRQ_RISING, handler=debounce_reset)
# Register a new hardware timer.
timer = Timer(0)
#---------------------------#


#------------------------------------- Web page--------------------------------------------#
def web_page():
  html = """<html><head> <title>ESP Web Server</title> <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" href="data:,"> <style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
  h1{color: #0F3376; padding: 2vh;}p{font-size: 1.5rem;}.button{display: inline-block; background-color: #4CAF50; border: none; 
  border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
  .button2{background-color: #555555;}.button3{background-color: #f44336;}</style></head>
  <body>
  <h1>ESP Web Server</h1>
  <h2>7-segment control</h2>
  <p>
    <span class=>Display on 7-segment</span> 
    <span>"""+str(i)+"""</span>
  </p>
<a href="/Inc"><button class="button">INC</button></a></p>
  <p><a href="/Dec"><button class="button button2">DEC</button></a></p>
<p><a href="/Reset"><button class="button button3">Reset</button></a></p>
</body></html>"""
  return html

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)


while True:
  conn, addr = s.accept()   # Socket accept()
  print('Got a connection from %s' % str(addr))
  request = conn.recv(1024)
  request = str(request)

  print('Content = %s' % request)
 # Socket send()
  Inc = request.find("/Inc")
  Dec = request.find("/Dec")
  Reset = request.find("/Reset")
  display_segment(i)
  if Inc == 6 :
    if i == 9:
      i=0
    else:
      i=i+1
    display_segment(i)
  if Dec == 6 :
    if i == 0:
      i=9
    else:
      i=i-1
    display_segment(i)
  if Reset == 6 :
    i = 0
    display_segment(i)
  response = web_page()
  conn.send('HTTP/1.1 200 OK\n')
  conn.send('Content-Type: text/html\n')
  conn.send('Connection: close\n\n')
  conn.sendall(response)
  # Socket close()
  conn.close()










