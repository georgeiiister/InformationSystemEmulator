from typing import Optional

class Seq:

    __begin = 1
    __end = 100_000_000
    __increment = 1

    def __init__(self
                 , begin: Optional[int] = None
                 , end: Optional[int] = None
                 , increment: Optional[int] = None
                 ):

        self.__begin = begin or Seq.__begin
        self.__end = end or Seq.__end
        self.__step = increment or Seq.__increment

        self.__val = None
        self.__iterator_expression = iter(range(self.__begin,self.__end, self.__increment))

    @property
    def begin(self):
        return self.__begin

    @property
    def end(self):
        return self.__end

    @property
    def increment(self):
        return self.__increment

    def __iter__(self) :
        return self.__iterator_expression

    def __next__(self):
        for i in self:
            self.__val = i
            return self.__val