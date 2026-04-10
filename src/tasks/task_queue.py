from collections.abc import Callable
from typing import Iterable, Any

from src.tasks.models.models import Task


class TaskQueue:
    """
    Ленивая обертка над коллекцией задач

    Обеспечивает потоковую обработку задач, поддерживает повторный обход
    """

    def __init__(self, iter_factory: Callable[[], Iterable[Task[Any]]]):
        self._iter_factory = iter_factory

    def __iter__(self):
        return iter(self._iter_factory())
        # for item in (self._iter_factory()):
        #     yield item

    def filter(self, predicate: Callable[[Task[Any]], bool]) -> TaskQueue:
        return TaskQueue(lambda: (task for task in self if predicate(task)))

    def cached(self) -> list[Task[Any]]:
        return list(self._iter_factory())

    # ИЛИ???
    # def cached(self) -> TaskQueue:
    #     return TaskQueue(lambda: list(self._iter_factory()))
