
import time
from src.tasks.asyncio.async_task_executor import AsyncTaskExecutor


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
    print(f"{'='*10} [{name}] Completed in {end_time - start_time:.2f} seconds {'='*10}")