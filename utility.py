from typing import Union
from typing import Optional

class Collection:
    def __init__(self,value: Union[list,tuple,str]):
        self.__value = value

    @property
    def value(self):
        return self.__value

    def count(self, item: Optional = None):
        if item:
            try:
                histogram = {i: self.value.count(item) for i in self.value}
                return histogram.get(item,0)
            except TypeError:
                return len(tuple((i for i in self.value if i == item)))
        else:
            return len(self.__value)

    def __len__(self):
        return self.count()

class CollectionNumber(Collection):
    def __init__(self,value:Union[list[int],tuple[int]]):
        Collection.__init__(self,value=value)
        self.__deep_sum = 0

    def deep_sum(self):
        return self.__deep_sum or self.__calculate_deep_sum()

    def __calculate_deep_sum(self,value:Optional[int] = None):
        value = value or self.value
        for item in value:
            try:
                self.__deep_sum = self.__calculate_deep_sum(item)
            except TypeError:
                self.__deep_sum += item
        return self.__deep_sum