import time
from multi_tasks import MultiTasks


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

    multi_tasks = MultiTasks()
    multi_tasks.register(task=test_func, name="0")
    multi_tasks.register(task=test_func, name="1")
    multi_tasks.register(task=test_object.test_func, name="2")

    multi_tasks.start()

    _stime = time.perf_counter()
    out = multi_tasks(
        (1, 2), (3, 4), (10,)
    )
    _etime = time.perf_counter()
    print(out, _etime - _stime)

    multi_tasks.join()

