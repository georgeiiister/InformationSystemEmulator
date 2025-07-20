from object import Object
from error import StateError

class Factory(Object):

    class New(Object):
        def __init__(self, name):
            super().__init__(internal_id = 0, name = None, state = None)


    class Active(Object):
        def __init__(self, name):
            super().__init__(internal_id = 1, name = None, state = None)


    class Locked(Object):
        def __init__(self, name):
            super().__init__(internal_id = 2, name = None, state = None)


    class Closed(Object):
        def __init__(self, name):
            super().__init__(internal_id = 3, name = None, state = None)


    class Deleted(Object):
        def __init__(self, name):
            super().__init__(internal_id = 4, name = None, state = None)


    def __init__(self):
        super().__init__(internal_id = 0, name = None, state = None)
        self.__states = {
                             'new': self.__class__.New
                            , 'active': self.__class__.Active
                            , 'locked': self.__class__.Locked
                            , 'closed': self.__class__.Closed
                            , 'deleted': self.__class__.Deleted
                         }
        self.__count = 0

    def __getitem__(self, name_of_state):
        class_of_state = self.__states.get(name_of_state)

        if class_of_state is None:
            raise StateError

        state_of_object = class_of_state(name = name_of_state)
        return state_of_object

    def __iter__(self):
        return self

    def __next__(self):
        while self.__count < len(self.__states):
            name_of_state = list(self.__states.keys())[self.__count]
            class_of_state = self.__states.get(name_of_state)
            state_of_object = class_of_state(name = name_of_state)
            self.__count +=1
            return state_of_object

        raise StopIteration
