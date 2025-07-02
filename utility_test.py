from utility import UHash
from utility import Collection

objects = ([1,2], 100001, 'acc___', 101.12, (1,2), {3,2})

for i in objects:
    print(f'{i}: {str(UHash.hash_(i)):>25}')

o1 = Collection(value=[3,2,1,1,2,3])
o2 = Collection(value='321123')
o3 = Collection(value=(3,2,1,1,2,3))

print('get distinct items from collections')
for i in (o1,o2,o3):
    print(f'source collections = {i.collection_value}, collection with distinct items={i.distinct}')