from logging import Logger
from logging import getLogger
from logging import FileHandler
from logging import StreamHandler
from logging import Formatter
from logging import DEBUG
from logging import ERROR


class LoggingManager(Logger):

    @staticmethod
    def name_logger():
        return 'information_system_emulator'

    @staticmethod
    def file_name_logger():
        return 'information_system_emulator.log'

    def __new__(cls, name=None, level=None):
        logger = getLogger(cls.name_logger())
        logger.setLevel(DEBUG)
        file_formatter = Formatter('%(asctime)s|%(levelname)s|'
                              '%(message)s')
        file_handler = FileHandler(cls.file_name_logger())
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

        #stream_handler = StreamHandler()
        #stream_handler.setLevel(ERROR)
        #logger.addHandler(stream_handler)
        return logger

    def warning(self, msg, *args):
        super().warning(msg,*args)

    def info(self, msg, *args):
        super().info(msg,*args)

    def error(self, msg, *args):
        super().error(msg,*args)