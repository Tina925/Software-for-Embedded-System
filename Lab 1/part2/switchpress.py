import neopixel
from machine import Pin
from time import sleep

led_board = Pin(2, Pin.OUT)
led_board.value(1)

pixel = neopixel.NeoPixel(Pin(0), 1)  

button = Pin(38, Pin.IN) 

switchCount = 0

RED = (255, 0, 0)
GREEN = (0, 255, 0)
OFF = (0, 0, 0)

pixel[0] = RED
pixel.write()

while True:
    bp = button()
    if bp == False:  
        pixel[0] = GREEN
        pixel.write()
        sleep(0.5)
        switchCount += 1
    else:
        pixel[0] = RED
        pixel.write()  
    if switchCount >= 5:
        pixel[0] = OFF
        pixel.write()  
        print("You have successfully implemented LAB1!")
        break
