import logging
import sys


class Logger:
    def __init__(self, name="main"):
        # Store the name so we can refer to it
        self.name = name
        self.__setUpLogger()

    def __setUpFileHandler(self):
        file_handler = logging.FileHandler("log.txt", mode="a")
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)

    def __setUpLogger(self):
        # 1. Get a specific logger by name instead of the root
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(logging.DEBUG)

        # Clear existing handlers to prevent duplicate logs
        if self.logger.hasHandlers():
            self.logger.handlers.clear()

        # 2. File Handler (Everything to log.txt)
        self.__setUpFileHandler()

        # 3. Stream Handler (Console)
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(logging.INFO)

        # Filter: Now specifically looking for your custom name
        class NameOnlyFilter(logging.Filter):
            def __init__(self, name):
                super().__init__()
                self.target_name = name

            def filter(self, record):
                return record.name == self.target_name

        stream_handler.addFilter(NameOnlyFilter(self.name))

        stream_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        stream_handler.setFormatter(stream_formatter)
        self.logger.addHandler(stream_handler)

    def log(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)
