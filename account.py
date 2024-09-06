import datetime
import seq
import pickle

from typing import Optional
from typing import Dict
from typing import List
from typing import Tuple
from typing import Iterable

class AccountError(Exception):
    pass

class RedBalanceError(AccountError):
    pass


class NotSetStartDateOfAction(AccountError):
    pass

class NotValidDateActivationError(AccountError):
    pass

class AccountsError(Exception):
    pass


class AccountNotFoundError(AccountsError):
    pass


class Account:
    """Main class for creation object account"""

    __count = 0
    __internal_id = 0  # internal counter of account (save value on delete object)
    __internal_generator_id = seq.Seq(seq_name='account')

    __new = 0
    __active = 1

    def __init__(self,
                 account_number: str, balance: int = 0,
                 account_id: Optional[int] = None,
                 account_collection = None,
                 describe: Optional[str] = None,
                 registration_datetime: datetime.datetime = datetime.datetime.now(),
                 activation_datetime: Optional[datetime.datetime] = None
                 ) -> None:

        self.__account_id = account_id
        self.__account_number = account_number
        self.__balance = balance
        self.__describe = describe
        self.__account_collection: Optional[Accounts] = account_collection
        self.__registration_datetime = registration_datetime


        Account.__count += 1
        Account.__internal_id = next(Account.__internal_generator_id)
        self.__internal_id = Account.__internal_id

        if not self.__account_id:
            self.__account_id = Account.__internal_id

        if activation_datetime is not None:
            self.activation(activation_datetime = activation_datetime)
        else:
            self.__state = Account.__new
            self.__activation_datetime = activation_datetime

    @property
    def account_collection(self):
        return self.__account_collection

    @account_collection.setter
    def account_collection(self, value) -> None:
        self.__account_collection = value

    def credit(self, amount: int) -> None:
        if self.activation_datetime is None:
            raise NotSetStartDateOfAction
        self.__balance += amount

    def debit(self, amount: int):
        if self.activation_datetime is None:
            raise NotSetStartDateOfAction
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

    @property
    def registration_datetime(self):
        return self.__registration_datetime

    @property
    def activation_datetime(self):
        return self.__activation_datetime

    def activation(self, activation_datetime:Optional[datetime.datetime]=None):
        activation_datetime = activation_datetime or datetime.datetime.now()

        if self.registration_datetime > activation_datetime:
            raise NotValidDateActivationError

        self.__activation_datetime = activation_datetime
        self.__state = Account.__active

    @property
    def state(self):
        return self.__state

    def __hash__(self):
        return hash(self.account_id)

    def __repr__(self):
        return (f'Account(account_id={self.account_id}'
                f', balance={self.balance}'
                f', account_number={self.account_number}'
                f', account_collection={self.account_collection}'
                f', describe={self.describe}'
                f', registration_datetime={self.registration_datetime}'
                f', activation_datetime={self.activation_datetime}'
                f')'
                )

    def __del__(self):
        Account.__count -= 1

    @property
    def pickle(self):
        return self.account_id, pickle.dumps(self)


class Accounts:
    """Main class for creation collection of accounts"""

    __count = 0
    __internal_id = 0
    __internal_generator_id = seq.Seq(seq_name='accounts')

    def __init__(self,
                 account: Account,
                 accounts_collection_id: Optional[int] = None,
                 primary: bool = False  # add as primary account in collection, accounts_property=None
                 ):

        self.__item_id = None  # internal number account in collection
        self.__accounts_collection_id = accounts_collection_id
        self.__account_ids: Dict[Account.account_id, Account] = dict()
        self.__account_numbers: List[Account.account_number] = []
        self.__accounts: Dict[int, Account] = dict()
        self.__primary_item_id: Optional[int] = None
        self.add_account(account=account, primary=primary)

        Accounts.__count += 1
        Accounts.__internal_id = next(Accounts.__internal_generator_id)

        if not self.__accounts_collection_id:
            self.__accounts_collection_id = Accounts.__internal_id  # add internal id as account collection id

    def add_account(self,
                    account: Account,
                    primary: bool = False  # add as primary account in collection
                    ):
        """Method for add object account to this account collection"""

        self.__account_ids[account.account_id] = account
        self.__account_numbers.append(account.account_number)

        self.__item_id = len(self.__account_numbers)-1
        self.__accounts[self.__item_id] = account

        account.account_collection = self  # set on account link to this collection
        if primary:
            self.__primary_item_id = self.__item_id

    def find_account_by_id(self, account_id: Account.account_id) -> Account:
        """Find account by account id (internal id account)"""

        result: Account = self.__account_ids.get(account_id)
        if not result:
            raise AccountNotFoundError
        return result

    def find_account_by_number(self, account_number: Account.account_number) -> List[Account]:
        """Find account by account number"""
        result = []
        item_id: Optional[int] = -1
        try:
            while True:
                item_id = self.__account_numbers.index(account_number, item_id+1)
                result.append(self.find_account_by_item_id(item_id))
        except ValueError:
            if not result:
                raise AccountNotFoundError
        return result

    def find_account_by_item_id(self, item_id: int) -> Account:
        """Find account by item id in collection"""

        result: Account = self.__accounts.get(item_id)  # work with dictionary accounts
        if not result:
            raise AccountNotFoundError
        return result

    @property
    def primary(self) -> Optional[Account]:
        """Method return primary account in collection"""
        if self.__primary_item_id:
            return self.find_account_by_item_id(item_id=self.__primary_item_id)

    def set_primary(self, item_id: int) -> None:
        """Method set primary account in collection"""

        result: Account = self.find_account_by_item_id(item_id=item_id)
        if not result:
            raise AccountNotFoundError
        self.__primary_item_id = item_id

    @property
    def accounts(self) -> Dict[int, Account]:
        return self.__accounts

    @property
    def count(self)-> int:
        return len(self.__accounts)

    def __del__(self) -> None:
        Accounts.__count -= 1

    def __iter__(self) -> Iterable:
        return iter(self.__accounts.items())

    def __next__(self)->Tuple[int, Account]:
        for item in self:
            return item

    def __repr__(self) -> str:
        return (f'Collection(accounts={self.__accounts}'
                f', account_collection_id=({self.__accounts_collection_id})'
                f', primary={self.primary}'
                f')')

    @property
    def accounts_collection_id(self):
        return self.__accounts_collection_id

    @property
    def pickle(self):
        return self.__accounts_collection_id, pickle.dumps(self)
