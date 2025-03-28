from functools import reduce

import account

#pool of accounts
acc_pool = tuple((account.Account() for i in range(10)))

#activing of accounts
active_acc_pool = ((account, account.activation()) for account in acc_pool[:int(len(acc_pool)/2)+1])
active_acc_pool = tuple(account[0] for account in active_acc_pool)

for i in active_acc_pool:
    print(i.state)