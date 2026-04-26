import uuid
from typing import Iterable
import random

from src.tasks.models.models import Task

TASK_TAG = "gen.num"


class GenNumberTaskSource:
    """
    Источник задач, генерирующий случайные числа
    """

    def __init__(self, tasks_count: int = 5):
        self.tasks_count = tasks_count

    def get_tasks(self) -> Iterable[Task[int]]:
        for _ in range(self.tasks_count):
            yield Task(id_=f"{TASK_TAG}_{uuid.uuid4()}", payload=random.randint(1, 100),
                       description_="RandomNumberTask",
                       priority_=random.randint(1, 100), task_type="RandomNumber")
