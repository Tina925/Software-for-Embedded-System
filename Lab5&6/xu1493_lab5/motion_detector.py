import machine
from machine import Pin, I2C, Timer
import utime, network, socket
from neopixel import NeoPixel

# Network setup
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    print('connecting to network...')
    wlan.connect('tina', '88888888')
    while not wlan.isconnected():
        pass

print("Connected to", wlan.config('ssid'))
print("IP Address: ", wlan.ifconfig()[0])

# LED setup for visual feedback
led_board = Pin(2, Pin.OUT)
led_board.value(1)

# I2C setup for MPU6050
i2c = machine.SoftI2C(scl=Pin(14), sda=Pin(22))
address = i2c.scan()[0]
#print(address)

class MPU:
    ACC_X = 0x3B
    ACC_Y = 0x3D
    ACC_Z = 0x3F

    def __init__(self, i2c):
        self.i2c = i2c
        self.addr = i2c.scan()[0]
        self.i2c.start()
        self.i2c.writeto(0x68, bytearray([107, 0])) # MPU6050 initialization
        self.i2c.stop()
        #print('Initialized MPU6050.')
        self.offx = 0
        self.offy = 0
        self.offz = 0

    @staticmethod
    def __bytes_to_int(data):
        if not data[0] & 0x80:
            return data[0] << 8 | data[1]
        return -(((data[0] ^ 0xFF) << 8) | (data[1] ^ 0xFF) + 1)

    def calibrate(self):
        print("Calibrating...")
        utime.sleep(5) # Delay to give time to position the sensor

        # Reading initial acceleration for calibration
        self.i2c.start()
        raw_acc_x = self.i2c.readfrom_mem(self.addr, MPU.ACC_X, 2)
        raw_acc_y = self.i2c.readfrom_mem(self.addr, MPU.ACC_Y, 2)
        raw_acc_z = self.i2c.readfrom_mem(self.addr, MPU.ACC_Z, 2)
        self.i2c.stop()

        acc_x = self.__bytes_to_int(raw_acc_x) / 16384 * 9.81
        acc_y = self.__bytes_to_int(raw_acc_y) / 16384 * 9.81
        acc_z = self.__bytes_to_int(raw_acc_z) / 16384 * 9.81

        # Set offsets
        self.offx = acc_x
        self.offy = acc_y
        self.offz = acc_z - 9.8

        #print("Calibration complete")
        #print("Offset X:", self.offx)
        #print("Offset Y:", self.offy)
        #print("Offset Z:", self.offz)

    def read_acceleration(self):
        self.i2c.start()
        raw_acc_x = self.i2c.readfrom_mem(self.addr, MPU.ACC_X, 2)
        raw_acc_y = self.i2c.readfrom_mem(self.addr, MPU.ACC_Y, 2)
        raw_acc_z = self.i2c.readfrom_mem(self.addr, MPU.ACC_Z, 2)
        self.i2c.stop()

        acc_x = (self.__bytes_to_int(raw_acc_x) / 16384 * 9.81) - self.offx
        acc_y = (self.__bytes_to_int(raw_acc_y) / 16384 * 9.81) - self.offy
        acc_z = (self.__bytes_to_int(raw_acc_z) / 16384 * 9.81) - self.offz

        return acc_x, acc_y, acc_z
    def is_motion_detected(self, threshold=1.0):
        acc_x, acc_y, acc_z = self.read_acceleration()
        return abs(acc_x) > threshold or abs(acc_y) > threshold or abs(acc_z-9.8) > threshold

# Initialize MPU
mpu = MPU(i2c)

# Calibrate the sensor
mpu.calibrate()

# Timer callback to read acceleration
def timer_callback(timer):
    acc_x, acc_y, acc_z = mpu.read_acceleration()
    print("X: {:.1f} Y: {:.1f} Z: {:.1f}".format(round(acc_x, 1), round(acc_y, 1), round(acc_z, 1)))

# Create and start the timer
timer1 = Timer(1)
timer1.init(period=500, callback=timer_callback)


def mycallback1(timer2):
    
    addr = socket.getaddrinfo('api.thingspeak.com',80)[0][-1]
    request = "GET https://api.thingspeak.com/channels/2331686/feeds.json?api_key=AUSTZM8VY4JM642F&results=2\r\n\r\n"

    s = socket.socket()
    s.connect(addr)
    s.send(request)
    while True:
        response = s.recv(1024)
        break
    response = response[-30:]
    #print(response)
    if'deactivate"' in response:
        np = NeoPixel(Pin(0), 1)
        np[0] = (0, 0, 0)
        np.write()
            
    elif 'activate' in response:
        np = NeoPixel(Pin(0), 1)
        np[0] = (0, 255, 0)
        np.write()
        #timer3 = Timer(3)
        mycallback3()
        #timer3.init(period=500, callback=mycallback3)
    s.close()
    
timer2 = Timer(2)
timer2.init(period=30000, callback=mycallback1)

def send_notification():
    try:
        host = 'maker.ifttt.com'
        port = 80
        addr = socket.getaddrinfo(host, port)[0][-1]
        url_path = "/trigger/sensorreceive/with/key/n62vkgKV5Bz4cVNsyFTDqdEg_Dfe7fCTE1tWRr7-6gs"
        request = "POST {} HTTP/1.1\r\nHost: {}\r\n\r\n".format(url_path, host)

        s = socket.socket()
        s.connect(addr)
        s.send(request)

        response = s.recv(1024)  # Receive the response
        print("Notification sent, response:", response)
        s.close()
    except Exception as e:
        print("Error sending notification:", e)


def mycallback3():
    led = Pin(13, Pin.OUT)
    if mpu.is_motion_detected():
        led.on()
        send_notification()
    else:
        led.off()

