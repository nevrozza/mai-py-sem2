from dataclasses import dataclass
from typing import TypeVar, Generic

T = TypeVar("T")

@dataclass(frozen=True)
class Task(Generic[T]):
    """
    Класс, представляющий задачу

    :param id: Айдишник
    :param payload: Данные
    """
    id: str
    payload: T
