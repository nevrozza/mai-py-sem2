class TaskError(Exception):
    """Базовое исключение системы задач"""


class ValidationError(TaskError):
    """Ошибка валидации данных (неверный диапазон, etc.)"""


class TaskProcessingError(TaskError):
    """Ошибка при обработке конкретной задачи"""


class BusinessLogicError(TaskProcessingError):
    """Ошибка нарушения правил логики задачи"""


class ExecutorError(TaskError):
    """Базовое исключение исполнителя задач"""


class ExecutorNotStartedError(ExecutorError):
    """Попытка использовать исполнитель до запуска"""
