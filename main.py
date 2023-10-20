import time
from pid_controller import PIDController
from read_temp import NTC
import RPi.GPIO as GPIO


class Main:
    def __init__(self):

        self.target_temp = 100.0
        self.wait_time = 60
        self.stabilize_temp = 92.0
        self.min_heating_output = 20
        self.pid = PIDController(self.stabilize_temp, kp=1.0, ki=0.01, kd=0.1)
        self.temp_sensor = NTC()
        self.heating_output = 0
        GPIO.setmode(GPIO.BCM)
        self.heating_pin = 12
        GPIO.setup(self.heating_pin, GPIO.OUT)
        self.heating_pwm = GPIO.PWM(self.heating_pin, 1000)
        #Üst satırda 1000 değeri ısıtıcınn frekansına göre güncelle

    def run(self):
        print("Sıcaklık 100°C'ye çıkarılıyor...")
        while True:
            current_temp = self.temp_sensor.read_temperature()

            if current_temp >= self.target_temp:
                print("Sıcaklık 100°C'ye ulaştı. Lütfen 1 dakika bekleyiniz.")
                time.sleep(self.wait_time)

                current_temp = self.temp_sensor.read_temperature()
                self.pid.setpoint = self.stabilize_temp  # PID'nin hedef sıcaklığını güncelle

                while current_temp > self.stabilize_temp:
                    pid_output = self.pid.calculate(current_temp)
                    pid_output = min(max(pid_output, self.min_heating_output), 100)
                    print(f"Anlık Sıcaklık Değeri: {current_temp:.2f}°C | PID Çıktısı: {pid_output:.2f}")
                    self.set_heating_output(pid_output)

                    if current_temp < self.stabilize_temp - 2:
                        print("Sıcaklık 92°C'nin altında. Isıtılıyor...")
                        self.set_heating_output(self.min_heating_output + 20)

                    time.sleep(1)
                    current_temp = self.temp_sensor.read_temperature()

                    print("Sıcaklık 92°C'de sabitlendi.")
                    self.set_heating_output(0)
                    break

            time.sleep(1)

    def set_heating_output(self, output):

        self.heating_pwm.ChangeDutyCycle(min(max(output, 0), 100))
        print(f"Heating Output Set to: {output:.2f}%")


