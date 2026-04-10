from collections.abc import Callable
from typing import Iterable, Any

from src.tasks.models.models import Task


class TaskQueue:
    """
    Ленивая обертка над коллекцией задач

    Обеспечивает потоковую обработку задач, поддерживает повторный обход

    Важно! При итерации таски "получаются" заново – чтобы избежать этого, используйте persisted
    """

    def __init__(self, iter_factory: Callable[[], Iterable[Task[Any]]]):
        self._iter_factory = iter_factory

    def __iter__(self):
        """
        Благодаря использованию фабрики, каждый вызов итератора выдаёт
        свежий поток данных. Это позволяет обходить очередь многократно,
        даже если исходные данные поступают из одноразовых генераторов
        """
        return iter(self._iter_factory())
        # for item in (self._iter_factory()):
        #     yield item

    def filter(self, predicate: Callable[[Task[Any]], bool]) -> TaskQueue:
        """
        Создает новую очередь, фильтруя задачи по заданному критерию

        Этот метод ленивый – он не выполняет фильтрацию сразу,
        а возвращает новую очередь, которая применит условие только в момент
        итерации по ней.
        """
        return TaskQueue(lambda: (task for task in self if predicate(task)))

    def persisted(self) -> TaskQueue:
        """
        Фиксирует текущее состояние очереди

        Это гарантирует, что при последующих итерациях данные не будут
        запрашиваться из источников заново, что критично для
        недетерминированных источников (например, с рандомом)
        """
        snapshot = list(self)
        return TaskQueue(lambda: snapshot)

    # ИЛИ???
    # def cached(self) -> list[Task[Any]]:
    #     return list(self._iter_factory())
