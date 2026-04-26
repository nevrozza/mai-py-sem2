import asyncio

from src.tasks.models.models import Task
from src.tasks.models.utils import TaskStatus


class MockHandler:
    """Моковый-обработчик для неизвестных типов задач: просто меняет status задачи с delay"""

    async def handle(self, task: Task, delay: float = 0.15) -> None:
        task.status = TaskStatus.IN_PROGRESS
        await asyncio.sleep(delay)
        task.status = TaskStatus.DONE
