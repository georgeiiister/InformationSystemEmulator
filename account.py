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
    """Main class for creation account"""

    __count = 0
    __internal_id = 0  # internal counter of account (save value on delete object)
    __internal_generator_id = seq.Seq(seq_name='account')

    __active_account = 'a'
    __passive_account = 'p'
    __active_passive_account = 'ap'

    __slots__ = (
        '__balance',
        '__describe',
        '__registration_datetime',
        '__close_datetime',
        '__collection',
        '__id_in_collection',
        '__lock',
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
            account_number: Optional[str] = None,
            category: Optional[int] = None,
            balance: Currency = Currency('0'),
            describe: Optional[str] = None,
            registration_datetime: DateAndTime = DateAndTime.now(),
            activation_datetime: Optional[DateAndTime] = None
    ) -> None:

        Account.__internal_id = next(Account.__internal_generator_id)
        ISObject.__init__(self, internal_id=Account.__internal_id)

        self.__balance = balance
        self.__describe = describe
        self.__registration_datetime = registration_datetime
        self.__close_datetime = None
        self.__collection = None
        self.__id_in_collection = None
        self.__lock = False

        self.__account_number = account_number or f'number{self.internal_id}'

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

    @collection.setter
    def collection(self, value) -> None:
        if value:
            self.__collection = value[0]
            self.__id_in_collection = value[1]

    def credit(self, amount: Currency) -> None:
        if self.activation_datetime is None:
            raise NotSetDateBeginOfAction
        if abs(self.__balance) < amount and self.__category == Account.__active_account:
            raise ActiveBalanceError

        self.__balance += amount
        self.info(f'{self.account_number}({self.internal_id})'
                  f', credit_amount={amount}')

    def debit(self, amount: Currency):
        if self.activation_datetime is None:
            raise NotSetDateBeginOfAction
        if self.__balance < amount and self.__category == Account.__passive_account:
            raise RedBalanceError

        self.__balance -= amount
        self.info(f'{self.account_number}({self.internal_id})'
                  f', debit_amount={amount}')

    @property
    def balance(self):
        return self.__balance

    @property
    def account_id(self):
        return self.internal_id

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
        self.info(f'{self.account_number}({self.internal_id})'
                  f', activation_date={self.__activation_datetime}')

    def close(self, close_datetime: Optional[DateAndTime] = None):
        close_datetime = close_datetime or DateAndTime.now()

        if self.registration_datetime > close_datetime:
            raise NotValidDateCloseError

        if self.balance != 0:
            _exception = BalanceIsNotZero(f'The account {self.account_number}({self.internal_id})'
                                          f' cannot be closed because the '
                                          f'account balance is greater than zero')
            self.error(msg=_exception)
            raise _exception

        state_closed = StateFactory()['closed']

        if self.state == state_closed:
            raise StateError

        self.__close_datetime = close_datetime
        self.state = state_closed
        self.info(f'{self.account_number}({self.internal_id})'
                  f', close_date={self.__close_datetime}')

    @property
    def close_datetime(self):
        return self.__close_datetime

    @property
    def pickle(self):
        return self.internal_id, pickle.dumps(self)

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
        return hash(self.internal_id)

    @property
    def dict_view(self):
        return {
            'account_id': self.internal_id
            , 'balance': self.balance
            , 'account_number': self.account_number
            , 'state_id': self.state_id
            , 'account_collection': self.__collection
            , 'describe': self.describe
            , 'registration_datetime': self.registration_datetime
            , 'activation_datetime': self.activation_datetime
            , 'close_datetime': self.close_datetime
        }

    @property
    def jsons(self):
        result = self.dict_view.copy()
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
        dumps = json.dumps(result, default=lambda obj: obj.raw_jsons)
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
        '__accounts_by_id',
        '__accounts_numbers',
        '__accounts',
        '__primary_id_in_collection',
        '__accounts_collection_id'
    )
    __count = 0
    __internal_generator_id = seq.Seq(seq_name='accounts')
    __internal_generator_account_id = seq.Seq(seq_name='account')

    def __init__(
            self,
            accounts: Iterable[Account],
            primary_id: int
    ):

        ISObject.__init__(self, internal_id=next(Accounts.__internal_generator_id))

        self.__accounts: Dict[int, Account] = dict()
        self.__items = self.__accounts.items()
        self.__accounts_by_id: Dict[Account.internal_id, Account] = dict()
        self.__primary_id_in_collection: Optional[int] = None

        self.add_account(accounts=accounts, primary_id=primary_id)

        Accounts.__count += 1

    # add as primary account in collection
    def __add_account(self, account: Account, primary: bool = False):
        """Method for add object account to this account collection"""
        self.__accounts_by_id[account.internal_id] = account

        id_in_collection = next(Accounts.__internal_generator_account_id)
        self.__accounts[id_in_collection] = account
        if primary:
            self.__primary_id_in_collection = id_in_collection

        # set on account link to this collection
        account.collection = (self, id_in_collection)

    def add_account(self
                    , accounts: Iterable[Account] | Account
                    , primary_id: Optional[Account.account_id]
                    ):
        for account in accounts:
            self.__add_account(account=account, primary=(account.account_id == primary_id))

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
        self.__del_account_by_id_in_collection(id_in_collection=account.id_in_collection)

    def __del_account_by_id_in_collection(self, id_in_collection: int):
        account: Account = self.account_by_id_in_collection(id_in_collection=id_in_collection)

        if account == self.primary:
            raise DeletePrimaryAccountError

        del self.__accounts_by_id[account.internal_id]
        account.collection(value=(None, None))

    def account_by_number(self, account_number: str) -> List[Account]:
        """Find account by account number"""
        result = []
        for account in self.__accounts.values():
            if account.account_number == account_number:
                result.append(account)
        return result

    def account_by_id_in_collection(self, id_in_collection: int) -> Account:
        """Find account by item id in collection"""
        result: Account = self.__accounts.get(id_in_collection)  # work with dictionary accounts
        if not result:
            raise AccountNotFoundError
        return result

    @property
    def primary(self) -> Optional[Account]:
        """Method return primary account in collection"""
        result = None
        if self.__primary_id_in_collection:
            result = self.account_by_id_in_collection(id_in_collection=self.__primary_id_in_collection)
        return result

    @primary.setter
    def primary(self, id_in_collection: int) -> None:
        """Method set primary account in collection"""
        result: Account = self.account_by_id_in_collection(id_in_collection=id_in_collection)

        if not result:
            raise AccountNotFoundError
        self.__primary_id_in_collection = id_in_collection

    @property
    def accounts(self) -> Dict[int, Account]:
        return self.__accounts

    @property
    def pickle(self):
        return self.__accounts_collection_id, pickle.dumps(self)

    def close(self):
        for item_id in self.__accounts:
            self.__accounts.get(item_id).close()

    @property
    def dict_view(self):
        return {
            'collection_id': self.internal_id
            , 'accounts': self.accounts
            , 'primary': self.primary
        }

    @property
    def jsons(self):
        result = self.dict_view.copy()
        result['accounts'] = {item[0]: item[1].account_number for item in result.get('accounts').items()}
        result['primary'] = result.get('primary').account_number
        dumps = json.dumps(result, default=lambda obj: obj.raw_jsons)
        self.info(msg=f'accounts_json_view={dumps}')
        return dumps

    def __getitem__(self, item):
        return tuple(self.__items)[item]


