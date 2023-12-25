
from Nema17MotorControl import Nema17MotorControl


class Main:
    def __init__(self):
        pass

    def run(self):
        # Add your code here
        
        mc = Nema17MotorControl(1, 2, 3, 4)
        mc.rotate_clockwise()
        mc.stop()

        print("Done!")


if __name__ == "__main__":
    main = Main()
    main.run()


