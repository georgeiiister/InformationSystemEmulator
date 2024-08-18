import account

class FinDocError:
    pass

class FinDocAlreadyActual(FinDocError):
    pass

class FinDoc:

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
                 ,debit_account: account.Account
                 ,debit_amount:int
                 ,credit_account: account.Account
                 ,credit_amount:int
                ):

        self.__debit_account = debit_account
        self.__debit_amount = debit_amount
        self.__credit_account = credit_account
        self.__credit_amount = credit_amount
        self.__state = FinDoc.state_new()

        FinDoc.__count += 1
        self.__serial_number = FinDoc.__count

    def actual(self):
        if self.__state > FinDoc.state_new():
            raise FinDocAlreadyActual

        self.__debit_account.debit(amount = self.__debit_amount)
        self.__credit_account.credit(amount=self.__credit_amount)
        self.__state = FinDoc.state_actual()

    @property
    def state(self):
        return self.__state
