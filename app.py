import logging
from logging.handlers import TimedRotatingFileHandler
from flask import Flask, request, jsonify
import config
import sys
import pigpio

from m_tca9548a import get_lux_readings

app = Flask(__name__)

logger = logging.getLogger(__name__)

log_level = logging.getLevelName(config.general['log_level'])

handler = logging.handlers.RotatingFileHandler(config.general['log_file_name'],
                                               maxBytes=config.general["max_log_size"],
                                               backupCount=config.general["max_log_file_count"])

syserr_handler = logging.StreamHandler(sys.stderr)
logger.addHandler(syserr_handler)

logger.setLevel(log_level)

formatter = logging.Formatter('%(asctime)s: %(levelname)-8s: %(threadName)-12s: %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

PROCESS_NAME = "TEAPOT"
PI = pigpio.pi()


@app.route("/", methods=["GET"])
def welcome():
    return "would you like some tea?"


@app.route("/lux", methods=["GET"])
def accept_lux_get():
    message = "lux requested from: %s" % request.environ["REMOTE_ADDR"]
    logger.info(message)
    lux = get_lux()
    return lux


@app.route("/dc", methods=["POST"])
def accept_dc_post():
    if request.json:
        data = validate_dc_post_request_and_get_data(request.json)
        if data:
            if len(data) == 3:
                pin, freq, dc = data
                set_dc(pin, freq, dc)
                return "Accepted", 202

    logger.info("invalid request", str(request))
    return "send request with json payload", 400


@app.route("/dc", methods=["GET"])
def accept_dc_get():
    message = "dc requested from: %s" % request.environ["REMOTE_ADDR"]
    logger.info(message)
    pin = request.args.get('pin')
    if pin not in ('12', '13'):
        return "send request with pin number either 12 or 13", 400
    pin = int(pin)
    dc = get_dc_from_rpi(pin)
    logger.debug("dc measured as {}".format(dc))
    return jsonify({str(pin): dc})


def get_lux():
    lux = get_lux_readings(logger)
    return jsonify(lux)


def get_dc_from_request(request_json):
    logger.info(request.json)
    return request_json.get('dc')


def get_dc_from_rpi(pin):
    try:
        dc = PI.get_PWM_dutycycle(pin)
    except Exception as e:
        logger.error("error :{}".format(str(e)))
        dc = -1
    return dc


def set_dc(pin, freq, dc):
    logger.info("setting pin {0} to dc {1} at freq {2}".format(pin, freq, dc))
    PI.hardware_PWM(pin, freq, dc)
    pass


def validate_dc_post_request_and_get_data(json_obj):
    dc = json_obj.get('dc')
    if dc not in range(0, 1000001):
        return False
    freq = json_obj.get('freq')
    if freq not in range(0, 3001):
        return False
    pin = json_obj.get('pin')
    if pin not in (12, 13):
        return False
    return [pin, freq, dc]


if __name__ == "__main__":
    app.run(host="0.0.0.0")
