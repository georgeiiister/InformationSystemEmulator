from object import Object
from error import StateError

class State(Object):

    class New(Object):
        def __init__(self):
            super().__init__(internal_id = 0, name = None, state = None)


    class Active(Object):
        def __init__(self):
            super().__init__(internal_id = 1, name = None, state = None)


    class Locked(Object):
        def __init__(self):
            super().__init__(internal_id = 2, name = None, state = None)


    class Closed(Object):
        def __init__(self):
            super().__init__(internal_id = 3, name = None, state = None)


    class Deleted(Object):
        def __init__(self):
            super().__init__(internal_id = 4, name = None, state = None)


    def __init__(self):
        super().__init__(internal_id = 0, name = None, state = None)
        self.__states = {
                             'new': self.__class__.New
                            ,'active': self.__class__.Active
                            ,'locked': self.__class__.Locked
                            , 'closed': self.__class__.Closed
                            , 'deleted': self.__class__.Deleted
                         }

    def __getitem__(self, item):
        state_class = self.__states.get(item)

        if state_class is None:
            raise StateError

        state_object = state_class()
        state_object.name = item

        return state_object