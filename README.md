# Курсовая 5 по БД

Получает данные о работодателях и их вакансиях с сайта hh.ru. Для этого используйте публичный API hh.ru и библиотеку 
requests

В файле data/ids_employers.json прописаны 10 интересных  компаний, от которых  будут получать данные о вакансиях по API.

Реализует код, который заполняет созданные в БД PostgreSQL таблицы данными о работодателях и их вакансиях.

И выводит следующие данные в консоль:

— список всех компаний и количество вакансий у каждой компании.

— список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.

— среднюю зарплату по вакансиям.

— список всех вакансий, у которых зарплата выше средней по всем вакансиям.

— список всех вакансий, в названии которых содержатся переданные в метод слова, например python.

# ПРИМЕЧАНИЕ 

 для корекнтной работы нужен файл с настройками подключекния базе данных под именем database.ini

 Содержание файла database.ini: 
 
```
[postgresql]
host=localhost
user=user_db
password=pass_user_db
port=5432
```

