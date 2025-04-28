import seq

with seq.Seq() as s1:
    for i in range(5):
        print(next(s1))

s1 = seq.Seq()
for i in range(5):
    print(s1.next_id())


