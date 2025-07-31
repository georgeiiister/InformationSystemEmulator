from object import ISObject


class InformationSystemError(Exception, ISObject):
    pass


class StateError(InformationSystemError):
    pass