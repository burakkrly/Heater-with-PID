import threading
import time
import RPi.GPIO as GPIO
import pid_controller
from read_temp import NTC


class PidService:
    def __init__(self):
        self.__pid_controller = pid_controller.PIDController(setpoint=43.2, kp=1, ki=0.05, kd=0.2)
        self.__ntc = NTC()
        self.__temp = 43

        self.GPIO = GPIO
        self.GPIO.setmode(GPIO.BCM)
        self.GPIO.setup(12, GPIO.OUT)
        self.pwm = GPIO.PWM(12, 25000)

        self.__pid_state = False
        self.pwm.start(0)
        self.pid_service_thread = threading.Thread(target=self.pid_thread_handle)
        self.pid_service_thread.start()

    @property
    def temperature(self):
        return self.__temp

    @property
    def pid_start(self):
        return self.__pid_state

    @pid_start.setter
    def pid_start(self, value):
        self.__pid_state = value

    def pid_thread_handle(self):
        while True:
            self.__temp = self.__ntc.read_temperature()[0]
            if self.__pid_state:
                pid_output = self.__pid_controller.calculate(self.__temp)
                pwm_duty = pid_output + 12
                fan_speed = min(max(pwm_duty, 0), 100)
                self.pwm.ChangeDutyCycle(fan_speed)
                print("Temperature:", self.__temp, "°C", "Fan Speed:", fan_speed)

            else:
                self.pwm.stop()
            print("thread içinde")

            time.sleep(0.1)

