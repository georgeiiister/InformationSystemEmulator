from object import Object


class InformationSystemError(Object, Exception):
    pass

class StateError(InformationSystemError):
    pass
