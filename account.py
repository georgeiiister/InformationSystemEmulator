import datetime
import seq
import pickle

from typing import Optional
from typing import Dict
from typing import List
from typing import Iterable


class AccountError(Exception):
    pass


class BalanceError(AccountError):
    pass


class RedBalanceError(BalanceError):
    pass


class BalanceIsNotZero(BalanceError):
    pass


class DateAccountError(AccountError):
    pass


class DateActivationError(DateAccountError):
    pass


class NotSetDateBeginOfAction(DateActivationError):
    pass


class NotValidDateActivationError(DateActivationError):
    pass


class DateCloseError(DateAccountError):
    pass


class NotValidDateCloseError(DateCloseError):
    pass


class StateError(AccountError):
    pass


class AccountsError(Exception):
    pass


class AccountNotFoundError(AccountsError):
    pass


class AccountDeleteFromCollectionError(AccountsError):
    pass


class DeletePrimaryAccount(AccountDeleteFromCollectionError):
    pass


class Account:
    """Main class for creation object account"""

    __count = 0
    __internal_id = 0  # internal counter of account (save value on delete object)
    __internal_generator_id = seq.Seq(seq_name='account')

    __states = {'__new': 0,
                '__active':  1,
                '__locked':  2,
                '__closed':  3,
                '__deleted': 4
                }

    def __init__(self,
                 account_number: str = None,
                 balance: int = 0,
                 account_id: Optional[int] = None,
                 describe: Optional[str] = None,
                 registration_datetime: datetime.datetime = datetime.datetime.now(),
                 activation_datetime: Optional[datetime.datetime] = None
                 ) -> None:

        self.__account_id = account_id
        self.__balance = balance
        self.__describe = describe
        self.__registration_datetime = registration_datetime
        self.__close_datetime = None
        self.__collection = None
        self.__id_in_collection = None

        Account.__count += 1
        Account.__internal_id = next(Account.__internal_generator_id)
        self.__internal_id = Account.__internal_id

        if not self.__account_id:
            self.__account_id = Account.__internal_id

        self.__account_number = account_number or f'number{self.__account_id}'

        if activation_datetime is not None:
            self.activation(activation_datetime=activation_datetime)
        else:
            self.__state = Account.__states.get('__new')
            self.__activation_datetime = activation_datetime

        self.__lock = False

    @property
    def collection(self):
        return self.__collection

    @property
    def id_in_collection(self):
        return self.__id_in_collection

    def set_collection(self,
                       value,
                       id_in_collection
                       ) -> None:
        self.__collection = value
        self.__id_in_collection = id_in_collection

    def credit(self, amount: int) -> None:
        if self.activation_datetime is None:
            raise NotSetDateBeginOfAction
        self.__balance += amount

    def debit(self, amount: int):
        if self.activation_datetime is None:
            raise NotSetDateBeginOfAction
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

    def activation(self,
                   activation_datetime:Optional[datetime.datetime] = None
                   ):
        activation_datetime = activation_datetime or datetime.datetime.now()

        if self.registration_datetime > activation_datetime:
            raise NotValidDateActivationError

        self.__activation_datetime = activation_datetime
        self.__state = Account.__states.get('__active')

    def close(self,
              close_datetime: Optional[datetime.datetime] = None
              ):
        close_datetime = close_datetime or datetime.datetime.now()

        if self.registration_datetime > close_datetime:
            raise NotValidDateCloseError

        if self.balance != 0:
            raise BalanceIsNotZero

        state_closed = Account.__states.get('__closed')

        if self.__states == state_closed:
            raise StateError

        self.__close_datetime = close_datetime
        self.__state = Account.__states.get('__closed')

    @property
    def state(self):
        return self.__state

    def __hash__(self):
        return hash(self.account_id)

    def __repr__(self):
        return (f'Account(account_id={self.account_id}'
                f', balance={self.balance}'
                f', account_number={self.account_number}'
                f', account_collection={self.collection}'
                f', describe={self.describe}'
                f', registration_datetime={self.registration_datetime}'
                f', activation_datetime={self.activation_datetime}'
                f', close_datetime={self.__close_datetime}'
                f')'
                )

    def __del__(self):
        Account.__count -= 1

    @property
    def pickle(self):
        return self.account_id, pickle.dumps(self)

    def __enter__(self):
        self.__lock = True

    def __exit__(self, exc_type=None, exc_val=None, exc_tb=None):
        self.__lock = False

    @property
    def lock(self):
        return self.__lock


