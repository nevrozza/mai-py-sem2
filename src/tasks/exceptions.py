class TaskError(Exception):
    """Базовое исключение системы задач"""
    pass

class ValidationError(TaskError):
    """Ошибка валидации данных (неверный диапазон, etc.)"""
    pass

class BusinessLogicError(TaskError):
    """Ошибка нарушения правил логики задачи"""
    pass