import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import math
import board
import time

class NTC:
    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        #self.scl = busio.I2C(board.SCL)
        #self.sda = busio.I2C(board.SDA)
        self.ads = ADS.ADS1115(i2c)
        self.ntc_positive_chan = AnalogIn(self.ads, ADS.P0)
        self.ntc_negative_chan = AnalogIn(self.ads, ADS.P2)
        self.ntc_ref_chan = AnalogIn(self.ads, ADS.P3)
        self.reference_resistance = 10000  # 10k NTC reference resistance
        self.ntc_nominal_resistance = 10000  # 10k NTC nominal resistance at 25°C
        self.ntc_nominal_temperature = 25


    def read_temperature(self):
        ntc_positive_voltage = self.ntc_positive_chan.voltage
        ntc_negative_voltage = self.ntc_negative_chan.voltage
        ntc_ref_voltage = self.ntc_ref_chan.voltage

        ntc_resistance = (self.reference_resistance * (ntc_positive_voltage - ntc_negative_voltage)) / (ntc_ref_voltage - ntc_negative_voltage)
        #print("NTC Resistance: {:.2f} ohms".format(ntc_resistance))
        #print("NTC Positive Voltage: {:.2f} V".format(ntc_positive_voltage))
        #print("NTC Negative Voltage: {:.2f} V".format(ntc_negative_voltage))
        #print("NTC Ref Voltage: {:.2f} V".format(ntc_ref_voltage))

        steinhart = math.log(ntc_resistance / self.ntc_nominal_resistance)
        steinhart /= 3950
        steinhart += 1.0 / (self.ntc_nominal_temperature + 273.15)
        steinhart = 1.0 / steinhart
        temp_celsius = steinhart - 273.15

        return temp_celsius, ntc_resistance

ntc_sensor = NTC()

if __name__ == "__main__":

    while True:
        temperature, resistance = ntc_sensor.read_temperature()
        print("Temperature: {:.2f} °C".format(temperature))
        #print("Resistance: {:.2f} ohms".format(resistance))
        time.sleep(1)
