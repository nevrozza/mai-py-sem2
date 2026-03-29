import random
import time
from typing import Iterable

from src.tasks.models.models import Task
from src.tasks.sources.gen_num_source import GenNumberTaskSource

TASK_TAG = "api.mock"


class APIMockTaskSource:
    """
    Источник задач, имитирующий API-запрос

    Под капотом используется `GenNumberTaskSource`
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
            yield Task(id_=f"{TASK_TAG}_{task.id}", payload=new_payload, description_="ApiMockTask",
                       priority_=random.randint(1, 100))
            time.sleep(0.5)
