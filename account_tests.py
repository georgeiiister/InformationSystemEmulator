import account
import random

from decimal import Decimal
from account import Accounts

# pool of accounts
acc_pool = tuple((account.Account() for i in range(10)))
accounts = Accounts(accounts = acc_pool, primary_id = acc_pool[0].account_id)

# pool of activated accounts
a_acc = slice(0, int(len(acc_pool) / 2) + 1)
for account in acc_pool[a_acc]:
    account.activation()

for i, account in enumerate(acc_pool, 1):
    if account.active:
        amount: Decimal = Decimal(str(round(random.randint(1, 10_000) * random.random(), 2)))
        account.credit(amount = amount)

# pool active of account with not zero balance
acc_pool_balance = (account for account in acc_pool if account.balance > 0)
for account in acc_pool_balance:
    print(account.balance, account.state_id)


for account in acc_pool_balance:
    account.debit(amount=account.balance)
    account.close()