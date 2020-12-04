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
START = [0, 180, 90, 90, 180, 0, 90, 90, 45]
EXTEND = [135, 70, 135, -1, 45, 130, 45, -1, -1]
LIFT = [-1, -1, -1, -1, -1, -1, -1, -1, -1]


class Robot:
    def __init__(self):
        self.kit = ServoKit(channels=16)
        self.lFoot = self.kit.servo[0]
        self.lAnkle = self.kit.servo[1]
        self.lKnee = self.kit.servo[2]
        self.lHip = self.kit.servo[3]
        self.rFoot = self.kit.servo[4]
        self.rAnkle = self.kit.servo[5]
        self.rKnee = self.kit.servo[6]
        self.rHip = self.kit.servo[7]
        self.wheel = self.kit.servo[8]

        self._set_all(START)


    """-------------------------------------- Parallel Movement --------------------------------------"""

    def feet(self, angle=-1):
        if angle == -1:
            return self.lFoot.angle
        else:
            self.lFoot.angle = angle
            self.rFoot.angle = 180 - angle

    def ankles(self, angle=-1):
        if angle == -1:
            return self.rAnkle.angle
        else:
            self.lAnkle.angle = 180 - angle
            self.rAnkle.angle = angle

    def knees(self, angle=-1):
        if angle == -1:
            return self.rKnee.angle - 90
        else:
            self.lKnee.angle = 90 - angle
            self.rKnee.angle = 90 + angle

    def hips(self, angle=-1):
        if angle == -1:
            return self.rHip.angle
        else:
            self.lHip.angle = 180 - angle
            self.rHip.angle = angle

    """-------------------------------------- Roll Onto Front --------------------------------------"""

    def forward_roll(self):
        self.lKnee.angle = 135
        self.lAnkle.angle = 70
        self.lFoot.angle = 135

        self.rKnee.angle = 45
        self.rAnkle.angle = 130
        self.rFoot.angle = 45

        sleep(1)

        self.curl_roll()

    def curl_roll(self):
        self.lKnee.angle = 180
        self.rKnee.angle = 0

        sleep(0.01)

        self.lFoot.angle = 0
        self.lAnkle.angle = 180

        self.rFoot.angle = 180
        self.rAnkle.angle = 0

    def un_roll(self):
        self.extend()
        sleep(0.5)
        self.reset()

    """-------------------------------------- Step (Parallel) --------------------------------------"""

    def step(self):
        self.ankles(45)
        sleep(0.1)
        self.feet(45)
        sleep(0.1)
        self.reset()

    def curl(self):
        self.knees(0)

        sleep(0.01)

        self.lFoot.angle = 0
        self.lAnkle.angle = 180

        self.rFoot.angle = 180
        self.rAnkle.angle = 0

    """-------------------------------------- Walk (Biped) --------------------------------------"""

    def walk(self, steps):
        for i in range(0, steps):
            # Brace w left
            self.lHip.angle = 135
            self.lKnee.angle = 30

            sleep(0.01)

            # Move w right
            self.rHip.angle = 0
            self.rKnee.angle = 45

            sleep(0.01)

            # Brace w right
            self.rAnkle.angle = 45
            self.rFoot.angle = 135

            sleep(0.01)

            self.lHip.angle = 135
            self.lKnee.angle = 90
            sleep(0.01)
            self.lHip.angle = 90

            # Move w both
            # self.lHip.angle =

        # self.reset()

    """-------------------------------------- Whole Body --------------------------------------"""

    def reset(self):
        self._set_all(START)

    def extend(self):
        self._set_all(EXTEND)

    def turn(self, degrees):
        """
        turn(degrees) - turns the robot in maximum steps of 45 degrees
        :param degrees: the total number of degrees to turn
        :return: none
        """
        max_angle = 60

        while degrees > 60 or degrees < -60:
            if degrees > 60:
                self.turn(60)
                degrees -= 60
            elif degrees < -60:
                self.turn(-60)
                degrees += 60

        self.kit.servo[8].angle = 60 + degrees

    """-------------------------------------- Private Helpers --------------------------------------"""

    def _set_all(self, arr):
        """
        _set_all(arr) - sets all servos to the values in arr
        :param arr: the array of ints for the servo angles. Use -1 to skip value
        :return: none
        """
        for i in range(0, len(arr)):
            if arr[i] != -1:
                self.kit.servo[i].angle = arr[i]

    def _print_all(self):
        print("lFoot:\t{}".format(self.lFoot.angle))
        print("lAnkle:\t{}".format(self.lAnkle.angle))
        print("lKnee:\t{}".format(self.lKnee.angle))
        print("lHip:\t{}".format(self.lHip.angle))
        print("rFoot:\t{}".format(self.rFoot.angle))
        print("rAnkle:\t{}".format(self.rAnkle.angle))
        print("rKnee:\t{}".format(self.rKnee.angle))
        print("rHip:\t{}".format(self.rHip.angle))
