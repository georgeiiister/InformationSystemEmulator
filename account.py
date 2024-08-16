class Account:

    def __init__(self
                 , account_id: int
                 , initial_amount: int = 0):

        self.__account_id = account_id
        self.__balance = initial_amount

    @property
    def balance(self):
        return self.__balance

    @property
    def account_id(self):
        return self.__account_id