import logging
import sys

def get_logger(name = 'DEFAULT_NAME'):
    logFormatterString = "%(asctime)s [%(name)-28.28s] [%(levelname)-5.5s]  %(message)s"
    logFormatter = logging.Formatter(logFormatterString)
    logging.basicConfig(
        filename='fetch_reviews.log',
        format = logFormatterString,
        level = logging.DEBUG
    )
    logger = logging.getLogger(name)
    consoleHandler = logging.StreamHandler(sys.stdout)
    consoleHandler.setFormatter(logFormatter)
    consoleHandler.setLevel(logging.INFO)

    logger.addHandler(consoleHandler)
    return logger
