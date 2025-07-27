from object import Object


class InformationSystemError(Exception,Object):
    pass


class StateError(InformationSystemError):
    pass