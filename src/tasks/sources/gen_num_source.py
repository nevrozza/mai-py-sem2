import uuid
from typing import Iterable
import random

from src.tasks.models import Task

TASK_TAG = "gen.num"


class GenNumberTaskSource:
    """
    TODO
    """

    def __init__(self, tasks_count: int = 5):
        self.tasks_count = tasks_count

    def get_tasks(self) -> Iterable[Task[int]]:
        for _ in range(self.tasks_count):
            yield Task(id=f"{TASK_TAG}_{uuid.uuid4()}", payload=random.randint(1, 100))
