import json

from src.tasks.models import Task

# TODO: добавить возможность парсить разные типы тасков (serializable?)

TASK_TAG = "file"


class FileJSONTaskSource:
    """
    Источник задач, читающий данные из JSON файла
    """

    def __init__(self, json_file_path: str):
        self.filename = json_file_path

    def get_tasks(self) -> list[Task[str]]:  # not iterable cuz we already open WHOLE file
        # TODO: errors catching
        with open(self.filename, 'r', encoding='utf-8') as f:
            data = json.load(f)  # loads whole file here

        tasks = []
        for item in data:
            tasks.append(Task(id=f"{TASK_TAG}_{item['id']}", payload=item['payload']))

        return tasks
