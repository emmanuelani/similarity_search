import logging


def set_logger(name: str):
    # create a logger
    logger = logging.getLogger("bloomzon")
    # set logger level
    logger.setLevel(logging.DEBUG)

    # create a file and console handler
    file_handler = logging.FileHandler("log.log")
    console_handler = logging.StreamHandler()

    # set handlers formatters
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # add handler
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

