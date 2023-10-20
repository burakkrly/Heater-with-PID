import RPi.GPIO as GPIO
import time
from read_temp import NTC, ntc_sensor

fan_pin = 12

# GPIO konfigürasyonunu ayarlayın
GPIO.setmode(GPIO.BCM)
GPIO.setup(fan_pin, GPIO.OUT)

# PWM nesnesini oluşturun
pwm = GPIO.PWM(fan_pin, 25000)
while True:
    pwm.start(50)
#try:
#    while True:
#        temperature, _ = ntc_sensor.read_temperature()
#
#        if temperature >= 46:
#            pwm.start(50)
#        elif temperature <= 45:
#            pwm.start(50)
#
#        time.sleep(1)  #
#
#except KeyboardInterrupt:
#    pass
#
#finally:
#    pwm.stop()         # Program sonlandığında fanı durdur
#    GPIO.cleanup()     # GPIO pinlerini temizle
#