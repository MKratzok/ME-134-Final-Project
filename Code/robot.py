from adafruit_servokit import ServoKit
from time import sleep

''' SERVO MAP:
    [0] is L Leg Foot
    [1] is L Leg Ankle
    [2] is L Leg Knee
    [3] is L Leg Hip
    [4] is R Leg Foot
    [5] is R Leg Ankle
    [6] is R Leg Knee
    [7] is R Leg Hip
    [8] is Wheel'''

# Preset Servo Angles
START = [-1, -1, -1, -1, -1, -1, -1, -1, -1]
STEP = [-1, -1, -1, -1, -1, -1, -1, -1, -1]
LIFT = [-1, -1, -1, -1, -1, -1, -1, -1, -1]

class Robot:
    def __init__(self):
        self.kit = ServoKit(channels=16)
        self._set_all(START)

    def _set_all(self, arr):
        """
        _set_all(arr) - sets all servos to the values in arr
        :param arr: the array of ints for the servo angles. Use -1 to skip value
        :return: none
        """
        for i in range(0, len(arr)):
            if arr[i] != -1:
                self.kit.servo[i].angle = arr[i]

    def step(self):
        self._set_all(STEP)

    def extend(self):
        #STUB TODO
        return

    def turn(self, degrees):
        """
        turn(degrees) - turns the robot in maximum steps of 45 degrees
        :param degrees: the total number of degrees to turn
        :return: none
        """
        while degrees > 90 or degrees < -90:
            if degrees > 90:
                self.turn(90)
                degrees -= 90
            elif degrees < -90:
                self.turn(-90)
                degrees += 90

        self.kit.servo[8].angle = 90 + degrees