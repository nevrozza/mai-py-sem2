import pytest
import asyncio

from src.tasks.asyncio.async_task_executor import AsyncTaskExecutor
from src.tasks.models.models import Task
from src.tasks.models.utils import TaskStatus, cut_id
from src.tasks.exceptions import ExecutorNotStartedError, ExecutorError


@pytest.fixture
async def executor():
    """Фикстура для создания и автоматической остановки исполнителя"""
    async with AsyncTaskExecutor(2) as ex:
        yield ex


@pytest.fixture
def sample_task():
    return Task(
        id_="test_1",
        payload=42,
        description_="TestTask",
        priority_=10,
        task_type="test_type"
    )


class TestHandler:
    """
    Моковый обработчик для тестов.
    Позволяет проверять количество вызовов и имитировать задержку и ошибку
    """

    def __init__(self, delay: float = 0, should_fail: bool = False):
        self.delay = delay
        self.should_fail = should_fail
        self.call_count = 0
        self.processed_tasks: list[Task] = []

    async def handle(self, task: Task) -> None:
        self.call_count += 1
        self.processed_tasks.append(task)

        task.status = TaskStatus.IN_PROGRESS

        await asyncio.sleep(self.delay)

        if self.should_fail:
            raise Exception(f"Mock error for task {cut_id(task.id)}")

        task.status = TaskStatus.DONE

    def called_once_with(self, task: Task) -> bool:
        """Вспомогательный метод для удобства тестов – когда handler использовался единожды"""
        return self.call_count == 1 and self.processed_tasks[0].id == task.id


async def test_success(executor, sample_task):
    handler = TestHandler()
    executor.register_handler("test_type", handler)

    await executor.submit(sample_task)
    await executor.wait_all()

    assert handler.called_once_with(sample_task)
    assert len(executor.errors) == 0


async def test_handlers_registration(executor, sample_task):
    default_handler = TestHandler()
    specific_handler = TestHandler()
    lishniy_handler = TestHandler()

    # Проверка протокола
    with pytest.raises(TypeError):
        executor.register_handler("type", "not_a_handler_object")

    # Проверка, когда у нас нет хендлеров
    await executor.submit(sample_task)
    await executor.wait_all()
    assert len(executor.errors) == 1
    assert "not registered" in str(executor.errors[0].cause)

    executor.register_default_handler(default_handler)

    executor.register_handler("other_type", lishniy_handler)

    await executor.submit(sample_task)
    await executor.wait_all()

    assert default_handler.called_once_with(sample_task)

    executor.register_handler(sample_task.task_type, specific_handler)
    await executor.submit(sample_task)
    await executor.wait_all()

    assert default_handler.called_once_with(sample_task)
    assert specific_handler.called_once_with(sample_task)


async def test_error_accumulation(executor, sample_task):
    broken_handler = TestHandler(should_fail=True)

    executor.register_handler(sample_task.task_type, broken_handler)

    for _ in range(10):
        await executor.submit(sample_task)
    await executor.wait_all()

    assert len(executor.errors) == 10
    assert all("Mock error" in str(e.cause) for e in executor.errors)


async def test_executor_not_started_error(sample_task):
    executor = AsyncTaskExecutor()

    with pytest.raises(ExecutorNotStartedError):
        await executor.submit(sample_task)


async def test_soft_shutdown(sample_task):
    """Закрытие контекстного менеджера до wait_all"""
    handler = TestHandler(delay=0.2)

    async with AsyncTaskExecutor(workers_count=1) as ex:
        ex.register_default_handler(handler)
        await ex.submit(sample_task)
        await ex.submit(sample_task)

    assert handler.call_count == 2
    assert all(t.status == TaskStatus.DONE for t in handler.processed_tasks)
