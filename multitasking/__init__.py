from typing import Dict, List, Any, Callable
from ._task import Task


class MultiTasking:
    r"""
        A multiprocessing framework.
        ---
        Example::
            >>> from multitasking import MultiTasking
            >>> multi_tasks = MultiTasks.registers(
            >>>    <Function0>, <Function1>, <Object.Method>)
            >>> out = multi_tasks( (1, 2), (3, 4), (10,) )
            >>> multi_tasks.join()
    """

    def __init__(self, *tasks) -> None:
        self._tasks: Dict[str, Task] = {}
        for i, task in enumerate(tasks):
            self._tasks[i] = Task(task=task, additional_idx=i)

    def __call__(self, *args) -> List[Any]:
        return self.run(*args)

    @classmethod
    def registers(cls, *tasks) -> 'MultiTasking':
        return MultiTasking(*tasks)

    def register(self, task: Callable):
        _idx = len(self._tasks)
        self._tasks[_idx] = Task(task=task, additional_idx=_idx)

    def run(self, *args) -> List[Any]:
        for (_, task_), arg in zip(self._tasks.items(), args):
            if arg is None:
                task_.async_()
            else:
                task_.async_(*arg)

        _results = []
        for _, task_ in self._tasks.items():
            _results.append( task_.wait_() )
        return _results

    def join(self):
        for _, task_ in self._tasks.items():
            task_.join()


__all__ = [
    Task,
    MultiTasking,
]

