from typing import TypeVar, Protocol, Iterable, runtime_checkable

from src.tasks.models import Task

T = TypeVar("T")  # , covariant=True


@runtime_checkable
class TaskSource(Protocol[T]):
    """
    TODO
    """

    def get_tasks(self) -> Iterable[Task[T]]:
        """
        TODO
        :return:
        """
        ...

    # mb later??
    # def get_tasks_async(self) -> AsyncIterable[Task[T]]:
    #     ...
