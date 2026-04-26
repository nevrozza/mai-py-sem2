import asyncio

from src.tasks.models.models import Task
from src.tasks.models.utils import TaskStatus


class MockAsyncHandler:
    """Моковый-обработчик для неизвестных типов задач: просто меняет status задачи с delay"""

    def __init__(self,  delay: float = 0.15):
        self.delay = delay

    async def handle(self, task: Task) -> None:
        task.status = TaskStatus.IN_PROGRESS
        await asyncio.sleep(self.delay)
        task.status = TaskStatus.DONE
