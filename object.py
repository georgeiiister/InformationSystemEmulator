import json
import datetime
import currency
from abc import ABC
from logging_manager import LoggingManager

from typing import Optional


class ISObject(ABC):

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
                f'{self.__internal_id}'
                ,f',{self.__name!r}'
                ,f'{self.__state})')

    def __format_msg(self, msg):
        return f'{self.__class__.__name__}|{msg}'

    def warning(self, msg, *args):
        self.__class__.__logger.warning(msg = self.__format_msg(msg),*args)

    def info(self, msg, *args):
        self.__class__.__logger.info(msg = self.__format_msg(msg),*args)

    def error(self, msg, *args):
        self.__class__.__logger.error(msg = self.__format_msg(msg),*args)

    @property
    def raw_jsons(self):
        dumps = json.dumps(self.__dict__, default=lambda obj: obj.raw_jsons)
        self.info(msg=f'account_json_view={dumps}')
        return dumps