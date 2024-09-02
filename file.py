import pathlib
import os
import seq
import datetime

class FileError(Exception):
    pass

class PositiveNumberDumpingError(FileError):
    pass


class File:
    __file_id = seq.Seq()
    __size_of_dumping = 100_000

    @staticmethod
    def home_path():
        return pathlib.Path(os.path.expanduser('~'))

    @classmethod
    def get_file_id(cls):
        return next(cls.__file_id)

    def __init__(self, path=None, size_of_dumping:int=None):
        self.__path = path or f'{File.home_path}{os.sep}information_system.file{File.get_file_id()}'
        self.__text = []
        self.__size_of_dumping = size_of_dumping or File.__size_of_dumping

    @property
    def size_of_dumping(self):
        return self.__size_of_dumping

    @size_of_dumping.setter
    def size_of_dumping(self, value):
        if value < 0:
            raise PositiveNumberDumpingError
        self.__size_of_dumping = value

    @property
    def path(self):
        return self.__path

    @path.setter
    def path(self, value):
        self.__path = value

    @property
    def view_rows(self):
        return self.__text

    def append(self, value):
        self.__text.append(value)
        if self.count_of_rows >= self.size_of_dumping:
            self.dumping()

    @property
    def count_of_rows(self):
        return len(self.view_rows)

    def clearing(self):
        self.__text.clear()

    def __write_immediate(self, value, mode='a+', end=''):
        with open(self.path, mode) as fl:
            fl.write(f'{value}{end}')

    def dumping(self, mode='a+',sep='', end='', clear=True):
        text = sep.join(self.view_rows)
        self.__write_immediate(value=text, mode=mode, end=end)
        if clear:
            self.__text.clear()


class Log(File):

    __sep = '^'

    @classmethod
    def __make_name(cls):
        return f'log{datetime.datetime.now()}_{File.get_file_id()}.log'

    def __init__(self):
        File.__init__(self, path=f'{File.home_path()}{os.sep}{Log.__make_name()}')

    def append(self, value):
        File.append(self, value=f'{datetime.datetime.now()}{Log.__sep}{value}')

    def dumping(self, mode='a+',sep='\n', end='\n', clear=True):
        File.dumping(self,mode=mode,sep=sep, end=end, clear=clear)
