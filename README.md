# Python. Второй семестр

## Интересные штучки

**Лаба1**

- Используется `Protocol` для определения контракта [`TaskSource`](./src/tasks/protocols.py)
- [`Task`](./src/tasks/models/models.py) и [`TaskSource`](./src/tasks/protocols.py) типизированы (`payload: T`)
- [`APIMockTaskSource`](./src/tasks/sources/api_mock_source.py) использует внутри себя [
  `GenNumberTaskSource`](./src/tasks/sources/gen_num_source.py)
- Использование `yield` в источниках позволяет получать задачи по требованию, не загружая их все в память (кроме случая
  с [`FileJSONTaskSource`](./src/tasks/sources/file_source.py))
- Используется `time.sleep` для имитации задержки API в [`APIMockTaskSource`](./src/tasks/sources/api_mock_source.py)
- Для тестирования [`FileJSONTaskSource`](./src/tasks/sources/file_source.py) создаётся временный файл

**Лаба2**

- `Task` остаётся содержит дескрипторы и остаётся dataclass с поддержкой slots
- Примеры Data и Non Data дескипторов, работа с @property
- Для `created_at` и `id` использован [`ImmutableDescriptor`](./src/tasks/models/descriptors.py#L32)
- Красивый консольный вывод `Task` (через карточки)

**Лаба3**
- В [тестах](./tests/test_queue.py) для [`TaskQueue`](./src/tasks/task_queue.py) показано множество corner-cases, связанных с итерациями

> [!NOTE]
> С помощью данной лабораторной работы я смог освоить Test-Driven Development (TDD)

## Структура проекта

```
Курсач второй семестр гаддем
├── src
│   ├── tasks
│   │   ├── asyncio
│   │   │   ├── async_task_executor         # Асинхронный исполнитель задач – AsyncTaskExecutor
│   │   │   └── mock_handler                # Моковый асинхронный обработчик – MockAsyncHandler
│   │   │
│   │   ├── sources
│   │   │   ├── api_mock_source.py          # Источник задач, имитирующий API-запрос – APIMockTaskSource
│   │   │   ├── async_api_mock_source.py    # Асинхронный источник задач, имитирующий API-запрос – AsyncAPIMockTaskSource
│   │   │   ├── file_source.py              # Источник задач, читающий данные из JSON файла – FileJSONTaskSource
│   │   │   └── gen_num_source.py           # Источник задач, генерирующий случайные числа – GenNumberTaskSource
│   │   │
│   │   ├── models
│   │   │   ├── models.py	                # Generic Task dataclass
│   │   │   ├── descriptors.py              # Дескрипторы для Task
│   │   │   └── utils.py	                # Утилиты для работы с Task, валидации, энамчики
│   │   │
│   │   ├── dispatcher.py	                # Диспетчер для сбора и обработки задач – TasksDispatcher
│   │   ├── protocols.py	                # Протоколы: TaskSource, AsyncTaskSource, AsyncTaskHandler
│   │   └── exceptions.py	                # Кастомные ошибки
│   │
│   ├── main.py				                # Входная точка в программу (Асинхронщина: AsyncTaskExecutor)
│   ├── sync_main.py		                # Старая входная (до лаб4) точка в программу (old: TasksDispatcher)
│   └── consts.py			                # Константы: путь к файлу, используемый в FileJSONTaskSource
│
└── tests					                # Тесты для TasksDispatcher, AsyncTaskExecutor и реализаций TaskSource
```

## Quick start

0) Установить `uv` _0_o_
1) Клонировать этот репозиторий через git и активировать uv:

   ```
   git clone https://github.com/nevrozza/mai-py-sem2
   cd mai-py-sem2
   uv sync
   ```

2) Запустить программу через `uv`:
   `uv run -m src.main`

> [!IMPORTANT]
> Если запускать не из директории проекта, то необходимо отредактировать [`consts.py`](./src/consts.py), где указан путь
> к [`tasks.sample.json`](./tasks.sample.json)

3) Вы великолепны!
 
