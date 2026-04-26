import asyncio
import logging

from src.tasks.models.models import Task
from src.tasks.protocols import TaskHandler
from src.tasks.exceptions import TaskProcessingError, ExecutorNotStartedError, ExecutorError
from src.tasks.models.utils import cut_id

logger = logging.getLogger("AsyncTaskExecutor")


class AsyncTaskExecutor:
    """
        Асинхронный исполнитель задач с пулом воркеров.
        Используется как контекстный менеджер для безопасного запуска и остановки.
    """

    def __init__(self, workers_count: int = 2):
        self._queue: asyncio.Queue[Task | None] | None = None
        self._workers_count = workers_count
        self._workers_tasks: list[asyncio.Task] = []
        self._running = False
        self._handlers: dict[str, TaskHandler] = {}
        self._default_handler: TaskHandler | None = None
        self._errors: list[TaskProcessingError] = []

    def register_handler(self, task_type: str, handler: TaskHandler) -> None:
        """
        Регистрирует обработчик для конкретного типа задач (по task_type)

        :raises TypeError: Если handler не реализует TaskHandler.

        """

        if not isinstance(handler, TaskHandler):
            raise TypeError(f"Handler {handler!r} must implement TaskHandler protocol")

        self._handlers[task_type] = handler
        logger.info(f"Registered handler for {task_type}")

    def register_default_handler(self, handler: TaskHandler) -> None:
        """
        Регистрирует fallback обработчик для задач
        :raises TypeError: Если handler не реализует TaskHandler.
        """

        if not isinstance(handler, TaskHandler):
            raise TypeError(f"Handler {handler!r} must implement TaskHandler protocol")

        self._default_handler = handler
        logger.debug(f"Registered default handler")

    async def submit(self, task: Task) -> None:
        """Поставить задачу в очередь

        :raises ExecutorNotStartedError: Если исполнитель не запущен.
        """
        if not self._running or self._queue is None:
            raise ExecutorNotStartedError("Executor not started. Use 'asyncio with'")
        await self._queue.put(task)
        logger.info(f"Task {cut_id(task.id)} was submitted")

    async def _process_task(self, task: Task, worker_id: str) -> None:
        """Выбор обработчика и выполнение задачи с перехватом ошибок"""
        task_key = task.task_type
        handler = self._handlers.get(task_key, self._default_handler)

        try:
            if not handler:
                raise ExecutorError(f"Handler for '{task_key}' or fallback is not registered")

            logger.info(f"[{worker_id}] Starting task {cut_id(task.id)}")
            await handler.handle(task)
            logger.info(f"[{worker_id}] Finished task {cut_id(task.id)} (Status: {task.status.value})")
        except Exception as e:
            error = TaskProcessingError(task, e)
            self._errors.append(error)
            logger.error(f"[{worker_id}] Failed task {cut_id(task.id)}: {e}")

    async def _worker_loop(self, worker_id: str) -> None:
        """Цикл worker'а: берёт задачи из очереди и обрабатывает"""

        while True:
            task = await self._queue.get()
            if task is None:  # sentinel — выходим
                self._queue.task_done()
                break
            await self._process_task(task, worker_id)
            self._queue.task_done()

    async def wait_all(self) -> None:
        """Дожидается выполнения всех задач, которые сейчас есть в очереди"""
        if self._queue:
            await self._queue.join()

    @property
    def errors(self) -> list[TaskProcessingError]:
        """Ошибки, возникшие при обработке задач"""
        return list(self._errors)

    async def __aenter__(self) -> AsyncTaskExecutor:
        logger.info(f"Starting executor with {self._workers_count} workers")
        self._queue = asyncio.Queue()
        self._running = True
        self._workers_tasks = [
            asyncio.create_task(self._worker_loop(f"worker-{i}"))
            for i in range(self._workers_count)
        ]
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> bool:
        logger.info("Stopping executor and cleaning up workers...")

        # Отправляем sentinel для каждого worker'а
        for _ in self._workers_tasks:
            await self._queue.put(None)

        # Ждём завершения всех workers
        await asyncio.gather(*self._workers_tasks, return_exceptions=True)
        self._running = False

        logger.info("Executor stopped.")
        return False
