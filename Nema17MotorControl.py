
class Nema17MotorControl:
    def __init__(self, pin1, pin2, pin3, pin4):
        self.pin1 = pin1
        self.pin2 = pin2
        self.pin3 = pin3
        self.pin4 = pin4

    def rotate_clockwise(self):
        # Code to rotate the motor clockwise
        print("Rotating clockwise")

    def rotate_counterclockwise(self):
        # Code to rotate the motor counterclockwise
        print("Rotating counterclockwise")

    def stop(self):
        # Code to stop the motor
        print("Stopping")

# Usage example
# motor = Nema17MotorControl(1, 2, 3, 4)
# motor.rotate_clockwise()
# motor.stop()
