class Person:
    """Main class for create object person"""

    __count = 0

    def __init__(self
                 ,person_id: int
                 ,name: str
                 ):

        self.__person_id = person_id
        self.__name = name
        Person.__count+=1

    @property
    def person_id(self):
        return self.__person_id

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    def __del__(self):
        Person.__count -= 1