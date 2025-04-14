import logging
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "..", "logs")

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)
if os.getenv("PYCHARM_HOSTED"):
    LOG_FILE = os.path.join(LOG_DIR, "test_pycharm.log")
else:
    LOG_FILE = os.path.join(LOG_DIR, "test_terminal.log")

logger = logging.getLogger("TestLogger")
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(LOG_FILE, mode='a', encoding='utf-8')
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

if not logger.hasHandlers():
    logger.addHandler(file_handler)
