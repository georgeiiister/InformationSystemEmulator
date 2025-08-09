from decimal import Decimal


class Currency(Decimal):
    def __str__(self):
        return f'{self:>.4}'
