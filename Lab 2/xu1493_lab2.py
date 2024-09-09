import machine
from machine import Pin
from machine import PWM

year = input("Year? ")
month = input("Month? ")
day = input("Day? ")
weekday = input("Weekday? ")
hour = input("Hour? ")
minute = input("Minute? ")
second = input("Second? ")
microsecond = input("Microsecond? ")

def mycallback1(timer):
    print(rtc.datetime())
rtc = machine.RTC()
rtc.init((int(year), int(month), int(day), int(weekday), int(hour), int(minute), int(second), int(microsecond)))
timer1 = machine.Timer(1)
timer1.init(period=30000, callback=mycallback1)
#----------------------------------------------------------------
def changefreq(value):
    final_frequency = scale_frequency(value)
    pwm.freq(final_frequency)
    #print(pwm)
def changeduty(value):
    final_duty = scale_duty(value)
    pwm.duty(final_duty)
    #print(pwm)
def change(value):
    if switchCount % 2 == 0:
        changeduty(value)
    else:
        changefreq(value)
def mycallback2(timer):
    if switchCount != 0:
        analog_value = adc.read()
        #print(switchCount)
        change(analog_value)
        #print(analog_value)
    
adc = machine.ADC(Pin(34))
adc.atten(adc.ATTN_11DB)
timer2 = machine.Timer(2)
timer2.init(period=100, callback = mycallback2)
#----------------------------------------------------------------
led = Pin(32, Pin.OUT)
pwm = PWM(led, freq=10, duty=512)
#pwm.init()
#----------------detect switch-press-----------------------------
def debounce(switch):
    prev = None
    for x in range(32):
        curr = switch.value()
        if prev != curr and prev is not None:
            return None
        prev = curr
    return prev

def scale_duty(adc_value):
    return int(adc_value * (1023 / 4095))
def scale_frequency(adc_value):
    return 1 + (adc_value // 70)
def mycallback3(switch):
    #print("Button pressed!")
    global switchCount
    debounced = debounce(switch)
    if debounced is None:
        return
    if debounced == 0:
        switchCount+=1

switch = Pin(38, Pin.IN)
switchCount = 0
switch.irq(trigger=Pin.IRQ_FALLING, handler=mycallback3)

#while True:
#    pass


