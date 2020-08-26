import adafruit_bh1750
import board
import busio


def get_lux_readings():
    i2c = busio.I2C(board.SCL, board.SDA)
    sensor = adafruit_bh1750.BH1750(i2c)
    return {"tsl_9": sensor.lux}
