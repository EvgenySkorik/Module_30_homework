import logging
from pathlib import Path

LOG_DIR = Path(__file__).resolve().parent.parent / "hw/logs"
LOG_FILE_NAME = "log.log"

LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    filename=LOG_DIR / LOG_FILE_NAME,
    filemode="a",
    format="%(asctime)s [%(name)s] [%(levelname)s] %(message)s",
    encoding="utf-8",
    force=True,
)


def get_logger(name=None):
    """Возвращает настроенный логгер"""
    logger = logging.getLogger(name or __name__)

    return logger
