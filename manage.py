import sys

from loguru import logger

from main import render_charts

logger.remove()
logger.add(sys.stdout, level="INFO")
logger.level('INFO', color='<blue>')


render_charts(None)
