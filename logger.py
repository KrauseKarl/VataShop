import logging
import sys
from config import DATE_FORMAT, LOG_FILE

logging.basicConfig(
    level="INFO",
    format=DATE_FORMAT,
    datefmt="%d/%b/%Y %H:%M:%S",
    filename=LOG_FILE
)
logger = logging.getLogger("vataShop")