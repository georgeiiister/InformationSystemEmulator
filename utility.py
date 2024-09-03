from typing import Iterable
from typing import Optional

class Collection:
    def __init__(self,value:Iterable):
        self.__value = value
        self.__sum = 0

    @property
    def value(self):
        return self.__value

    @property
    def sum(self):
        return self.__sum or self.__calculate_sum()

    def __calculate_sum(self,value:Optional[int]=None):
        value = value or self.value

        for item in value:
            try:
                self.__sum = self.__calculate_sum(item)
            except TypeError:
                self.__sum += item

        return self.__sum