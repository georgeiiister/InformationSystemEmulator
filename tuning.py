class Tuning:
    def __init__(self):
        self.__program_name = ('information', 'system', 'emulator')
        self.__directory_name_of_program = 'ISE'
        self.__directory_name_of_db_program = 'DB_ISE'
        self.__file_name_of_sequence='seq'
        self.__file_name_of_account='account'

    @property
    def program_name(self):
        return self.__program_name

    @property
    def directory_name_of_program(self):
        return self.__directory_name_of_program

    @property
    def directory_name_of_db_program(self):
        return self.__directory_name_of_db_program

    @property
    def file_name_of_sequence(self):
        return self.__file_name_of_sequence

    @property
    def file_name_of_account(self):
        return self.__file_name_of_sequence