class Account:
    """Main class for creation object account """
    __count = 0

    def __init__(self
                 ,account_id: int
                 ,account_number: str
                 ,balance: int = 0):

        self.__account_id = account_id
        self.__account_number = account_number
        self.__balance = balance
        Account.__count+=1
        self.__serial_number=Account.__count

    def credit(self,summa: int):
      self.__balance+=summa

    def debit(self,summa: int):
        if self.__balance >= summa:
            self.__balance-=summa

    @property
    def balance(self):
        return self.__balance

    @property
    def account_id(self):
        return self.__account_id

    @property
    def account_number(self):
        return self.__account_number

    def __len__(self):
        return 1

    def __hash__(self):
        return hash(self.account_id)

    def __repr__(self):
        return (f'Contact(account_id={self.__account_id}, '
                f'balance={self.balance}),'
                f'account_number={self.__account_number}'
                )

    def __del__(self):
        Account.__count-=1

class Collection:
    """main class for creation collection of object account """
    __count = 0

    def __init__(self,account: Account):
        self.__accounts = set()
        self.__dict_accounts = dict()
        self.add_account(account = account)
        Collection.__count += 1   # counter of objects
        self.__serial_number = Collection.__count

    def add_account(self,account: Account):
        self.__accounts.add(account)
        self.__dict_accounts[account.account_id] = account

    def get_account(self,account_id: int):
        return self.__dict_accounts.get(account_id)

    @property
    def count_of_accounts(self):
        return len(self.__accounts)

    def __del__(self):
        Collection.__count -= 1

    def __repr__(self):
        return f'Collection(accounts={self.__accounts})'



