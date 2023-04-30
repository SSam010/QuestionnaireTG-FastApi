import logging

# Enable logging
log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

logging.basicConfig(
    format=log_format, level=logging.INFO
)
logger = logging.getLogger(__name__)

# Creating object for writing to a file
handler = logging.FileHandler('log_app.log', encoding='utf-8')

formatter = logging.Formatter(log_format)
handler.setFormatter(formatter)

# Add an object to write to a file in the logger
logger.addHandler(handler)
