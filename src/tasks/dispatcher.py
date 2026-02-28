from collections.abc import Callable
from typing import Any, Iterable

from tasks.models import Task
from tasks.sources.protocol import TaskSource


class TasksDispatcher:
    """
    TODO
    """

    def __init__(self) -> None:
        self._sources: list[TaskSource[Any]] = []

    def register_source(self, source: Any) -> None:
        """
        TODO
        :param source:
        :return:
        :raises TypeError:
        """

        class_name = type(source).__name__
        if isinstance(source, TaskSource):
            self._sources.append(source)
            print(f"da! Source {class_name} is gucci")
        else:
            raise TypeError(f"net! Class {class_name} is not TaskSource..")

    def run_tasks_flow(self) -> Iterable[Task[Any]]:
        """
        TODO
        :return:
        """
        for source in self._sources:
            yield from source.get_tasks()

    def collect(self,
                action: Callable[[Task[Any]], None]) -> None:
        """
        TODO

        Naming from kotlinx.coroutines =) flow.collect { item -> do smth }
        :param action:
        :return:
        """
        for task in self.run_tasks_flow():
            action(task)
