import json

import pytest

from src.tasks.sources.gen_num_source import GenNumberTaskSource
from src.tasks.dispatcher import TasksDispatcher
from src.tasks.sources.file_source import FileJSONTaskSource


def get_random_dispatcher(tasks_count: int) -> TasksDispatcher:
    source = GenNumberTaskSource(tasks_count=tasks_count)
    dispatcher = TasksDispatcher()
    dispatcher.register_source(source)
    return dispatcher


def get_static_dispatcher(tmp_path) -> TasksDispatcher:
    data = [{"id": "1", "payload": "test_data2"}, {"id": "2", "payload": "test_data2"},
            {"id": "3", "payload": "test_data1"}]
    p = tmp_path / "test_tasks.json"
    p.write_text(json.dumps(data))
    source = FileJSONTaskSource(json_file_path=str(p))
    dispatcher = TasksDispatcher()
    dispatcher.register_source(source)
    return dispatcher


def test_taskqueue_for():
    init_count = 42
    dispatcher = get_random_dispatcher(init_count)

    real_count = 0

    for _ in dispatcher.tasks:
        real_count += 1

    assert real_count == init_count


def test_taskqueue_sum(tmp_path):
    dispatcher = get_static_dispatcher(tmp_path)

    assert sum(int(task.id.replace("file_", "")) for task in dispatcher.tasks) == 6


def test_taskqueue_list():
    init_count = 42
    dispatcher = get_random_dispatcher(init_count)
    lst = list(dispatcher.tasks)
    assert len(lst) == init_count


def test_taskqueue_many_tasks():
    init_count = 999_999
    dispatcher = get_random_dispatcher(init_count)
    real_count = 0

    for _ in dispatcher.tasks:
        real_count += 1

    assert real_count == init_count


# Здесь статичные данные (не изменяются – одинаковые всегда)
def test_taskqueue_static_retry(tmp_path):
    dispatcher = get_static_dispatcher(tmp_path)
    lst = list(dispatcher.tasks)

    for (index, task) in enumerate(dispatcher.tasks):
        assert lst[index].id == task.id
    for (index, task) in enumerate(dispatcher.tasks):
        assert lst[index].id == task.id


# Здесь динамические данных (при каждом обращении разные)
def test_taskqueue_dynamic_retry():
    dispatcher = get_random_dispatcher(1000)
    tasks = dispatcher.tasks
    lst = list(tasks)
    assert any(lst[index].id != task.id for (index, task) in
               enumerate(tasks))  # я не верю, что когда-то все 1000 элементов будут равны =))


def test_taskqueue_filters(tmp_path):
    payload = "test_data2"
    dispatcher = get_static_dispatcher(tmp_path)

    filter_data2 = lambda el: el.payload == payload

    filtered_tasks = dispatcher.tasks.filter(filter_data2)

    for task in filtered_tasks:
        assert task.payload == payload

    assert len(list(filtered_tasks)) == 2

def test_taskqueue_stop_iteration():
    dispatcher = get_random_dispatcher(10)

    it = iter(dispatcher.tasks)

    with pytest.raises(StopIteration):
        while True:
            next(it)





