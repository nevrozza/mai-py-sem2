# Python. Второй семестр

## Интересные штучки
  - Используется `Protocol` для определения контракта [`TaskSource`](./src/tasks/protocols.py)
  - [`Task`](./src/tasks/models/models.py) и [`TaskSource`](./src/tasks/protocols.py) типизированы (`payload: T`)
  - [`APIMockTaskSource`](./src/tasks/sources/api_mock_source.py) использует внутри себя [`GenNumberTaskSource`](./src/tasks/sources/gen_num_source.py)
  - Использование `yield` в источниках позволяет получать задачи по требованию, не загружая их все в память (кроме случая с [`FileJSONTaskSource`](./src/tasks/sources/file_source.py))
  - Используется `time.sleep` для имитации задержки API в [`APIMockTaskSource`](./src/tasks/sources/api_mock_source.py)
  - Для тестирования [`FileJSONTaskSource`](./src/tasks/sources/file_source.py) создаётся временный файл
  
## Структура проекта
```
Курсач второй семестр гаддем
├── src
│   ├── tasks
│   │   ├── sources
│   │   │   ├── api_mock_source.py	# Источник задач, имитирующий API-запрос – `APIMockTaskSource`
│   │   │   ├── file_source.py		# Источник задач, читающий данные из JSON файла – `FileJSONTaskSource`
│   │   │   └── gen_num_source.py	# Источник задач, генерирующий случайные числа – `GenNumberTaskSource`
│   │   ├── dispatcher.py			# Диспетчер для сбора и обработки задач – `TasksDispatcher`
│   │   ├── models.py				# Generic `Task` dataclass
│   │   └── protocols.py			# Протокол `TaskSource`
│   ├── main.py						# Входная точка в программу
│   └── consts.py					# Константы: путь к файлу, используемый в `FileJSONTaskSource`
└── tests							# Тесты для `TasksDispatcher` и реализаций `TaskSource`
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
> Если запускать не из директории проекта, то необходимо отредактировать [`consts.py`](./src/consts.py), где указан путь к [`tasks.sample.json`](./tasks.sample.json)
 3) Вы великолепны!
 
