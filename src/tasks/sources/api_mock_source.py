import random
from typing import Iterable

from tasks.models import Task
from tasks.sources.gen_num_source import GenNumberTaskSource

TASK_TAG = "api.mock"


class APIMockTaskSource:
    """
    TODO
    """

    def __init__(self, url: str = "ya.ru", tasks_count: int = 5):
        self.url = url
        self.gen_num_source = GenNumberTaskSource(tasks_count=tasks_count)

    def get_tasks(self) -> Iterable[Task[dict]]:
        for task in self.gen_num_source.get_tasks():
            new_payload = {
                "api_source": self.url,
                "item_id": task.payload,
                "count": random.randint(1, 100)
            }
            yield Task(id=f"{TASK_TAG}_{task.id}", payload=new_payload)
