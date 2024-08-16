class LegalPerson:
    """Main class for create object legal person """

    __count = 0

    def __init__(self
                 ,legal_person_id: int
                 ,legal_person_name: str
                 ):

        self.__legal_person_id = legal_person_id
        self.__legal_person_name = legal_person_name
        LegalPerson.__count+=1

    @property
    def legal_person_id(self):
        return self.__legal_person_id

    @property
    def legal_person_name(self):
        return self.__legal_person_name

    def __del__(self):
        LegalPerson.__count -= 1