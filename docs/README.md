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