class Account:
    """Main class for creation object account """

    __count = 0

    def __init__(self
                 ,account_id: int
                 ,balance: int = 0):

        self.__account_id = account_id
        self.__balance = balance
        Account.__count+=1
        self.__serial_number=Account.__count

    @property
    def balance(self):
        return self.__balance

    @property
    def account_id(self):
        return self.__account_id

    def __len__(self):
        return 1

    def __hash__(self):
        return hash(self.account_id)

    def __repr__(self):
        return (f'Contact(account_id={self.__account_id}, '
                f'balance={self.balance})'
                )

    def __del__(self):
        Account.__count-=1


class Collection:
    """main class for creation collection of object account """
    __count = 0

    @classmethod
    def accounts_dict_from_accounts_set(cls,accounts:{Account}):
        return {account.account_id:account for account in accounts}

    def __init__(self,accounts: {Account}):
        self.__accounts = accounts
        Collection.__count+=1
        self.__serial_number = Collection.__count

    def add_accounts(self,accounts: {Account}):
        self.__accounts += accounts

    def add_account(self,account: Account):
        self.__accounts.add(account)

    @property
    def count(self):
        return len(self.__accounts)

    def __del__(self):
        self.__count -= 1

    def __repr__(self):
        return f'Collection(accounts={self.__accounts})'



