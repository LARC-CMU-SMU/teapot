import board
import busio
import adafruit_bh1750
import adafruit_tca9548a


def get_lux_readings(logger):
    tsl_dict = {}
    lux_dict = {}
    try:
        i2c = busio.I2C(board.SCL, board.SDA)
        tca = adafruit_tca9548a.TCA9548A(i2c)
    except Exception as e:
        logger.error("error at initiating i2c devices :{}".format(str(e)))
        return lux_dict
    for i in range(8):
        try:
            tsl_dict["tsl_{}".format(i)] = adafruit_bh1750.BH1750(tca[i])
        except Exception as e:
            logger.error("error in initiating lux sensor at {}th pin :{}".format(i, str(e)))
            pass
    for k, tsl in tsl_dict.items():
        try:
            lux_dict[k] = tsl.lux
        except Exception as e:
            logger.error("error in reading lux at {}th sensor :{}".format(i, str(e)))
            lux_dict[k] = -1
    return lux_dict
