import abc

from typing import Optional


class Object(abc.ABC):

    def __init__(
            self
            , internal_id: Optional[int] = None
            , name: Optional[str] = None
            , state: Optional[object] = None
    ):
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
        return self.internal_id == other.internal_id