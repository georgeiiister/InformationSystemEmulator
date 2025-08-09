import seq
import pickle
import json

from typing import Optional
from typing import Dict
from typing import List
from typing import Iterable
from object import ISObject
from date import DateAndTime
from currency import Currency

from error import StateError

from error_of_account import RedBalanceError
from error_of_account import ActiveBalanceError
from error_of_account import BalanceIsNotZero
from error_of_account import NotSetDateBeginOfAction
from error_of_account import NotValidDateActivationError
from error_of_account import NotValidDateCloseError
from error_of_account import CategoryOfAccountError
from error_of_account import AccountNotFoundError
from error_of_account import DeletePrimaryAccountError
from error_of_account import PrimaryAccountNotFoundError

from state import Factory as StateFactory

class Account(ISObject):
    """Main class for creation object account"""

    __count = 0
    __internal_id = 0  # internal counter of account (save value on delete object)
    __internal_generator_id = seq.Seq(seq_name='account')

    __active_account = 'a'
    __passive_account = 'p'
    __active_passive_account = 'ap'

    __slots__ = (
        '__account_id',
        '__balance',
        '__describe',
        '__registration_datetime',
        '__close_datetime',
        '__collection',
        '__id_in_collection',
        '__lock',
        '__account_id',
        '__account_number',
        '__activation_datetime',
        '__category'
    )

    @classmethod
    def category_of_account(cls) -> dict:
        return {
            cls.__active_account: 'active',
            cls.__passive_account: 'passive',
            cls.__active_passive_account: 'active_passive'
        }

    def __init__(
            self,
            account_number: str = None,
            category: int = None,
            balance: Currency = Currency('0'),
            account_id: Optional[int] = None,
            describe: Optional[str] = None,
            registration_datetime: DateAndTime = DateAndTime.now(),
            activation_datetime: Optional[DateAndTime] = None
    ) -> None:

        Account.__internal_id = next(Account.__internal_generator_id)
        ISObject.__init__(self, internal_id=Account.__internal_id)

        self.__account_id = account_id
        self.__balance = balance
        self.__describe = describe
        self.__registration_datetime = registration_datetime
        self.__close_datetime = None
        self.__collection = None
        self.__id_in_collection = None
        self.__lock = False

        if not self.__account_id:
            self.__account_id = Account.__internal_id

        self.__account_number = account_number or f'number{self.__account_id}'

        if activation_datetime is not None:
            self.activation(activation_datetime=activation_datetime)
        else:
            self.state = StateFactory()['new']
            self.__activation_datetime = None

        if category is None:
            self.__category = Account.__passive_account

        if Account.category_of_account().get(self.__category) is None:
            raise CategoryOfAccountError

        Account.__count += 1

    @property
    def collection(self):
        return self.__collection

    @property
    def id_in_collection(self):
        return self.__id_in_collection

    def set_collection(self, value, id_in_collection) -> None:
        self.__collection = value
        self.__id_in_collection = id_in_collection

    def credit(self, amount: Currency) -> None:
        if self.activation_datetime is None:
            raise NotSetDateBeginOfAction
        if abs(self.__balance) < amount and self.__category == Account.__active_account:
            raise ActiveBalanceError

        self.__balance += amount
        self.info(f'{self.account_number}({self.account_id})'
                  f', credit_amount={amount}')

    def debit(self, amount: Currency):
        if self.activation_datetime is None:
            raise NotSetDateBeginOfAction
        if self.__balance < amount and self.__category == Account.__passive_account:
            raise RedBalanceError

        self.__balance -= amount
        self.info(f'{self.account_number}({self.account_id})'
                  f', debit_amount={amount}')

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

    def activation(self, activation_datetime: Optional[DateAndTime] = None):
        activation_datetime = activation_datetime or DateAndTime.now()

        if self.registration_datetime > activation_datetime:
            raise NotValidDateActivationError

        self.__activation_datetime = activation_datetime
        self.state = StateFactory()['active']
        self.info(f'{self.account_number}({self.account_id})'
                  f', activation_date={self.__activation_datetime}')

    def close(self, close_datetime: Optional[DateAndTime] = None):
        close_datetime = close_datetime or DateAndTime.now()

        if self.registration_datetime > close_datetime:
            raise NotValidDateCloseError

        if self.balance != 0:
            _exception = BalanceIsNotZero(f'The account {self.account_number}({self.account_id})'
                                       f' cannot be closed because the '
                                       f'account balance is greater than zero')
            self.error(msg = _exception)
            raise _exception

        state_closed = StateFactory()['closed']

        if self.state == state_closed:
            raise StateError

        self.__close_datetime = close_datetime
        self.state = state_closed
        self.info(f'{self.account_number}({self.account_id})'
                  f', close_date={self.__close_datetime}')

    @property
    def close_datetime(self):
        return self.__close_datetime

    @property
    def pickle(self):
        return self.account_id, pickle.dumps(self)

    @property
    def lock(self):
        return self.__lock

    @property
    def active(self):
        return StateFactory()['active'] == self.state

    @property
    def state_id(self):
        return self.state.internal_id

    def __hash__(self):
        return hash(self.account_id)

    @property
    def dict_view(self):
        return {
            'account_id': self.__account_id
            ,'balance': self.balance
            ,'account_number': self.account_number
            ,'state_id': self.state_id
            ,'account_collection': self.__collection
            ,'describe': self.describe
            ,'registration_datetime': self.registration_datetime
            ,'activation_datetime': self.activation_datetime
            ,'close_datetime': self.close_datetime
        }

    def __str__(self):
        return str(self.dict_view)

    @property
    def jsons(self):
        result = self.dict_view
        json_time = None
        class_name = None
        result['balance'] = float(result['balance'])
        class_name = result['account_collection'].__class__.__name__
        result['account_collection'] = class_name
        try:
            json_time = result['registration_datetime'].json_time()
            result['registration_datetime'] = json_time
        except AttributeError:
            pass
        try:
            json_time = result['activation_datetime'].json_time()
            result['activation_datetime'] = json_time
        except AttributeError:
            pass
        try:
            json_time = result['close_datetime'].json_time()
            result['close_datetime'] = json_time
        except AttributeError:
            pass
        dumps = json.dumps(result,default=lambda obj: obj.raw_jsons)
        self.info(msg=f'account_json_view={dumps}')
        return dumps

    def __del__(self):
        Account.__count -= 1

    def __enter__(self):
        self.__lock = True

    def __exit__(self, exc_type=None, exc_val=None, exc_tb=None):
        self.__lock = False


