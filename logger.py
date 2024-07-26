import logging
from config import DATE_FORMAT
from config import LOG_FILE
from config import LOG_FORMAT

logging.basicConfig(
    level=logging.DEBUG,
    format=LOG_FORMAT,
    datefmt=DATE_FORMAT,
    filename=LOG_FILE,
    filemode="a"
)
logger = logging.getLogger("vataShop")