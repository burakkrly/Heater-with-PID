import time
from pid_fan import PidFan


def main():
    def create_pid_settings():
        return {"setpoint": 42.0, "kp": 1, "ki": 0.04, "kd": 0.3}

    def create_db_config():
        return {"host": "192.168.10.71", "database": "mydatabase", "user": "pi", "password": "1234"}

    def initialize_pid_fan(fan_pin, pid_settings, db_config):
        pid_fan = PidFan(fan_pin, pid_settings, db_config)
        return pid_fan

    fan_pin = 12
    pid_settings = create_pid_settings()
    db_config = create_db_config()

    pid_fan = initialize_pid_fan(fan_pin, pid_settings, db_config)

    try:
        while True:
            pid_fan.run()
            time.sleep(0.5)
    except KeyboardInterrupt:
        pass
    finally:
        pid_fan.close()


if __name__ == "__main__":
    main()
