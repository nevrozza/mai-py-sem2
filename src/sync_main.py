from src.consts import JSON_FILE_PATH
from src.tasks.dispatcher import TasksDispatcher
from src.tasks.sources.api_mock_source import APIMockTaskSource
from src.tasks.sources.file_source import FileJSONTaskSource
from src.tasks.sources.gen_num_source import GenNumberTaskSource
from src.tasks.models.utils import print_task_card


def main() -> None:
    """
    Демонстрирует работу TasksDispatcher на моковых данных
    """
    dispatcher = TasksDispatcher()
    sources = [
        APIMockTaskSource(tasks_count=5),
        FileJSONTaskSource(json_file_path=JSON_FILE_PATH),
        GenNumberTaskSource(tasks_count=5)
    ]

    for source in sources:
        dispatcher.register_source(source)

    for task in dispatcher.tasks:
        print_task_card(task)


if __name__ == "__main__":
    main()
