class ReferenceSetting:
    __setting = {
                "global_debug": True,
                "program_name": ["information", "system", "emulator"],
                "path_to_working_files_of_system": 'ISE_WorkingFiles',
                "path_to_db_files_of_system": 'ISE_DB'
                }
    def __init__(self):
        self.__value = ReferenceSetting.__setting

    @property
    def value(self):
        return self.__value

class InitialSettings:
    def __init__(self,setting_file):

        self.__program_name = settings.get('program_name')
        self.__path_to_working_files_of_system = settings.get('path_to_working_files_of_system')
        self.__path_to_db_files_of_system = settings.get('path_to_db_files_of_system')

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
        self.__file_name_of_sequence = 'seq'
        self.__file_name_of_account = 'account'

    @property
    def file_name_of_sequence(self):
        return self.__file_name_of_sequence

    @property
    def file_name_of_account(self):
        return self.__file_name_of_sequence
