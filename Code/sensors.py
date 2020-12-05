import board
import busio
import adafruit_vl6180x
# import cv2
import time

GAIN = [[1, adafruit_vl6180x.ALS_GAIN_1],  # 1x gain
        [1.25, adafruit_vl6180x.ALS_GAIN_1_25],  # 1.25x gain
        [1.67, adafruit_vl6180x.ALS_GAIN_1_67],  # 1.67x gain
        [2.5, adafruit_vl6180x.ALS_GAIN_2_5],  # 2.5x gain
        [5, adafruit_vl6180x.ALS_GAIN_5],  # 5x gain
        [10, adafruit_vl6180x.ALS_GAIN_10],  # 10x gain
        [20, adafruit_vl6180x.ALS_GAIN_20],  # 20x gain
        [40, adafruit_vl6180x.ALS_GAIN_40]]  # 40x gain


class Sensors:
    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.vl6180X = adafruit_vl6180x.VL6180X(i2c)
        # self.cap = cv2.VideoCapture(0)
        time.sleep(0.25)

    @property
    def range(self):
        val = self.vl6180X.range
        print('Range: {0}mm'.format(val))
        return val

    @property
    def range_status(self):
        val = self.vl6180X.range_status
        print('Range Status: {}'.format(val))
        return val

    def read_lux(self, gain=1):
        gain_val = ''
        for v in GAIN:
            if v[0] == gain:
                gain_val = v[1]

        if gain_val == '':
            print('ERROR: {}x gain is not available'.format(gain))
            return -1

        lux = self.vl6180X.read_lux(gain_val)

        print('Light ({}x gain): '.format(gain) + '{0} lux'.format(lux))
        return lux

    # def _chz(self):
    #     ret, img = self.cap.read()
    #     print('I took a picture! :)')