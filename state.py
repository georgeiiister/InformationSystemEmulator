from object import Object


class New(Object):
    def __init__(self):
        super().__init__(internal_id = 0, name = 'new', state = None)


class Active(Object):
    def __init__(self):
        super().__init__(internal_id = 1, name = 'active', state = None)


class Locked(Object):
    def __init__(self):
        super().__init__(internal_id = 2, name = 'locked', state = None)


class Closed(Object):
    def __init__(self):
        super().__init__(internal_id = 3, name = 'closed', state = None)


class Deleted(Object):
    def __init__(self):
        super().__init__(internal_id = 4, name = 'deleted', state = None)