from collections.abc import Callable
from typing import Any, Iterable

from src.tasks.models.models import Task
from src.tasks.protocols import TaskSource


class TasksDispatcher:
    """
    Диспетчер для сбора и обработки задач из различных источников
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

    def run_tasks_flow(self) -> Iterable[Task[Any]]:
        """
        Запускает поток задач из всех зарегистрированных источников
        :return: Итератор всех задач
        """
        for source in self._sources:
            yield from source.get_tasks()

    def collect(self,
                action: Callable[[Task[Any]], None]) -> None:
        """
        Выполняет действие для каждой задачи

        Взято из kotlinx.coroutines: `flow.collect { item -> smth() }`
        :param action: Функция-обработчик для одной задачи
        """
        for task in self.run_tasks_flow():
            action(task)
