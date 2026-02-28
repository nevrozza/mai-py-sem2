from src.consts import JSON_FILE_PATH
from src.tasks.dispatcher import TasksDispatcher
from src.tasks.sources.api_mock_source import APIMockTaskSource
from src.tasks.sources.file_source import FileJSONTaskSource
from src.tasks.sources.gen_num_source import GenNumberTaskSource


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

    dispatcher.collect(
        lambda task: print(f"Processing Task | ID={task.id} | PayloadType={type(task.payload).__name__} | {task.payload}")
    )


if __name__ == "__main__":
    main()
