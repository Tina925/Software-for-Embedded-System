import machine
from machine import Pin, Timer, RTC, TouchPad, deepsleep
import network, ntptime, esp32
from neopixel import NeoPixel

#2.2.1

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
#print(wlan.isconnected())

#2.2.2

def mycallback1(timer1):
    
    newt = rtc.datetime()
    #if first sunday of november and second sunday of march at 2am -4, otherwise -5
    if (newt[1] >= 11 and newt[1] <= 3 and newt[1] == 11 and newt[2] <= 7 and newt[3] == 6) or (newt[1] >= 11 and newt[1] <= 3 and newt[1] == 3 and newt[2] >= 8 and newt[2] <= 14 and newt[3] == 6):

        print("Date: {:02}/{:02}/{:04}".format(newt[1], newt[2], newt[0]))
        print("Time: {:02}:{:02}:{:02} EDT".format(newt[4]-4, newt[5], newt[6]))
    else:

        print("Date: {:02}/{:02}/{:04}".format(newt[1], newt[2], newt[0]))
        print("Time: {:02}:{:02}:{:02} EST".format(newt[4]-5, newt[5], newt[6]))
    #print("Date: {:02}/{:02}/{:04}".format(newt[1], newt[2], newt[0]))
    #print("Time: {:02}:{:02}:{:02} EST".format(newt[4]-5, newt[5], newt[6]))

rtc = machine.RTC()
ntptime.host = "pool.ntp.org"
while True:
    try:
        ntptime.settime()
        break
    except:
        continue

timer1 = Timer(1)
timer1.init(period=15000, callback=mycallback1)

#2.2.3
def mycallback2(timer2):
    value = t.read()
    if value < thres:
        np[0] = (0, 255, 0)
    else:
        np[0] = (0, 0, 0)
    np.write()
led_board = Pin(2, Pin.OUT)
led_board.value(1)

t = TouchPad(Pin(32))
thres = 300
#t.config(50)
#esp32.wake_on_touch(True)

np = NeoPixel(Pin(0), 1)
timer2 = machine.Timer(2)
timer2.init(period=50, callback = mycallback2)

#2.2.4
def mycallback3 (timer3):
    print("I am going to sleep for 1 minute.")
    led.off()
    deepsleep(60000)

led = Pin(13, Pin.OUT)
led.on()
timer3 = machine.Timer(3)
timer3.init(period=30000, callback = mycallback3)
#t.config(500)
#t.irq(trigger=t.WAKE_LOW, wake=machine.DEEPSLEEP)

#2.2.4.1. Wake up Sources
switch = Pin(14, Pin.IN, Pin.PULL_DOWN)
esp32.wake_on_ext0(pin=switch, level=esp32.WAKEUP_ANY_HIGH)

if machine.wake_reason() == machine.EXT0_WAKE:
    print("EXT0 wake up")
elif machine.wake_reason() == machine.TIMER_WAKE:
    print("TIMER wake up")

#switch.irq(trigger=Pin.WAKE_LOW, wake=machine.DEEPSLEEP)



    