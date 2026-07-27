import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s : %(message)s",
    stream=sys.stdout,
)

logger = logging.getLogger("app")
logger.setLevel(logging.INFO)
