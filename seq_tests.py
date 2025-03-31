import seq

with seq.Seq() as s1:
    for i in range(5):
        print(next(s1))
