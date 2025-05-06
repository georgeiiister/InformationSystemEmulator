import abc

from typing import Optional


class Object(abc.ABC):

    __slots__ = (
                    '__internal_id'
                    , '__name'
                    , '__state_id'
                )

    def __init__(
            self
            , internal_id: Optional[int] = None
            , name: Optional[str] = None
            , state_id: Optional[int] = None
    ):
        self.__internal_id = internal_id
        self.__name = name
        self.__state_id = state_id

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
        self.__name = name_op

    @property
    def state_id(self):
        return self.__state_id

    @state_id.setter
    def state_id(self, value: int):
        self.__state_id = value
