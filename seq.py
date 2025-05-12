import pickle

from typing import Optional
from object import Object


class Seq(Object):
    __begin = 1
    __end = 100_000_000_000
    __step = 1
    __seq_name = (seq_number for seq_number in range(__begin, __end, __step))

    def __init__(self
                 , seq_name: str = None
                 , begin: Optional[int] = None
                 , end: Optional[int] = None
                 , step: Optional[int] = None
                 ):
        Object.__init__(self)
        self.__begin = begin or Seq.__begin
        self.__end = end or Seq.__end
        self.__step = step or Seq.__step
        self.__seq_name = seq_name or f'seq{next(Seq.__seq_name)}'

        self.__val = None
        self.__generator_expression = (i for i in range(self.__begin, self.__end, self.__step))
        self.__lock = False

    @property
    def seq_name(self):
        return self.seq_name

    @property
    def begin(self):
        return self.__begin

    @property
    def end(self):
        return self.__end

    @property
    def step(self):
        return self.__step

    def next_id(self):
        return self.__next__()

    def __next__(self):
        self.__val = next(self.__generator_expression)
        return self.__val

    def pickle(self):
        return self.seq_name, pickle.dumps(self)

    @property
    def lock(self):
        return self.__lock

    def __enter__(self):
        self.__lock = True
        return self

    def __exit__(self, exc_type=None, exc_val=None, exc_tb=None):
        self.__lock = False
