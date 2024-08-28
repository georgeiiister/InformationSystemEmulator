from typing import Optional

class Seq:

    __start = 1
    __stop = 100_000_000
    __step = 1

    @classmethod
    def c_start(cls):
        return cls.__start

    @classmethod
    def c_stop(cls):
        return cls.__stop

    @classmethod
    def c_step(cls):
        return cls.__step

    def __init__(self
                 , start: Optional[int] = None
                 , stop: Optional[int] = None
                 , step: Optional[int] = None
                 ):

        if start is None:
            start = Seq.c_start()
        self.__start = start

        if stop is None:
            stop = Seq.c_stop()
        self.__stop = stop

        if step is None:
            step = Seq.c_step()
        self.__step = step

        self.__val = None
        self.__iterator_expression = iter(range(self.start,self.stop, self.step))

    @property
    def start(self):
        return self.__start

    @property
    def stop(self):
        return self.__stop

    @property
    def step(self):
        return self.__step

    def __iter__(self) :
        return self.__iterator_expression

    def __next__(self):
        for i in self:
            self.__val = i
            return self.__val