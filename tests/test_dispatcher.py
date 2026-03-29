import pytest

from src.tasks.dispatcher import TasksDispatcher
from src.tasks.models.models import Task


def test_dispatcher_register_and_flow():
    dispatcher = TasksDispatcher()

    test_id = "test"
    payload = 100
    count = 5

    class TestSource:
        @staticmethod
        def get_tasks():
            for i in range(count):
                yield Task(id_=test_id, payload=payload, description_="test_description", priority_=10)

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
