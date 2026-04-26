from typing import TypeVar, Protocol, Iterable, runtime_checkable, AsyncIterable

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


@runtime_checkable
class TaskHandler(Protocol):
    """Контракт обработчика задачи.

    Любой объект с методом handle() совместим с этим контрактом.
    """

    async def handle(self, task: Task) -> None:
        """Обработать одну задачу."""
        ...

# @runtime_checkable
# class AsyncTaskSource(Protocol[T]):
#     """
#     Протокол, описывающий асинхронный источник задач
#     """
#
#     def get_tasks_async(self) -> AsyncIterable[Task[T]]:
#         """
#         Получает asyncio поток задач из источника
#         :return: Async итератор задач
#         """
#         ...
