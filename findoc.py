import account
from object import Object

from decimal import Decimal

class FinDocError:
    pass


class FinDocAlreadyActual(FinDocError):
    pass


class FinDoc(Object):
    __count = 0
    __state_actual = 1
    __state_new = 0

    @classmethod
    def state_actual(cls):
        return cls.__state_actual

    @classmethod
    def state_new(cls):
        return cls.__state_new

    def __init__(self
                 , debit_account: account.Account
                 , debit_amount: Decimal
                 , credit_account: account.Account
                 , credit_amount: Decimal
                 ):
        Object.__init__(self)
        self.__debit_account = debit_account
        self.__debit_amount = debit_amount
        self.__credit_account = credit_account
        self.__credit_amount = credit_amount
        self.__state = FinDoc.state_new()

        FinDoc.__count += 1
        self.__serial_number = FinDoc.__count

    def actual(self):
        debit_completed_successfully = False
        credit_completed_successfully = False

        if self.__state > FinDoc.state_new():
            raise FinDocAlreadyActual
        try:

            self.__debit_account.debit(amount=self.__debit_amount)
            debit_completed_successfully = True
            self.__credit_account.credit(amount=self.__credit_amount)
            debit_completed_successfully = True

        except account.RedBalanceError:

            if debit_completed_successfully:
                self.__debit_account.credit(amount=self.__debit_amount)

            if credit_completed_successfully:
                self.__credit_account.debit(amount=self.__credit_amount)

        self.__state = FinDoc.state_actual()
        self.info(f'{self.__debit_account}({self.__debit_amount})'
                  f',{self.__credit_account}({self.__credit_amount}')

    @property
    def state(self):
        return self.__state
