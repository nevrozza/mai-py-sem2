from dataclasses import dataclass
from typing import TypeVar, Generic

T = TypeVar("T")

@dataclass(frozen=True)
class Task(Generic[T]):
    """
    TODO
    """
    id: str
    payload: T
