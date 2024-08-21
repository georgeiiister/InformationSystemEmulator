class Property:
    """Main class for creation object Property"""

    def __init__(self, name, value):
        try:
            self.__properties = dict(zip(name,value))
        except TypeError:
            self.__properties = dict()
            self.__properties[name] = value

    @property
    def properties(self):
        return self.__properties

    def add_property(self,name, value):
        try:
            self.__properties = {**self.__properties,**dict(zip(name,value))}
        except TypeError:
            self.__properties = dict()
            self.__properties[name] = value

    def get_property(self,name_property):
        return self.__properties[name_property]

    def __repr__(self):
        return (f'Property(name_property={tuple(self.__properties.keys())},'
                f'value={tuple(self.__properties.values())}'
                f')')