import json
from src.tasks.models.models import Task
from src.tasks.sources.gen_num_source import GenNumberTaskSource
from src.tasks.sources.file_source import FileJSONTaskSource
from src.tasks.sources.api_mock_source import APIMockTaskSource


def test_gen_number_source():
    count = 42

    source = GenNumberTaskSource(tasks_count=count)
    tasks = list(source.get_tasks())

    assert len(tasks) == count
    assert isinstance(tasks[0], Task)


def test_api_mock_source():
    count = 2
    source = APIMockTaskSource(tasks_count=count)
    tasks = list(source.get_tasks())

    assert len(tasks) == count
    assert isinstance(tasks[0].payload, dict)


def test_file_json_source(tmp_path):
    # temp file =)
    data = [{"id": "1", "payload": "test_data"}]
    p = tmp_path / "test_tasks.json"
    p.write_text(json.dumps(data))

    source = FileJSONTaskSource(json_file_path=str(p))
    tasks = source.get_tasks()

    assert len(tasks) == 1
    assert tasks[0].payload == "test_data"
