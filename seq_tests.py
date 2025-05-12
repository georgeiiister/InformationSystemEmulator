import seq
import threading

with seq.Seq() as s1:
    for i in range(5):
        print(next(s1), end=' ')

print()

s1 = seq.Seq()
for i in range(5):
    print(s1.next_id(), end=' ')

print()


class ThreadsTest(threading.Thread):
    def __init__(self, name, seq):
        super().__init__(name=name)
        self.__seq = seq
        self.__result = []

    def run(self):
        while True:
            try:
                sum(range(10_000_000))
                self.__result.append(next(self.__seq))
            except StopIteration:
                print(self.name + ': ' + str(self.result))
                break

    @property
    def result(self):
        return self.__result


s2 = seq.Seq(seq_name='check_thread', begin=1, step=1, end=20)

threads = (ThreadsTest(name=f'thread{i}', seq=s2) for i in range(4))

for i in threads:
    i.start()
