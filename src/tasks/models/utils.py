from enum import Enum

from src.tasks.exceptions import ValidationError


class TaskStatus(Enum):
    NEW = "NEW"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"


def validate_type(value, need_to_be_type, attribute_name: str):
    if hasattr(need_to_be_type, "__args__"):  # Для Union
        type_names = f"[{", ".join(t.__name__ for t in need_to_be_type.__args__)}]"
    elif isinstance(need_to_be_type, tuple):  # Для Tuple
        type_names = f"({", ".join(t.__name__ for t in need_to_be_type)})"
    else:
        type_names = need_to_be_type.__name__

    if not isinstance(value, need_to_be_type):
        raise ValidationError(
            f"{attribute_name} must be {type_names}, got {type(value).__name__}: {value}")


def validate_not_empty(value, attribute_name: str):
    # Есть запрет на строки, заполненные пробелами
    if not value or (isinstance(value, str) and not value.strip()):
        raise ValidationError(f"{attribute_name} can't be empty")


def cut_id(idx: str) -> str:
    """:return: строку вида {id[:20]+'...'}"""
    return idx[:20] + "..."


def print_task_card(t):
    """
    Печатает красивую карточку задачки
    """
    lines = [
        f"TASK ID: {t.id}",
        f"Status:  {t.status.name}",
        f"Priority: {t.priority}",
        f"Created: {t.created_at_iso[:19]:<20}",
        f"Desc: {t.description}",
        f"Data: {t.payload}"
    ]

    max_len = max(len(line) for line in lines)
    width = max_len

    border_top = "┌" + "─" * (width + 2) + "┐"
    border_mid = "├" + "─" * (width + 2) + "┤"
    border_bot = "└" + "─" * (width + 2) + "┘"

    print(border_top)

    print(f"│ {lines[0]:<{width}} │")
    print(f"│ {lines[1]:<{width}} │")
    print(f"│ {lines[2]:<{width}} │")
    print(f"│ {lines[3]:<{width}} │")

    print(border_mid)

    print(f"│ {lines[4]:<{width}} │")  # Desc
    print(f"│ {lines[5]:<{width}} │")  # Data
    print(border_bot)