class Accounts(ISObject):
    """Main class for creation collection of accounts"""

    __slots__ = (
        '__collection_id',
        '__accounts_by_id',
        '__accounts_numbers',
        '__accounts',
        '__primary_item_id',
        '__accounts_collection_id'
    )
    __count = 0
    __internal_generator_id = seq.Seq(seq_name='accounts')
    __internal_generator_account_id = seq.Seq(seq_name='account')

    def __init__(
            self,
            accounts: Iterable[Account],
            primary_id: int,
            accounts_collection_id: Optional[int] = None
    ):

        ISObject.__init__(self, internal_id=next(Accounts.__internal_generator_id))

        self.__collection_id = accounts_collection_id
        self.__accounts_by_id: Dict[Account.account_id, Account] = dict()
        self.__accounts_numbers: List[Account.account_number] = []  # list only number of account
        self.__accounts: Dict[int, Account] = dict()
        self.__primary_item_id: Optional[int] = None

        self.add_account(accounts=accounts, primary_id=primary_id)

        if not self.__collection_id:
            self.__accounts_collection_id = self.internal_id  # add internal id as account collection id

        Accounts.__count += 1

    def __add_account(self, account: Account, primary: bool = False):  # add as primary account in collection
        """Method for add object account to this account collection"""
        self.__accounts_by_id[account.account_id] = account
        self.__accounts_numbers.append(account.account_number)

        item_id = next(Accounts.__internal_generator_account_id)
        self.__accounts[item_id] = account
        if primary:
            self.__primary_item_id = item_id

        # set on account link to this collection
        account.set_collection(value=self, id_in_collection=item_id)

    def add_account(self, accounts: Iterable[Account] | Account, primary_id: Optional[Account.account_id]):
        try:
            for account in accounts:
                self.__add_account(
                    account=account,
                    primary=account.account_id == primary_id
                )
        except TypeError:
            self.__add_account(
                account=accounts,
                primary=accounts.account_id == primary_id
            )

        if self.primary is None:
            raise PrimaryAccountNotFoundError

    def account_by_id(self, account_id: int) -> Account:
        """Find account by internal id account"""
        result: Account = self.__accounts_by_id.get(account_id)
        if not result:
            raise AccountNotFoundError
        return result

    def __del_account_by_id(self, account_id: int):
        account: Account = self.account_by_id(account_id=account_id)
        self.__del_account_by_item_id(item_id=account.id_in_collection)

    def __del_account_by_item_id(self, item_id: int):
        account: Account = self.account_by_item_id(item_id=item_id)

        if account == self.primary:
            raise DeletePrimaryAccountError

        del self.__accounts_by_id[account.account_id]
        account.set_collection(value=None, id_in_collection=None)

    def account_by_number(self, account_number: str) -> List[Account]:
        """Find account by account number"""
        result = []
        item_id: Optional[int] = -1
        try:
            while True:
                item_id = self.__accounts_numbers.index(account_number, item_id + 1)
                result.append(self.account_by_item_id(item_id))
        except ValueError:
            if not result:
                raise AccountNotFoundError
        return result


    def account_by_item_id(self, item_id: int) -> Account:
        """Find account by item id in collection"""
        result: Account = self.__accounts.get(item_id)  # work with dictionary accounts
        if not result:
            raise AccountNotFoundError
        return result

    @property
    def primary(self) -> Optional[Account]:
        """Method return primary account in collection"""
        result = None
        if self.__primary_item_id:
            result = self.account_by_item_id(item_id=self.__primary_item_id)
        return result

    @primary.setter
    def primary(self, item_id: int) -> None:
        """Method set primary account in collection"""
        result: Account = self.account_by_item_id(item_id=item_id)

        if not result:
            raise AccountNotFoundError
        self.__primary_item_id = item_id

    @property
    def accounts(self) -> Dict[int, Account]:
        return self.__accounts

    def __repr__(self) -> str:
        return (
            f'Collection(accounts={self.__accounts}'
            f', account_collection_id=({self.__accounts_collection_id})'
            f', primary_id={self.primary.account_id}'
            f')'
        )

    @property
    def accounts_collection_id(self):
        return self.__accounts_collection_id

    @property
    def pickle(self):
        return self.__accounts_collection_id, pickle.dumps(self)

    def close(self):
        for item_id in self.__accounts:
            self.__accounts.get(item_id).close()

