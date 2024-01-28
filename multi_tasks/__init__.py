from typing import Dict
from ._task import Task


class MultiTasks:
    r"""
        A multiprocessing framework.
        ---
        Example::
            >>> from multi_task import MultiTasks
            >>> multi_tasks = MultiTasks()
            >>> multi_tasks.register(
            >>>    task=<Function>, name="0", timeout=None)
            >>> multi_tasks.register(
            >>>    task=<Function>, name="1", timeout=None)
            >>> multi_tasks.register(
            >>>    task=<Object.Method>, name="2", timeout=None)
            >>> multi_tasks.start()
            >>> out = multi_tasks( (1, 2), (3, 4), (10,) )
            >>> multi_tasks.join()
    """

    def __init__(self) -> None:
        self._tasks: Dict[str, Task] = {}

    def __call__(self, *args):
        for (_, task_), arg in zip(self._tasks.items(), args):
            task_.async_(*arg)

        _results = []
        for _, task_ in self._tasks.items():
            _results.append( task_.wait_() )
        return _results

    def register(
        self, 
        task: str, 
        name: str | None = None, 
        timeout: int | float | None = None,
    ):
        _name = name if name is not None else task.__name__
        self._tasks[_name] = Task(
            name=_name,
            task=task,
            timeout=timeout
        )

    def start(self):
        for _, task_ in self._tasks.items():
            task_.start()

    def join(self):
        for _, task_ in self._tasks.items():
            task_.join()


__all__ = [
    Task,
    MultiTasks,
]

