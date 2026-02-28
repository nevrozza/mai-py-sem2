import pytest

from src.tasks.dispatcher import TasksDispatcher
from src.tasks.models import Task


def test_dispatcher_register_and_flow():
    dispatcher = TasksDispatcher()

    test_id = "test"
    payload = 100
    count = 5

    class TestSource:
        def get_tasks(self):
            for i in range(count):
                yield Task(id=test_id, payload=payload)

    source = TestSource()
    dispatcher.register_source(source)

    tasks = list(dispatcher.run_tasks_flow())
    assert len(tasks) == count
    assert tasks[0].id == test_id
    assert tasks[0].payload == payload


def test_dispatcher_register_not_source():
    dispatcher = TasksDispatcher()
    with pytest.raises(TypeError):
        dispatcher.register_source("murmeow")
