import random
import unittest
import json

from account import Account
from state import Factory as StateFactory

from decimal import Decimal

from error_of_account import BalanceIsNotZero


class TestAccount(unittest.TestCase):
    number_of_accounts = range(10)
    __accounts = tuple()
    __slice_of_pool = slice(0, 0)
    __accounts_for_activation = tuple()
    __print_info = False

    @staticmethod
    def __print_info_by_account(_account: Account):
        print('|balance:', f'{_account.balance:>9}',
              '|state:', f'{_account.state_id:<6}',
              '|id:', f'{_account.account_id:>3}|')

    @classmethod
    def __print_pool_of_accounts(cls, pool_account, header):
        if cls.__print_info:
            print(header)
            for item_account in pool_account:
                TestAccount.__print_info_by_account(item_account)
            print()

    @classmethod
    def setUpClass(cls):
        cls.__accounts = tuple((Account()
                                for _ in cls.number_of_accounts))

        cls.__slice_of_pool = slice(0, int(len(cls.__accounts) / 2))
        cls.__accounts_for_activation = cls.__accounts[cls.__slice_of_pool]

        cls.__print_pool_of_accounts(pool_account=cls.__accounts,
                                     header='pool of accounts:')

    def test_001_activation_of_account(self):
        __accounts = self.__class__.__accounts_for_activation
        for item_account in __accounts:
            item_account.activation()
            self.assertEqual(item_account.state, StateFactory()['active'])
        _header = 'it is accounts activated:'
        self.__class__.__print_pool_of_accounts(pool_account=__accounts,
                                                header=_header)

    def test_002_top_up_account(self):
        __accounts = self.__class__.__accounts_for_activation
        for item_account in __accounts:
            amount_of_account = Decimal(str(round(random.randint(1, 1000_000)
                                                  * random.random(), 2)))
            item_account.credit(amount=amount_of_account)
            self.assertEqual(item_account.balance, amount_of_account)

        self.__class__.__print_pool_of_accounts(pool_account=__accounts,
                                                header='credit operation:')

    def test_003_debit_account(self):
        __accounts = self.__class__.__accounts_for_activation
        for item_account in __accounts[2:]:
            item_account.debit(amount=item_account.balance)

        self.__class__.__print_pool_of_accounts(pool_account=__accounts,
                                                header='debit operation:')

    def test_004_close_account(self):
        __accounts = self.__class__.__accounts_for_activation
        for item_account in __accounts:
            try:
                item_account.close()
            except BalanceIsNotZero:
                self.assertEqual(item_account.state, StateFactory()['active'])
            else:
                self.assertEqual(item_account.state, StateFactory()['closed'])

        self.__class__.__print_pool_of_accounts(pool_account=__accounts,
                                                header='close of accounts:')
    def test_005_raw_json_view(self):
        for item_account in self.__class__.__accounts:
            _jsons = item_account.raw_json
            _jsons_etalon = json.dumps([1,2,3])
            self.assertTrue(issubclass(type(_jsons),type(_jsons_etalon)))


if __name__ == '__main__':
    unittest.main()
