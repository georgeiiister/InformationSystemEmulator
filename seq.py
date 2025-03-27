from typing import Optional
import pickle


class Seq:
    __begin = 1
    __end = 100_000_000_000
    __increment = 1
    __seq_name = (seq_number for seq_number in range(__begin, __end, __increment))

    def __init__(self
                 , seq_name: str = None
                 , begin: Optional[int] = None
                 , end: Optional[int] = None
                 , increment: Optional[int] = None
                 ):
        self.__begin = begin or Seq.__begin
        self.__end = end or Seq.__end
        self.__step = increment or Seq.__increment
        self.__seq_name = seq_name or f'seq{next(Seq.__seq_name)}'

        self.__val = None
        self.__iterator_expression = iter(range(self.__begin, self.__end, self.__increment))

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
    def increment(self):
        return self.__increment

    def __iter__(self):
        return self.__iterator_expression

    def __next__(self):
        for i in self:
            self.__val = i
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