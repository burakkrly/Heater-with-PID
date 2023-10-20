import time

class PIDController:
    def __init__(self, setpoint, kp, ki, kd):
        self.setpoint = setpoint
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.prev_error = 0
        self.integral = 0
        self.prev_time=time.time()

    def calculate(self, current_value):
        error = self.setpoint - current_value
        self.integral += error

        delta_time=time.time()-self.prev_time
        derivative = (error - self.prev_error)/delta_time

        output = self.kp * error + self.ki * self.integral + self.kd * derivative

        self.prev_error = error
        self.prev_time = time.time()
        output = -output

        print(output)
        print(self.integral)

        return output