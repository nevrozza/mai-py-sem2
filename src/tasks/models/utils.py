from enum import Enum


class TaskStatus(Enum):
    NEW = "NEW"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"

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

    border_top = "┌" + "─" * (width+2) + "┐"
    border_mid = "├" + "─" * (width+2) + "┤"
    border_bot = "└" + "─" * (width+2) + "┘"

    print(border_top)

    print(f"│ {lines[0]:<{width}} │")
    print(f"│ {lines[1]:<{width}} │")
    print(f"│ {lines[2]:<{width}} │")
    print(f"│ {lines[3]:<{width}} │")

    print(border_mid)

    print(f"│ {lines[4]:<{width}} │")  # Desc
    print(f"│ {lines[5]:<{width}} │")  # Data
    print(border_bot)