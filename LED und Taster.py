import sqlite3
import RPi.GPIO as GPIO
from datetime import datetime
import time

con = sqlite3.connect('sqlite.db')
cur = con.cursor()

f = open('database.sql')
sql = f.read()
cur.executescript(sql)


#cur.execute("INSERT INTO LED(is_on, timestamp) VALUES(?,?)",(True, str(datetime.now())))
#cur.execute("SELECT * FROM LED;")
#print(cur.fetchall())

GPIO.setmode(GPIO.BOARD)

class LED:
    def __init__(self, pin):
        self.pin = pin
        self.lights = False
        
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, 0)
        
    def on(self):
        GPIO.output(self.pin,1)
        self.lights = True
    
    def off(self):
        GPIO.output(self.pin,0)
        self.lights = False
        
    def is_on(self):
        return self.lights
    
class taster:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.IN)
        
    def pressed(self):
        if GPIO.input(self.pin) == GPIO.HIGH:
            return True
        else:
            return False


led = LED(37)
taster = taster(31)

try:
    while True:
        if led.is_on():
            if taster.pressed():
                time1 = time.time()
                #print(time1)
                while taster.pressed():
                    time2 = time.time()
                    #print(time2)
                if time2 - time1 <= 0.5:
                    led.off()
                    cur.execute("INSERT INTO LED(is_on, timestamp) VALUES(?,?)",(led.is_on(), str(datetime.now())))
        if led.is_on() == False:
            if taster.pressed():
                time1 = time.time()
                #print(time1)
                while taster.pressed():
                    time2 = time.time()
                    #print(time2)
                if time2 - time1 <= 0.5:
                    led.on()
                    cur.execute("INSERT INTO LED(is_on, timestamp) VALUES(?,?)",(led.is_on(), str(datetime.now())))
except KeyboardInterrupt:
    GPIO.cleanup()
    cur.execute("SELECT * FROM LED;")
    print(cur.fetchall())