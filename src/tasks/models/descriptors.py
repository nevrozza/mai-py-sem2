from src.tasks.exceptions import ValidationError, BusinessLogicError
from src.tasks.models.utils import TaskStatus


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
        return getattr(instance, self.name)

    def __set__(self, instance, value: TaskStatus):
        if not isinstance(value, TaskStatus):
            raise BusinessLogicError(f"Status of task must be `TaskStatus`, got {type(value)}")

        current_status = self.__get__(instance, instance.__class__)

        if current_status not in TaskStatusDescriptor.allowed_transitions[current_status]:
            raise BusinessLogicError(
                f"Change order: NEW -> IN_PROGRESS -> DONE, but your: {current_status} -> {value}")
        setattr(instance, self.name, value)


class ImmutableDescriptor:
    """
    Non Data Descriptor (неизменяемый типок)
    """

    def __set_name__(self, owner, name):
        self.name = f"_{name}"

    def __get__(self, instance, owner):
        return getattr(instance, self.name)
