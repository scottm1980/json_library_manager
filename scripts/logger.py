import logging
from logging.handlers import RotatingFileHandler

def setup_logger(name=__name__, log_file='app.log', level=logging.INFO):
    """
    Sets up a logger with the specified name, log file, and level.
    Logs are written to both console and the specified log file.
    The log file is rotated when it reaches 5MB, keeping up to 3 backup files.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = False  # Prevents logging from propagating to the root logger multiple times

    if not logger.handlers:
        # Formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # Console Handler
        ch = logging.StreamHandler()
        ch.setLevel(level)
        ch.setFormatter(formatter)

        # File Handler with rotation
        fh = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=3)
        fh.setLevel(level)
        fh.setFormatter(formatter)

        # Add Handlers to the logger
        logger.addHandler(ch)
        logger.addHandler(fh)

    return logger
