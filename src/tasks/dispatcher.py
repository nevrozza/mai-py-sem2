from typing import Any, Iterable

from src.tasks.models.models import Task
from src.tasks.protocols import TaskSource
from src.tasks.task_queue import TaskQueue


class TasksDispatcher:
    """
    Диспетчер для сбора источников задач

    Работа с задачами происходит через TaskQueue (tasks)
    """

    def __init__(self) -> None:
        self._sources: list[TaskSource[Any]] = []

    def register_source(self, source: Any) -> None:
        """
        Регистрирует источник задач

        :param source: Объект, соответствующий протоколу TaskSource
        :raises TypeError: Если объект не соответствует протоколу TaskSource
        """

        class_name = type(source).__name__
        if isinstance(source, TaskSource):
            self._sources.append(source)
            # print(f"da! Source {class_name} is gucci")
        else:
            raise TypeError(f"net! Class {class_name} is not TaskSource..")

    @property
    def tasks(self) -> TaskQueue:
        """
        Возвращает TaskQueue – ленивую очередь задач
        Аккуратнее! Данные не кэшируются, а вычисляются заново каждый вызов
        Если хотите "заплатить памятью" – используйте cached()
        """
        def stream_all_tasks() -> Iterable[Task]:
            for source in self._sources:
                yield from source.get_tasks()

        return TaskQueue(stream_all_tasks)

    # def get_tasks_by_source(self, source_type) -> TaskQueue:
    #     for source in self._sources:
    #         if isinstance(source, source_type):
    #             return TaskQueue(source.get_tasks())
    #     return TaskQueue([])
