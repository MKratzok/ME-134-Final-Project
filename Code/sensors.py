import board
import busio
import adafruit_vl6180x
import adafruit_vl53l0x
from picamera import PiCamera
import time
import send_img

GAIN = [[1, adafruit_vl6180x.ALS_GAIN_1],  # 1x gain
        [1.25, adafruit_vl6180x.ALS_GAIN_1_25],  # 1.25x gain
        [1.67, adafruit_vl6180x.ALS_GAIN_1_67],  # 1.67x gain
        [2.5, adafruit_vl6180x.ALS_GAIN_2_5],  # 2.5x gain
        [5, adafruit_vl6180x.ALS_GAIN_5],  # 5x gain
        [10, adafruit_vl6180x.ALS_GAIN_10],  # 10x gain
        [20, adafruit_vl6180x.ALS_GAIN_20],  # 20x gain
        [40, adafruit_vl6180x.ALS_GAIN_40]]


class Sensors:
    def __init__(self):
        self.camera = PiCamera()
        self.camera.rotation = 180

        i2c = busio.I2C(board.SCL, board.SDA)

        try:
            self.vl53l0x = adafruit_vl53l0x.VL53L0X(i2c, address=28)
        except:
            input('Unplug VL6180 (top Time of Flight sensor)')
            # self.change_addr(i2c)
            self.vl53l0x = self.change_addr(i2c)
            input('Plug it back in and press enter to continue. ')

        try:
            self.vl6180X = adafruit_vl6180x.VL6180X(i2c)
        except:
            input('Plug in the VL6180x Sensor. Press enter to continue.')
            self.vl6180X = adafruit_vl6180x.VL6180X(i2c)
        time.sleep(0.25)

    def change_addr(self, i2c):
        time.sleep(2)
        vl53l0x = adafruit_vl53l0x.VL53L0X(i2c)
        vl53l0x.set_address(28)
        print('I think everything worked')
        return vl53l0x

    @property
    def range(self):
        def helper():
            return self.vl53l0x.range

        # x = 0
        # count = 0
        # for x in range(0, 5):
        #     count +=1
        #     x += helper()
        #
        # x = x/count
        x = helper()
        print('Range: {0}mm'.format(x))
        return x

    @property
    def range_short(self):
        def helper():
            return self.vl6180X.range

        x = 0
        count = 0
        for i in range(0, 5):
            count +=1
            x += helper()

        x = x / count

        print('Range: {0}mm'.format(x))
        return x

    @property
    def range_status(self):
        val = self.vl6180X.range_status
        print('Range Status: {}'.format(val))
        return val

    def read_lux(self, gain=1):
        def helper():
            gain_val = ''
            for v in GAIN:
                if v[0] == gain:
                    gain_val = v[1]

            if gain_val == '':
                print('ERROR: {}x gain is not available'.format(gain))
                return -1

            return self.vl6180X.read_lux(gain_val)

        x = 0
        count = 0
        for i in range(0, 5):
            count +=1
            x += helper()

        lux = x / count

        print('Light ({}x gain): '.format(gain) + '{0} lux'.format(lux))
        return lux

    def send_photo(self, sendto='kratzok@gmail.com'):
        send_img.run(self.camera, sendto)
        print('I took a picture! :)')
