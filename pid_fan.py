import RPi.GPIO as GPIO
import psycopg2
from read_temp import NTC
from pid_controller import PIDController


class PidFan:
    def __init__(self, fan_pin, pid_settings, db_config):
        self.fan_pin = fan_pin
        self.pid_settings = pid_settings
        self.db_config = db_config
        self.GPIO = GPIO

        self.GPIO.setmode(GPIO.BCM)
        self.GPIO.setup(self.fan_pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.fan_pin, 25000)
        self.pwm.start(0)
        self.ntc_sensor = NTC()
        self.pid_controller = PIDController(**pid_settings)
        self.conn = psycopg2.connect(**db_config)
        self.cursor = self.conn.cursor()

    def run(self):
        temperature, _ = self.ntc_sensor.read_temperature()
        pid_out = self.pid_controller.calculate(temperature)
        pwm_duty = pid_out + 12
        fan_speed = min(max(pwm_duty, 0), 100)

        self.pwm.ChangeDutyCycle(fan_speed)

        self.cursor.execute(
            "INSERT INTO temperature_fan_data (temperature, fan_speed, pid_output, setpoint, integral) VALUES (%s, %s, %s, %s, %s) RETURNING id, timestamp",
            (temperature, fan_speed, pid_out, self.pid_controller.setpoint, self.pid_controller.integral)
        )
        self.conn.commit()

        inserted_id, inserted_timestamp = self.cursor.fetchone()
        print("Inserted ID:", inserted_id)
        print("Inserted Timestamp:", inserted_timestamp)

        print("Temperature: {:.2f} °C".format(temperature))
        print("Fan Speed: %{:.2f}".format(fan_speed))

        return temperature, fan_speed

    def close(self):
        self.pwm.stop()
        self.GPIO.cleanup()
        self.cursor.close()
        self.conn.close()
