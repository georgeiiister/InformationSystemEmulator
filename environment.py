from setting import InitialSettings
from setting import SystemSettings
from setting import SystemDebug

from file import File
import pathlib
import os

class Environment:
    def __init__(self):
        self.__initial_settings = InitialSettings()
        self.__system_setting = SystemSettings()
        self.__system_debug = SystemDebug()

    @property
    def initial_settings(self):
        return self.__initial_settings

    @property
    def program_name(self):
        return ' '.join(self.__initial_settings.program_name)

    @property
    def path2program(self):
        return pathlib.Path(f'{File.home_dir()}'
                            f'{os.sep}'
                            f'{self.initial_settings.path_to_working_files_of_system}')

    @property
    def path2db(self):
        return pathlib.Path(f'{File.home_dir()}'
                            f'{os.sep}'
                            f'{self.initial_settings.path_to_db_files_of_system}')

