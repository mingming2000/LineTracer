import time
from multi_tasks import Task


def test_func(a: int, b: int):
    time.sleep(2)
    return a + b


class TestObject:
    def __init__(self) -> None:
        self.a = 2

    def test_func(self, b: int):
        time.sleep(2)
        return self.a + b


if __name__ == "__main__":
    task = Task(task=test_func, name=None, timeout=None)
    task.start()

    _stime = time.perf_counter()
    out = task.sync_(1, 2)
    _etime = time.perf_counter()
    print(f"[SYNC] {out}, {_etime-_stime:.3f} (sec)")

    _stime = time.perf_counter()
    task.async_(1, 2)
    out = task.wait_()
    _etime = time.perf_counter()
    print(f"[SYNC] {out}, {_etime-_stime:.3f} (sec)")

    task.join()


    test_object = TestObject()
    task = Task(task=test_object.test_func, name=None, timeout=None)
    task.start()

    _stime = time.perf_counter()
    out = task.sync_(3,)
    _etime = time.perf_counter()
    print(f"[ASYNC] {out}, {_etime-_stime:.3f} (sec)")

    _stime = time.perf_counter()
    task.async_(4,)
    out = task.wait_()
    _etime = time.perf_counter()
    print(f"[ASYNC] {out}, {_etime-_stime:.3f} (sec)")

    task.join()
