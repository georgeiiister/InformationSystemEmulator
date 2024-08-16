class Person:
    """Main class for create object person """

    __count = 0

    def __init__(self
                 ,person_id: int
                 ,person_name: str
                 ):

        self.__person_id = person_id
        self.__person_name = person_name
        Person.__count+=1

    @property
    def person_id(self):
        return self.__person_id

    @property
    def person_name(self):
        return self.__person_name

    def __del__(self):
        Person.__count -= 1