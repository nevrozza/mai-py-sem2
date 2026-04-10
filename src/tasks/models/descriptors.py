from src.tasks.exceptions import BusinessLogicError
from src.tasks.models.utils import TaskStatus, validate_type, validate_not_empty


class TaskStatusDescriptor:
    """
    Data Descriptor для статуса задачи (менять можно только в таком порядке: NEW -> IN_PROGRESS -> DONE)
    """
    allowed_transitions = {
        TaskStatus.NEW: [TaskStatus.NEW, TaskStatus.IN_PROGRESS, TaskStatus.DONE],
        TaskStatus.IN_PROGRESS: [TaskStatus.IN_PROGRESS, TaskStatus.DONE],
        TaskStatus.DONE: [TaskStatus.NEW],
    }

    def __set_name__(self, owner, name):
        self.name = f"_{name}"

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.name)

    def __set__(self, instance, value: TaskStatus):
        validate_type(value, TaskStatus, self.name)

        current_status = self.__get__(instance, instance.__class__)

        if value not in TaskStatusDescriptor.allowed_transitions[current_status]:
            raise BusinessLogicError(
                f"Change order: NEW -> IN_PROGRESS -> DONE, but your: {current_status} -> {value}")
        setattr(instance, self.name, value)


class ImmutableDescriptor:
    """
    `Non` Data Descriptor (неизменяемый типок)

    :param object_type: Тип данных (для валидации)
    :param name: Название _переменной, где будет храниться само значение, если передать пустую строку, то будет _"название переменной"
    :param allow_empty: Проверка на пустоту при валидации (Например, не принимаются пустые строки)
    """

    def __init__(self, object_type, name: str = "", allow_empty: bool = True):
        self.allow_empty = allow_empty
        self.object_type = object_type
        self.name = name

    def __set_name__(self, owner, name):
        if not self.name:
            self.name = f"_{name}"

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.name)

    def validate_init(self, value):
        validate_type(value, self.object_type, self.name)
        if not self.allow_empty:
            validate_not_empty(value, self.name)
