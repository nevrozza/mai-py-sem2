import asyncio
import sys

from src.tasks.asyncio.async_task_executor import AsyncTaskExecutor
from src.tasks.asyncio.mock_handler import MockHandler
from src.tasks.sources.gen_num_source import GenNumberTaskSource
from src.tasks.sources.async_api_mock_source import AsyncAPIMockTaskSource
from src.tasks.sources.api_mock_source import APIMockTaskSource
from src.utils import run_test_case

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

        executor.register_default_handler(MockHandler())
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


if __name__ == "__main__":
    asyncio.run(main())