class Accounts:
    """Main class for creation collection of accounts"""

    __internal_generator_id = seq.Seq(seq_name='accounts')
    __internal_generator_account_id = seq.Seq(seq_name='account')

    def __init__(self,
                 account: Account,
                 accounts_collection_id: Optional[int] = None,
                 primary: bool = False  # add as primary account in collection
                 ):

        self.__collection_id = accounts_collection_id
        self.__accounts_by_id: Dict[Account.account_id, Account] = dict()
        self.__accounts_numbers: List[Account.account_number] = []  # list only number of account
        self.__accounts: Dict[int, Account] = dict()
        self.__primary_item_id: Optional[int] = None

        self.add_account(account=account,
                         primary=primary
                         )

        self.__internal_id = next(Accounts.__internal_generator_id)

        if not self.__collection_id:
            self.__accounts_collection_id = self.__internal_id  # add internal id as account collection id

    def add_account(self,
                    account: Account,
                    primary: bool = False
                    ): # add as primary account in collection
        """Method for add object account to this account collection"""

        self.__accounts_by_id[account.account_id] = account
        self.__accounts_numbers.append(account.account_number)

        item_id = next(Accounts.__internal_generator_account_id)
        self.__accounts[item_id] = account
        if primary:
            self.__primary_item_id = item_id

        # set on account link to this collection
        account.set_collection(value = self,
                               id_in_collection = item_id
                              )

    def account_by_id(self,
                      account_id: Account.account_id
                      ) -> Account:
        """Find account by internal id account"""

        result: Account = self.__accounts_by_id.get(account_id)
        if not result:
            raise AccountNotFoundError
        return result

    def __del_account_by_id(self,
                            account_id: Account.account_id
                            ):
        account: Account = self.account_by_id(account_id = account_id)
        self.__del_account_by_item_id(item_id = account.id_in_collection)

    def __del_account_by_item_id(self,
                                 item_id: int
                                 ):
        account: Account = self.account_by_item_id(item_id = item_id)

        if account == self.primary:
            raise DeletePrimaryAccount

        del self.__accounts_by_id[account.account_id]
        account.set_collection(value = None, id_in_collection = None)

    def account_by_number(self,
                          account_number: Account.account_number
                          ) -> List[Account]:
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

    def __getitem__(self, item):
        """Find account by account number"""
        result = []
        item_id: Optional[int] = -1
        try:
            while True:
                item_id = self.__accounts_numbers.index(item, item_id + 1)
                result.append(self.account_by_item_id(item_id))
        except ValueError:
            if not result:
                raise AccountNotFoundError
        return result

    def account_by_item_id(self,
                           item_id: int
                           ) -> Account:
        """Find account by item id in collection"""

        result: Account = self.__accounts.get(item_id)  # work with dictionary accounts
        if not result:
            raise AccountNotFoundError
        return result

    @property
    def primary(self) -> Optional[Account]:
        """Method return primary account in collection"""
        if self.__primary_item_id:
            return self.account_by_item_id(item_id=self.__primary_item_id)

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

    @property
    def __len__(self) -> int:
        raise NotImplemented

    def __del__(self, account_id) -> None:
        self.__del_account_by_id(account_id = account_id)

    def __iter__(self) -> Iterable:
        return iter(self.__accounts.items())

    def __next__(self):
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

    def close(self):
        for item_id in self.__accounts:
            self.__accounts.get(item_id).close()