class AccountError(Exception):
    pass


class RedBalanceError(AccountError):
    pass


class CollectionError(Exception):
    pass


class AccountNotFoundError(CollectionError):
    pass


class Property:
    pass


class Account:
    """Main class for creation object account"""

    __count = 0
    __internal_id = 0  # internal counter of account (save value on delete object)

    def __init__(self
                 , account_number: str
                 , balance: int = 0
                 , account_id: int | None = None
                 , account_collection = None
                 , describe: str | None = None
                 ):

        self.__account_id = account_id
        self.__account_number = account_number
        self.__balance = balance
        self.__describe = describe
        self.__account_collection = account_collection
        Account.__count += 1
        Account.__internal_id += 1
        self.__internal_id = Account.__internal_id

        if not self.__account_id:
            self.__account_id = Account.__internal_id

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
    def account_number(self):
        return self.__account_number

    @property
    def describe(self):
        return self.__describe

    @describe.setter
    def describe(self, value):
        self.__describe = value

    def __hash__(self):
        return hash(self.account_id)

    def __repr__(self):
        return (f'Contact(account_id={self.__account_id}'
                f', balance={self.balance}'
                f', account_number={self.__account_number}'
                f', account_collection={self.account_collection}'
                f')'
                )

    def __del__(self):
        Account.__count -= 1

class Accounts:
    """Main class for creation collection of accounts"""

    __count = 0
    __internal_id = 0
    __item_id = 0  # internal number account in collection

    def __init__(self
                 , account: Account
                 , accounts_collection_id: int | None = None
                 , primary: bool = False  # add as primary account in collection
                 ):

        self.__accounts_collection_id = accounts_collection_id
        self.__account_ids = dict()
        self.__account_numbers = dict()
        self.__accounts = dict()
        self.__primary_item_id = None
        self.add_account(account=account, primary=primary)

        Accounts.__count += 1
        Accounts.__internal_id += 1

        if not self.__accounts_collection_id:
            self.__accounts_id = Accounts.__internal_id # add internal id as account collection id

    def add_account(self
                    , account: Account
                    , primary: bool = False  # add as primary account in collection
                    ):
        """Method for add object account to this account collection"""

        self.__account_ids[account.account_id] = account
        self.__account_numbers[account.account_number] = account

        Accounts.__item_id += 1
        self.__accounts[Accounts.__item_id] = account

        account.accounts = self  # set on account link to this collection
        if primary:
            self.__primary_item_id = Accounts.__item_id

    def find_account_by_id(self, account_id: Account.account_id)-> Account:
        """Find account by account id (internal id account)"""

        result: Account = self.__account_ids.get(account_id)
        if not result:
            raise AccountNotFoundError
        return result

    def find_account_by_number(self, account_number: Account.account_number)-> Account:
        """Find account by account number"""

        result: Account = self.__account_numbers.get(account_number)
        if not result:
            raise AccountNotFoundError
        return result

    def find_account_by_item_id(self, item_id: int)-> Account:
        """Find account by item id in collection"""

        result: Account = self.__accounts.get(item_id)   # work with dictionary accounts
        if not result:
            raise AccountNotFoundError
        return result

    @property
    def primary(self)-> Account:
        """Method return primary account in collection"""

        return self.find_account_by_item_id(item_id=self.__primary_item_id)

    def set_primary(self, item_id: int):
        """Method set primary account in collection"""

        result = self.find_account_by_item_id(item_id=item_id)
        if not result:
            raise AccountNotFoundError
        self.__primary_item_id = item_id

    @property
    def accounts(self):
        return self.__accounts

    @property
    def count(self):
        return len(self.__accounts)

    def __del__(self):
        Accounts.__count -= 1

    def __repr__(self):
        return (f'Collection(accounts={self.__accounts}'
                f', account_collection_id=({self.__accounts_collection_id})'
                f', primary_item_id={self.__primary_item_id}'
                f')')
