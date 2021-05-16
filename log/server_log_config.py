import logging
import os
from logging.handlers import TimedRotatingFileHandler

from check import path_log

logging.basicConfig(
    filename=os.path.join(path_log(), "app.log"),
    format=" %(asctime)s %(levelname)s %(module)s %(message)s",
    level=logging.INFO
)

logger = logging.getLogger('basic')

rot_time = TimedRotatingFileHandler(filename=os.path.join(path_log(), "app"), when="H", interval=24, backupCount=3,
                                    utc=True)

logger.addHandler(rot_time)

if __name__ == "__main__":
    logger.info("Серверный модуль логов")
