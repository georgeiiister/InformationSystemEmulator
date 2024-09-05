from typing import Union
from typing import Optional

class Collection:
    def __init__(self,value: Union[list,tuple,str]):
        self.__value = value
        self.__item = None
        self.__count = 0
        self.__count_item = None
        self.__histogram = dict()
        self.__min_max = 0

    @property
    def collection_value(self):
        return self.__value

    @collection_value.setter
    def collection_value(self, value):
        self.__value = value
        self.__item = None
        self.__count = None
        self.__count_item = None
        self.__histogram = dict()
        self.__min_max = (None,None)

    def count(self, item: Optional = None):
        if item:
            if item == self.__item:
                return self.__count_item
            try:
                if not self.__histogram:
                    self.__histogram = {i: self.collection_value.count(item) for i in self.collection_value}
                self.__count_item = self.__histogram.get(item,0)
                return self.__count_item
            except TypeError:
                self.__count_item = len(tuple((i for i in self.collection_value if i == item)))
                return self.__count_item
        else:
            self.__count = self.__count or len(self.__value)
            return self.__count

    def __len__(self):
        return self.count()

    @property
    def min_max(self) -> Optional[tuple]:
        self.__min_max = self.__min_max or min(self.collection_value), max(self.collection_value)
        return self.__min_max

    @property
    def deep_min_max(self):
        raise NotImplemented  # DOIT

class CollectionNumber(Collection):
    def __init__(self,value:Union[list[int],tuple[int]]):
        Collection.__init__(self,value=value)
        self.__deep_sum = 0

    @property
    def deep_sum(self):
        return self.__deep_sum or self.__calculate_deep_sum()

    def __calculate_deep_sum(self,value:Optional[int] = None):
        value = value or self.collection_value
        for item in value:
            try:
                self.__deep_sum = self.__calculate_deep_sum(item)
            except TypeError:
                self.__deep_sum += item
        return self.__deep_sum