from functools import reduce

import account
import random
from decimal import Decimal

#pool of accounts
acc_pool = tuple((account.Account() for i in range(100)))

#activing of accounts
for account in acc_pool[:int(len(acc_pool)/2)+1]:
    account.activation()

for account in acc_pool:
    if account.active:
        amount:Decimal = Decimal(str(round(random.randint(1,10_000) * random.random(),2)))
        account.credit(amount = amount)
        print(f'{account.balance:>5}')


