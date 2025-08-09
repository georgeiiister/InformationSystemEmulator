from datetime import datetime
from datetime import date

class DateAndTime(datetime):
    def_mask = '%d.%m.%Y %H:%M:%S'
    json_mask = '%Y-%m-%dT%H:%M:%S'

    def __str__(self):
        return self.strftime(self.__class__.def_mask)
    def json_time(self):
        return self.strftime(self.__class__.json_mask)



class OnlyDate(date):
    pass