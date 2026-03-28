from typing import TypeVar, Protocol, Iterable, runtime_checkable

from src.tasks.models.models import Task

T = TypeVar("T")  # , covariant=True


@runtime_checkable
class TaskSource(Protocol[T]):
    """
    Протокол, описывающий источник задач
    """

    def get_tasks(self) -> Iterable[Task[T]]:
        """
        Получает поток задач из источника
        :return: Итератор задач
        """
        ...

    # mb later..
    # def get_tasks_async(self) -> AsyncIterable[Task[T]]:
    #     ...

