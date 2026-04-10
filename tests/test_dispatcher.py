import pytest

from src.tasks.dispatcher import TasksDispatcher


def test_dispatcher_register():
    dispatcher = TasksDispatcher()

    class TestSource:
        @staticmethod
        def get_tasks():
            ...

    source = TestSource()
    dispatcher.register_source(source)

    assert len(dispatcher._sources) == 1


def test_dispatcher_register_not_source():
    dispatcher = TasksDispatcher()
    with pytest.raises(TypeError):
        dispatcher.register_source("murmeow")
