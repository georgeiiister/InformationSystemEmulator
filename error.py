from object import Object


class InformationSystemError(Object, Exception):
    def __init__(self,*args):
        if args:
            self.name = args[0]
        else:
            self.name = self.__class__.__name__

class StateError(InformationSystemError):
    pass