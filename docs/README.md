```
Курсач второй семестр гаддем
├── src
│   ├── tasks
│   │   ├── asyncio
│   │   │   ├── async_task_executor.py      # Асинхронный исполнитель задач – AsyncTaskExecutor
│   │   │   └── mock_handler.py             # Моковый асинхронный обработчик – MockAsyncHandler
│   │   │
│   │   ├── sources
│   │   │   ├── api_mock_source.py          # Источник задач, имитирующий API-запрос – APIMockTaskSource
│   │   │   ├── async_api_mock_source.py    # Асинхронный источник задач, имитирующий API-запрос – AsyncAPIMockTaskSource
│   │   │   ├── file_source.py              # Источник задач, читающий данные из JSON файла – FileJSONTaskSource
│   │   │   └── gen_num_source.py           # Источник задач, генерирующий случайные числа – GenNumberTaskSource
│   │   │
│   │   ├── models
│   │   │   ├── models.py                   # Generic Task dataclass
│   │   │   ├── descriptors.py              # Дескрипторы для Task
│   │   │   └── utils.py                    # Утилиты для работы с Task, валидации, энамчики
│   │   │
│   │   ├── dispatcher.py                   # Диспетчер для сбора и обработки задач – TasksDispatcher
│   │   ├── protocols.py                    # Протоколы: TaskSource, AsyncTaskSource, AsyncTaskHandler
│   │   └── exceptions.py                   # Кастомные ошибки
│   │
│   ├── main.py                             # Входная точка в программу (Асинхронщина: AsyncTaskExecutor)
│   ├── sync_main.py                        # Старая входная (до лаб4) точка в программу (old: TasksDispatcher)
│   └── consts.py                           # Константы: путь к файлу, используемый в FileJSONTaskSource
│
└── tests                                   # Тесты для TasksDispatcher, AsyncTaskExecutor и реализаций TaskSource
```