import os
import seq
import datetime
import json
import setting


class FileError(Exception):
    pass


class PositiveNumberDumpingError(FileError):
    pass


class FileNotExistsError(FileError):
    pass


class File:
    __file_id = seq.Seq(seq_name='file')

    @staticmethod
    def home_dir():
        return f'{os.path.expanduser("~")}{os.sep}'

    @classmethod
    def get_file_id(cls):
        return next(cls.__file_id)

    def __init__(self, path):
        self.__path = path

    @property
    def path(self):
        return self.__path

    @path.setter
    def path(self, value):
        self.__path = value

    @property
    def dir(self):
        """Get directory of file"""
        return os.path.dirname(self.path)

    def mkdir(self, name):
        """Create subdirectory"""
        os.mkdir(self.dir+os.sep+name)

    def exists(self, raise_error=True):
        result = os.path.exists(self.path)
        if raise_error and not result:
            raise FileNotExistsError
        return result


class JsonFile(File):
    def __init__(self, path=None):
        File.__init__(self, path=path)
        self.__value = None

    def __load(self):
        self.exists()
        with open(self.path, 'r') as jf:
            self.__value = json.load(jf)
        return self.__value

    @property
    def value(self):
        self.__value = self.__value or self.__load()
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value

    def get_by_key(self,key):
        return self.value.get(key)

    def set_by_key(self,key,value):
        result = self.value[key]=value
        self.value[key]=result

    def dump(self,mode='w'):
        with open(self.path, mode=mode) as fl:
            json.dump(self.__value, fl, indent=4)


class SettingFile(JsonFile):
    __setting_file_name = 'setting.json'

    @classmethod
    def setting_file_name(cls):
        return cls.__setting_file_name

    def __init__(self, path=None):
        JsonFile.__init__(self, path=path)
        if self.path:
            self.exists()
        else:
            self.path = SettingFile.setting_file_name() #working directory
            if not self.exists(raise_error=False):
                self.path = JsonFile.home_dir() + SettingFile.setting_file_name()
                self.__ref_init()

    def __ref_init(self):
        self.value = setting.ReferenceSetting().value #get reference value
        self.dump()


class TextFile(File):
    __size_of_dumping = 100_000

    def __init__(self, path=None, size_of_dumping: int = None):
        File.__init__(self, path=path)
        self.__text = []
        self.__size_of_dumping = size_of_dumping or TextFile.__size_of_dumping

    @property
    def size_of_dumping(self):
        return self.__size_of_dumping

    @size_of_dumping.setter
    def size_of_dumping(self, value):
        if value < 0:
            raise PositiveNumberDumpingError
        self.__size_of_dumping = value

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

    def dumping(self, mode='a+', sep='', end='', clear=True):
        text = sep.join(self.view_rows)
        self.__write_immediate(value=text, mode=mode, end=end)
        if clear:
            self.__text.clear()


class LogFile(TextFile):
    __sep = '^'

    @classmethod
    def __make_name(cls):
        return f'log{datetime.datetime.now()}_{File.get_file_id()}.log'

    def __init__(self,path=None):
        TextFile.__init__(self, path = path or f'{TextFile.home_dir()}{LogFile.__make_name()}')

    def append(self, value):
        TextFile.append(self, value=f'{datetime.datetime.now()}{LogFile.__sep}{value}')

    def dumping(self, mode='a+', sep='\n', end='\n', clear=True):
        TextFile.dumping(self, mode=mode, sep=sep, end=end, clear=clear)
