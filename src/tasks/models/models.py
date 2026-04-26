import datetime
from dataclasses import dataclass, InitVar, field
from typing import TypeVar, Generic, Any

from src.tasks.models.descriptors import ImmutableDescriptor, TaskStatusDescriptor
from src.tasks.models.utils import TaskStatus
from src.tasks.exceptions import ValidationError
from src.tasks.models.utils import validate_type

T = TypeVar("T")


@dataclass(slots=True)
class Task(Generic[T]):
    """
    Класс, представляющий задачу:
    description и priority защищены @property, а id, created_at и status через дескрипторы
    """

    # -------- DataClass init --------
    # (Только в payload нет дескриптора или property, поэтому он без InitVar, а также его нет в __post_init__)
    id_: InitVar[str]
    payload: T  # Пока ещё мутабельно!
    description_: InitVar[str | None]
    priority_: InitVar[int]
    task_type: Any

    # -------- Internal, используется для хранения +генерируются slots --------
    _id: str = field(init=False)  # Защищаем изменение через дескриптор
    _description: str | None = field(init=False)  # Защищаем изменение через @property (полный запрет изменений)
    _priority: int = field(init=False)  # Валидируем изменение через @property
    _created_at: datetime.datetime = field(init=False, default_factory=datetime.datetime.now,
                                           repr=False)  # Защищаем изменение через дескриптор (полный запрет изменений)
    _status: TaskStatus = field(init=False, default=TaskStatus.NEW)  # Валидируем изменение через дескриптор

    # -------- Дескрипторы и @property --------
    id = ImmutableDescriptor(str, allow_empty=False)
    created_at = ImmutableDescriptor(datetime.datetime)
    status = TaskStatusDescriptor()

    @property
    def description(self) -> str | None:
        return self._description

    @property
    def priority(self) -> int:
        return self._priority

    @priority.setter
    def priority(self, priority: int) -> None:
        if not isinstance(priority, int) or not (0 <= priority <= 100):
            raise ValidationError(f"Priority must be int [0-100], got {type(priority).__name__}: {priority}")
        self._priority = priority

    def __post_init__(self, id_: str, description_: str | None, priority_: int):
        # ImmutableDescriptor не имеет сеттера, поэтому так.
        Task.id.validate_init(id_)  # валидация
        self._id = id_  # присваивание

        validate_type(description_, str | None, "_description")  # валидация руками
        self._description = description_  # присваивание

        self.priority = priority_  # валидация и присваивание, т.к. есть свой сеттер

    @property
    def is_ready_to_work(self) -> bool:
        """Вычисляемое свойство: можно ли брать задачу в работу"""
        return self._status == TaskStatus.NEW

    @property
    def created_at_iso(self) -> str:
        """Вычисляемое свойство: время создания в ISO формате"""
        return self._created_at.isoformat()
