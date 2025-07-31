import uuid
import pickle
import seq

from object import ISObject
from typing import Optional

class Queue(ISObject):
    class QueueError(Exception):
        pass

    class QueueIsFullError(QueueError):
        pass

    class QueueIsEmptyError(QueueError):
        pass

    class QueueIsLockError(QueueError):
        pass

    __internal_generator_id = seq.Seq(seq_name='queue')
    __error_if_lock = False

    @classmethod
    def _status_lock(cls):
        return cls.__error_if_lock

    def __init__(self, size:int, error_if_lock:Optional[bool] = None):
        ISObject.__init__(self)

        self.__size = size
        self.__queue = []
        self.__status_lock = error_if_lock or self.__class__._status_lock()
        self.__error_if_lock = error_if_lock
        self.__internal_id = next(self.__class__.__internal_generator_id)

    def get(self):
        return self.__get()

    def put(self, obj):
        self.__put(obj = obj)

    @property
    def size(self):
        return self.__size

    def dump(self, path = None):
        if path is None:
            path = str(uuid.uuid1())

        with open(path,'wb+') as _file:
            pickle.dump(self, _file)

    @property
    def status_lock(self):
        result = self.__status_lock

        if result and self.__error_if_lock:
            raise self.__class__.QueueIsLockError

        return result

    @property
    def internal_id(self):
        return self.__internal_id

    def __get(self):
        if not self.__queue:
            raise Queue.QueueIsEmptyError

        if not self.__status_lock:
            return self.__queue.pop(0)

    def __put(self, obj):
        if len(self.__queue) == self.__size:
            raise self.__class__.QueueIsFullError

        if not self.__status_lock:
            self.__queue.append(obj)

    def __lock(self):
        self.__queue = True

    def __unlock(self):
        self.__status_lock = False

    def __enter__(self):
        self.__lock()

    def __exit__(self, exc_type = None, exc_val  = None, exc_tb = None):
        self.__unlock()

    def __len__(self):
        return len(self.__queue)