import asyncio
import sys
import time

from src.tasks.asyncio.async_task_executor import AsyncTaskExecutor
from src.tasks.asyncio.mock_handler import MockAsyncHandler
from src.tasks.sources.gen_num_source import GenNumberTaskSource
from src.tasks.sources.async_api_mock_source import AsyncAPIMockTaskSource
from src.tasks.sources.api_mock_source import APIMockTaskSource

import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
    datefmt='%H:%M:%S',
    stream=sys.stdout
)


async def main() -> None:
    executor = AsyncTaskExecutor(workers_count=2)

    async with executor:
        await run_test_case("ERRORED SYNC", executor,
                            GenNumberTaskSource(tasks_count=3).get_tasks())

        executor.register_default_handler(MockAsyncHandler())
        await run_test_case("SYNC (Default Handler)", executor,
                            GenNumberTaskSource(tasks_count=3).get_tasks())

        sync_api_source = APIMockTaskSource(tasks_count=3)
        await run_test_case("BLOCKING (time.sleep)", executor,
                            sync_api_source.get_tasks())

        async_source = AsyncAPIMockTaskSource(tasks_count=3)
        await run_test_case("NON-BLOCKING (asyncio.sleep)", executor,
                            async_source.get_tasks_async())

    print(f"\nFINAL REPORT: Processed with {len(executor.errors)} errors")
    for err in executor.errors:
        print(f"| {err}")


async def run_test_case(name: str, executor: AsyncTaskExecutor, source_iter):
    print("\n", '-' * 20, name, '-' * 20)
    start_time = time.perf_counter()

    if hasattr(source_iter, '__aiter__'):
        async for task in source_iter:
            await executor.submit(task)
    else:
        for task in source_iter:
            await executor.submit(task)

    await executor.wait_all()
    end_time = time.perf_counter()
    print(f"{'=' * 10} [{name}] Completed in {end_time - start_time:.2f} seconds {'=' * 10}")


if __name__ == "__main__":
    asyncio.run(main())
