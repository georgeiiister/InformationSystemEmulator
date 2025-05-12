from utility import UHash

objects = ([1,2], 100001, 'acc___', 101.12, (1,2), {3,2})

for i in objects:
    print(f'{i}: {str(UHash.hash_(i)):>25}')
