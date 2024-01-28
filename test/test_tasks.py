import time
from multitasking import MultiTasking


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

    multi_tasks = MultiTasking.registers(
        test_func, 
        test_func, 
        test_object.test_func
    )

    _stime = time.perf_counter()
    out = multi_tasks(
        (1, 2), (3, 4), (10,)
    )
    _etime = time.perf_counter()
    print(out, _etime - _stime)

    multi_tasks.join()

