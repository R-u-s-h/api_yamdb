# api_yamdb
api_yamdb

## Наполнение базы данных
Реализована возможность наполнения базы данных из .csv файлов.

### Формат файлов
Первая строка файла — имена полей модели.

Остальные строки — значения полей.

Разделитель — `,` (запятая).

#### Пример файла:
`static/data/category.csv`
```csv
id,name,slug
1,Фильм,movie
2,Книга,book
3,Музыка,music
```

### Инструмент импорта данных
Импорт данных реализован с помощью пользовательской команды `import_csv`
скрипта `manage.py`

#### Синтаксис
```
python manage.py import_csv <csv_file> <model_name>

где:
  csv_file              имя .csv файла
  model_name            название модели в которую необходимо импортировать

для увеличения уровня информативности можно использовать опцию:
  -v2 (--verbosity 2)
```

#### Пример исползования
```shell
(venv) api_yamdb$ python manage.py import_csv static/data/category.csv Category -v2
Importing module <module 'reviews.models' from '/Users/ivr/Git/yandex_practicum/api_yamdb/api_yamdb/reviews/models.py'>
Using model <class 'reviews.models.Category'>
Created instance <Category: movie>
Updated instance <Category: book>
Updated instance <Category: music>
(venv) api_yamdb$
```