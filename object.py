from abc import ABC

from typing import Optional
from logging_manager import LoggingManager


class Object(ABC):

    __logger = LoggingManager()


    def __init__(
            self
            , internal_id: Optional[int] = None
            , name: Optional[str] = None
            , state: Optional[object] = None
    ):
        super().__init__()
        self.__internal_id = internal_id
        self.__name = name
        self.__state = state

    @property
    def internal_id(self):
        return self.__internal_id

    @internal_id.setter
    def internal_id(self, value: str):
        self.__internal_id = value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, value: object):
        self.__state = value

    def __eq__(self, other):
        is_id = self.internal_id == other.internal_id # self.id == other.id ?
        return is_id and type(self) == type(other)

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'{self.__internal_id},{self.__name!r}'
                ,f'{self.__state})')

    def warning(self, msg, *args):
        msg = f'{msg}'
        self.__class__.__logger.warning(msg = msg,*args)

    def info(self, msg, *args):
        msg = f'{msg}'
        self.__class__.__logger.info(msg = msg,*args)