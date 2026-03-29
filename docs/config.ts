//https://github.com/sennett-lau/readme-project-structure-generator.git
export const projectStructure = {
  src: {
            tasks: {
                sources: {
                    "api_mock_source.py": "Источник задач, имитирующий API-запрос – `APIMockTaskSource`",
                    "file_source.py": "Источник задач, читающий данные из JSON файла – `FileJSONTaskSource`",
                    "gen_num_source.py": "Источник задач, генерирующий случайные числа – `GenNumberTaskSource`"
                },
                models: {
                    "models.py": "Generic `Task` dataclass",
                    "descriptors.py": "Дескрипторы для `Task`",
                    "utils.py": "Утилиты для работы с `Task`, валидации, энамчики",
                },
                "dispatcher.py": "Диспетчер для сбора и обработки задач – `TasksDispatcher`",
                "protocols.py": "Протокол `TaskSource`",
                "exceptions.py": "Кастомные ошибки"
            },
            'main.py': 'Входная точка в программу',
            'consts.py': 'Константы: путь к файлу, используемый в `FileJSONTaskSource`'
        },
        'tests': 'Тесты для `TasksDispatcher` и реализаций `TaskSource`'
}