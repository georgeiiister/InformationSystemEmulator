import setting
import file
import pathlib

class Environment:
    def __init__(self):
        self.__initial_settings = setting.InitialSettings()
        self.__system_setting = setting.SystemSettings()

    @property
    def program_name(self):
        return ' '.join(self.__initial_settings.program_name)

    @property
    def path2program(self):
        #return pathlib.file.File.home_path()+os.sep+self.__initial_settings.directory_name_of_program
        raise NotImplemented

