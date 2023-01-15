import logging
import datetime


class Logger:
    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        console_handler = logging.StreamHandler()
        self.logger.addHandler(console_handler)
        self.start_time = datetime.datetime.now()

    def log(self, message):
        elapsed_time = datetime.datetime.now() - self.start_time
        hours, remainder = divmod(elapsed_time.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        elapsed_time_str = f'{hours:02d}:{minutes:02d}:{seconds:02d}'
        self.logger.info(f'[{elapsed_time_str}] {message}')


logger = Logger(__name__)
