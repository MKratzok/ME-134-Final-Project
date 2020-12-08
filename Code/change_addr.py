import adafruit_vl53l0x
from time import sleep

sleep(3)
vl53l0x = adafruit_vl53l0x.VL53L0X(i2c)
sleep(2)
vl53l0x.set_address(28)
print('I think everything worked')