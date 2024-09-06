from typing import Union
from typing import Optional

class Collection:
    def __init__(self,value: Union[list,tuple,str]):
        self.__value = value
        self.__item = None
        self.__count = 0
        self.__count_item = None
        self.__histogram = dict()
        self.__collection_tuple = tuple()
        self.__ucc = dict() #universal collection cache

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
        self.__collection_tuple = tuple()
        self.__ucc = dict()

    def exists_key(self, ucc_key):
        return ucc_key in self.__ucc

    def set_value_in_ucc(self,ucc_key, ucc_value):
        self.__ucc[ucc_key] = ucc_value

    def get_value_in_ucc(self,ucc_key):
        return self.__ucc.get(ucc_key)

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

    def deep_count(self):
        raise NotImplemented #DOIT

    def __len__(self):
        return self.count()

    @property
    def vector_tuple(self):
        return self.__collection_tuple or self.__value2vector_tuple()

    def __value2vector_tuple(self,value:Union[list,tuple,str] = None):
        value = value or self.collection_value
        for item in value:
            try:
                self.__collection_tuple = self.__value2vector_tuple(item)
            except TypeError:
                self.__collection_tuple += (item,)
        return self.__collection_tuple

    @property
    def deep_min_max(self):
        key_min = 'min'
        key_max = 'max'
        self.set_value_in_ucc(ucc_key = key_min,
                              ucc_value = self.get_value_in_ucc(key_min) or min(self.vector_tuple)
                              )
        self.set_value_in_ucc(ucc_key=key_max,
                              ucc_value=self.get_value_in_ucc(key_max) or max(self.vector_tuple)
                              )
        return self.get_value_in_ucc(ucc_key=key_min), self.get_value_in_ucc(ucc_key=key_max)

class CollectionNumber(Collection):
    def __init__(self,value:Union[list[int],tuple[int]]):
        Collection.__init__(self,value=value)
        self.__deep_sum = None

    @property
    def deep_sum(self):
        self.__deep_sum = self.__deep_sum or sum(self.vector_tuple)
        return self.__deep_sum
