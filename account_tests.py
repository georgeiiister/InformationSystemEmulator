import random

from account import Account
from decimal import Decimal
from account import Accounts

from error_of_account import BalanceIsNotZero

def print_info_account(balance, state, account_id):
    print('|balance:', f'{balance:>9}',
          '|state:', f'{state:<6}',
          '|id:', f'{account_id:>3}|'
          )

# pool of accounts
acc_pool = tuple((Account() for i in range(10)))
accounts = Accounts(accounts = acc_pool, primary_id = acc_pool[0].account_id)

# pool of activated accounts
a_acc = slice(0, int(len(acc_pool) / 2))

print('actions with pool of accounts:')
for account in acc_pool[a_acc]:
    print_info_account(balance=account.balance,
                       state=account.state_id,
                       account_id=account.account_id)

print('activation:')
for account in acc_pool[a_acc]:
    account.activation()
    print_info_account(balance=account.balance,
                       state=account.state_id,
                       account_id=account.account_id)

print('top up accounts')
for i, account in enumerate(acc_pool, 1):
    if account.active:
        amount: Decimal = Decimal(str(round(random.randint(1, 1000_000)
                                            * random.random(), 2)))
        account.credit(amount=amount)

# pool active of account with not zero balance
acc_pool_balance = tuple((account for account in acc_pool
                          if account.balance > 0))

for account in acc_pool_balance:

    print_info_account(balance=account.balance,
                       state=account.state_id,
                       account_id=account.account_id)
# debit

for i, account in enumerate(acc_pool_balance):
    try:
        if i>0:
            account.debit(amount=account.balance)
        account.close()
    except BalanceIsNotZero:
        pass