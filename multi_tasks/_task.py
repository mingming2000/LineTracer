from typing import Callable, List, Any
import functools
import multiprocessing as mp


class Task(mp.Process):
    r"""
        A multiprocessing framework.
        ---
        Example::
            >>> from multi_task import Task
            >>> task = Task(task=<Function>, name=None, timeout=None)
            >>> task.start()
            >>> out = task.sync_(1, 2)
            >>> task.async_(1, 2)
            >>> # To do other works
            >>> out = task.wait_()
            >>> task.join()
    """

    @staticmethod
    def _loop(func: Callable):
        @functools.wraps(func)
        def _decorated(
            self: 'Task', 
            host_msg: mp.Queue,
            input_args: mp.Queue,
            output_args: mp.Queue,
        ):
            while True:
                if host_msg.get():
                    break
                args = input_args.get(timeout=self._timeout)
                output_args.put(
                    func(self._task, args), 
                    timeout=self._timeout
                )
        return _decorated

    @_loop
    def _execute_task(task: Callable, args: List[Any]):
        return task(*args)

    def __init__(
        self, 
        name: str | None = None, 
        task: Callable[..., object] | None = None, 
        timeout: int | float | None = None,
    ) -> None:
        self._task = task
        self._timeout = timeout
        self._host_msg = mp.Queue()
        self._input_args = mp.Queue()
        self._output_args = mp.Queue()
        _name = name if name is not None else task.__name__
        super().__init__(
            name=_name,
            target=self._execute_task, 
            args=(self._host_msg, self._input_args, self._output_args,),
            daemon=True
        )

    def sync_(self, *args: Any) -> Any:
        self._host_msg.put(False)
        self._input_args.put(args)
        return self._output_args.get()

    def async_(self, *args: Any) -> None:
        self._host_msg.put(False)
        self._input_args.put(args)

    def wait_(self) -> Any:
        return self._output_args.get()

    def join(self, timeout: float | None = None) -> None:
        self._host_msg.put(True)
        return super().join(timeout)
