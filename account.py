class AccountError(Exception):
    pass


class RedBalanceError(AccountError):
    pass


class CollectionError(Exception):
    pass


class AccountNotFoundError(CollectionError):
    pass


class Account:
    """Main class for creation object account"""
    __count = 0

    def __init__(self
                 , account_id: int | None
                 , number: str
                 , balance: int = 0
                 , account_collection=None
                 ):

        self.__account_id = account_id
        self.__number = number
        self.__balance = balance
        self.__account_collection = account_collection
        Account.__count += 1

        if not self.__account_id:
            self.__account_id = Account.__count

    @property
    def account_collection(self):
        return self.__account_collection

    @account_collection.setter
    def account_collection(self, value):
        self.__account_collection = value

    def credit(self, amount: int):
        self.__balance += amount

    def debit(self, amount: int):
        if self.__balance < amount:
            raise RedBalanceError
        self.__balance -= amount

    @property
    def balance(self):
        return self.__balance

    @property
    def account_id(self):
        return self.__account_id

    @property
    def number(self):
        return self.__number

    def __len__(self):
        return 1

    def __hash__(self):
        return hash(self.account_id)

    def __repr__(self):
        return (f'Contact(account_id={self.__account_id}, '
                f'balance={self.balance}),'
                f'number={self.__number}'
                )

    def __del__(self):
        Account.__count -= 1


class AccountCollection:
    """Main class for creation collection of accounts"""
    __count = 0

    def __init__(self
                 , account_collection_id: int
                 , account: Account,  # account for add to collection
                 ):

        self.__account_collection_id = account_collection_id
        self.__account_ids = dict()
        self.__account_numbers = dict()
        self.__accounts = []
        self.add_account(account=account)
        AccountCollection.__count += 1  # counter of objects

        if not self.__account_collection_id:
            self.__account_collection_id = AccountCollection.__count

    def add_account(self, account: Account):
        """Method for add object account to this account collection"""
        self.__account_ids[account.account_id] = account
        self.__account_numbers[account.number] = account
        self.__accounts.append(account)
        account.account_collection = self  # set on account link to this collection

    def find_account_by_id(self, account_id: Account.account_id):
        """Account search by account id"""
        result = self.__account_ids.get(account_id)
        if not result:
            raise AccountNotFoundError
        return result

    def find_account_by_number(self, account_number: Account.number):
        """Account search by account number"""
        result = self.__account_numbers.get(account_number)
        if not result:
            raise AccountNotFoundError
        return result

    def find_account_by_index(self, index: int):
        """Account search by serial number in collection"""
        result = None
        try:
            result = self.__accounts[index]
        except IndexError:
            raise AccountNotFoundError
        return result

    @property
    def accounts(self):
        return self.__accounts

    @property
    def count(self):
        return len(self.__accounts)

    def __del__(self):
        AccountCollection.__count -= 1

    def __repr__(self):
        return f'Collection(accounts={self.__accounts})'
