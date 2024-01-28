import time
from multitasking import Task


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
    test_object = TestObject()

    task0 = Task(task=test_func)
    task1 = Task(task=test_object.test_func)

    # Test
    _stime = time.perf_counter()
    out = task0.sync_(1, 2)
    _etime = time.perf_counter()
    print(f"[SYNC] {out}, {_etime-_stime:.3f} (sec)")

    _stime = time.perf_counter()
    out = task1.sync_(3,)
    _etime = time.perf_counter()
    print(f"[SYNC] {out}, {_etime-_stime:.3f} (sec)")

    _stime = time.perf_counter()
    task0.async_(1, 2)
    task1.async_(4,)
    out0 = task0.wait_()
    out1 = task1.wait_()
    _etime = time.perf_counter()
    print(f"[ASYNC] {out0}, {out1}, {_etime-_stime:.3f} (sec)")

    # Join!
    task0.join()
    task1.join()

