import pathlib
import os
import seq
import datetime


class File:
    __file_id = seq.Seq()

    @staticmethod
    def home_path():
        return pathlib.Path(os.path.expanduser('~'))

    @classmethod
    def get_file_id(cls):
        return next(File.__file_id)

    def __init__(self, path=None):
        if path is None:
            path = f'{File.home_path}{os.sep}information_system.file{File.get_file_id()}'
        self.__path = path
        self.__text = []

    @property
    def path(self):
        return self.__path

    @path.setter
    def path(self, value):
        self.__path = value

    @property
    def view(self):
        return self.__text

    def append(self, value):
        self.__text.append(value)

    def clearing(self):
        self.__text.clear()

    def __write_immediate(self, value, mode='a+', end=''):
        with open(self.path, mode) as fl:
            fl.write(f'{value}{end}')

    def dumping(self, mode='a+',sep='', end='', clear=True):
        text = sep.join(self.view)
        self.__write_immediate(value=text, mode=mode, end=end)
        if clear:
            self.__text.clear()


class Log(File):

    @classmethod
    def __make_name(cls):
        return f'log{datetime.datetime.now()}_{File.get_file_id()}.log'

    def __init__(self):
        File.__init__(self, path=f'{File.home_path()}{os.sep}{Log.__make_name()}')

    def append(self, value):
        File.append(self, value=f'{datetime.datetime.now()}^{value}')

    def dumping(self, mode='a+',sep='\n', end='\n', clear=True):
        File.dumping(self,mode=mode,sep=sep, end=end, clear=clear)
