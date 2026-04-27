# Python. Второй семестр

Проект имитирует работу сервиса, который собирает задачи из различных источников
(API, файлы, etc.) и обрабатывает их, соблюдая протоколы
и принципы отказоустойчивости.


## Как всё работает
В проекте продемонстрирована "эволюция" сервиса.
Сначала (лабы 1-3) был просто синхронный распределитель задач [(`TasksDispatcher`)](./src/tasks/dispatcher.py):

- **Пайплайн:**
  - [`TaskSource`](./src/tasks/sources/api_mock_source.py) генерирует задачи
  - [`TaskQueue`](./src/tasks/task_queue.py) оборачивает поток задач (решает проблемы с повторным итерированием и добавляет ленивую фильтрацию)
  - [`TasksDispatcher`](./src/tasks/dispatcher.py): 
    ```
    for task in dispatcher.tasks:
      do_smth(task)
    ```
    - последовательно обходит задачи
    - обработка происходит **строго по одной задаче**
    - блокирующие операции (например time.sleep) останавливают весь поток
    

- **Повторная итерируемость:** Обычный генератор в Python можно обойти только один раз. 
  В [`TaskQueue`](./src/tasks/task_queue.py) эта проблема решена через фабрику итераторов (`iter_factory`) – при каждом новом обходе таски получаются заново (чтобы `заморозить` это, можно использовать `persisted`).

- **Lazy:** Благодаря `yield from` в источниках и `iter_factory` в [`TaskQueue`](./src/tasks/task_queue.py), задачи не загружаются в память все сразу. 
Они "текут" из источника только в момент итерации. Метод `filter` создает новую ленивую обертку, не запуская вычисления.  

---
После (лаба 4) был совершён переход к полноценному пулу асинхронных воркеров [(`AsyncTaskExecutor`)](./src/tasks/asyncio/async_task_executor.py),
способному конкурентно обрабатывать данные без блокировки основного потока:

- **Как это работает:**
  ```
  TaskSource -> submit(task) -> asyncio.Queue -> workers -> handler.handle(task)
  ```
  - задачи складываются в `asyncio.Queue`
  - запускается пул воркеров (`workers_count`)
  - в каждом воркере:
    ```
    while True:
      task = await queue.get()
      await handler.handle(task)
    ```
    

- **Управление воркерами:** Количество воркеров настраивается при инициализации. 
Каждый воркер работает в собственном цикле `_worker_loop`, ожидая новые задачи из `asyncio.Queue`.

- **Безопасный жизненный цикл:**
  - _Контекстный менеджер:_ Вся инициализация очереди и запуск воркеров происходит в __aenter__.

  - _Sentinels:_ В очередь отправляется None для остановки системы. Это гарантирует, что программа не "зависнет" при выходе из контекста.

- **Агрегация ошибок:** `Executor` не падает при ошибке в конкретной задаче. Все исключения упаковываются в `TaskProcessingError` и сохраняются в `_errors`.


## Что я познал
- Test-Driven Development
- Протоколы
- Дескрипторы + понял, как именно работает property
- Работа с lazy операциями и генераторами в Python
- Написание контекстных менеджеров
- Работа с асинхронщиной в Python

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
- `Task` содержит дескрипторы и остаётся dataclass с поддержкой slots
- Примеры Data и Non Data дескипторов, работа с @property
- Для `created_at` и `id` использован [`ImmutableDescriptor`](./src/tasks/models/descriptors.py#L34)
- Красивый консольный вывод `Task` (через карточки)

**Лаба3**
- В [тестах](./tests/test_queue.py) для [`TaskQueue`](./src/tasks/task_queue.py) показано множество corner-cases,
  связанных с итерациями

**Лаба4**
- Протокол [`AsyncTaskSource`](./src/tasks/protocols.py)
  и его реализация [(`AsyncAPIMockTaskSource`)](./src/tasks/sources/async_api_mock_source.py) c `asyncio.sleep` вместо
  `time.sleep`
- Простенькие бенчмарки в [`main.py`](./src/main.py): продемонстрирована разница между блокирующим и неблокирующим
  ожиданием
- Поддержка разных Handler'ов для разных типов задач +возможность указать fallback

## Структура проекта
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
> Можно запустить синхронную версию: `uv run -m src.sync_main`, но важно учесть:\
> Если запускать не из директории проекта, то необходимо отредактировать [`consts.py`](./src/consts.py), где указан путь
> к [`tasks.sample.json`](./tasks.sample.json)

3) Вы великолепны!
 
