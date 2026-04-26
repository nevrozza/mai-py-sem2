import asyncio

from src.tasks.asyncio.async_task_executor import AsyncTaskExecutor
from src.tasks.asyncio.mock_handler import MockHandler
from src.tasks.sources.gen_num_source import GenNumberTaskSource


async def main() -> None:
    executor = AsyncTaskExecutor(workers_count=2)

    executor.register_default_handler(MockHandler())

    async with executor:

        # sync
        sync_source = GenNumberTaskSource(tasks_count=3)
        for task in sync_source.get_tasks():
            await executor.submit(task)



if __name__ == "__main__":
    asyncio.run(main())
