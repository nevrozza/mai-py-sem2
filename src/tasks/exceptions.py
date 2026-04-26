class TaskError(Exception):
    """Базовое исключение системы задач"""


class ValidationError(TaskError):
    """Ошибка валидации данных (неверный диапазон, etc.)"""


class TaskProcessingError(TaskError):
    """Ошибка при обработке конкретной задачи"""

    def __init__(self, task_id: str, cause: Exception):
        self.task_id = task_id
        self.cause = cause
        super().__init__(f"[{task_id}] {cause}")


class BusinessLogicError(TaskError):
    """Ошибка нарушения правил логики задачи"""


class ExecutorError(TaskError):
    """Базовое исключение исполнителя задач"""


class ExecutorNotStartedError(ExecutorError):
    """Попытка использовать исполнитель до запуска"""
