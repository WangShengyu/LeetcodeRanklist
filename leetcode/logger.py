from flask.logging import default_handler
import logging
from .config import local_config

def init_logger(app):
    log_format = logging.Formatter('[%(asctime)s][%(levelname)s][%(filename)s:%(lineno)s][%(funcName)s] - %(message)s')
    logging.root.setLevel(logging.DEBUG)
    app.logger.removeHandler(default_handler)

    file_handler = logging.FileHandler("fsm.log")
    if local_config.log_file_level == None:
        file_handler.setLevel(logging.DEBUG)
    else:
        file_handler.setLevel(local_config.log_file_level)
    file_handler.setFormatter(log_format)
    app.logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    if local_config.log_console_level == None:
        stream_handler.setLevel(logging.WARNING)
    else:
        stream_handler.setLevel(local_config.log_console_level)
    stream_handler.setFormatter(log_format)
    app.logger.addHandler(stream_handler)

