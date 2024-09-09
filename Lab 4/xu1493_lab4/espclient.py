import machine
from machine import Pin, Timer
import network, esp32, socket, time

#2.2

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    print('connecting to network...')
    wlan.connect('tina', '88888888')
    while not wlan.isconnected():
        pass
#print('network config:', wlan.ifconfig())
print("Connected to", wlan.config('ssid'))
print("IP Address: ", wlan.ifconfig()[0])

def mycallback1(timer1):
    temperature = esp32.raw_temperature()
    hall = esp32.hall_sensor()
    print(temperature)
    print(hall)
    
    addr = socket.getaddrinfo('api.thingspeak.com',80)[0][-1]
    request = "GET https://api.thingspeak.com/update?api_key=8GNIJH9T0XTYOX0A&field1={:.2f}&field2={:.2f}\r\n\r\n".format(temperature, hall)
    s = socket.socket()
    s.connect(addr)
    s.send(request)
    while True:
        s.recv(1024)
        break
    s.close()
    
timer1 = Timer(1)
timer1.init(period=30000, callback=mycallback1)

end_time = time.time() + 300
while time.time() < end_time:
   pass
timer1.deinit()
