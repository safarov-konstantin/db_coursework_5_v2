import time
import os
from utils.view import print_possible_options, print_result
from pathlib import Path
from utils.employers import Employers
from utils.works_json import get_ids_employers
from utils.db_manager import DBManager


PATH_FILE = os.path.join(Path(__file__).parent, 'data/ids_employers.json')
PATH_DB = os.path.join(Path(__file__).parent, 'database.ini')


def main():
    # Получить данные о работодателях и их вакансиях
    id_employers = get_ids_employers(PATH_FILE)
    employers = []
    for id_employer in id_employers:
        employers.append(Employers(id_employer))
        time.sleep(0.5)

    # код, который заполняет созданны в БД PostgreSQL
    # таблицы данными о работодателях и их вакансиях.
    db_manager = DBManager(PATH_DB)
    db_manager.create_database()
    db_manager.save_data_to_database(employers)

    # Пользовательский интефейс
    print_possible_options()
    while True:   
        user_input = input("Выберите действие: ")
        if user_input == "1":
            print_result(db_manager.get_companies_and_vacancies_count())
        elif user_input == "2":
            print_result(db_manager.get_all_vacancies())
        elif user_input == "3":
            print_result(db_manager.get_avg_salary())
        elif user_input == "4":
            print_result(db_manager.get_vacancies_with_higher_salary())
        elif user_input == "5":
            user_word = input("Введите слова для поиска: ")
            print_result(db_manager.get_vacancies_with_keyword(user_word))
        elif user_input == "q":
            break
        else:
            print("Я не занаю такой команды!")    


if __name__ == '__main__':
    main()
