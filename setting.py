import os

class InitialSettings:
    def __init__(self):
        self.__program_name = ('information', 'system', 'emulator')
        self.__path_to_working_files_of_system = f'{os.path.expanduser("~")}{os.sep}ISE_WorkingFiles'
        self.__path_to_db_files_of_system = f'{self.__path_to_working_files_of_system}{os.sep}ISE_DB'

    @property
    def program_name(self):
        return self.__program_name

    @property
    def path_to_working_files_of_system(self):
        return self.__path_to_working_files_of_system

    @property
    def path_to_db_files_of_system(self):
        return self.__path_to_db_files_of_system


class SystemSettings:
    def __init__(self):
        self.__file_name_of_sequence='seq'
        self.__file_name_of_account='account'

    @property
    def file_name_of_sequence(self):
        return self.__file_name_of_sequence

    @property
    def file_name_of_account(self):
        return self.__file_name_of_sequence