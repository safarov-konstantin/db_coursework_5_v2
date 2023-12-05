def print_possible_options():
    """
    Вывыдит возможные действия в программе
    """
    print("Возможные действия: ")
    print("1 - Получить список всех компаний и количество вакансий у каждой компании")
    print("2 - Получить список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.")
    print("3 - Получить среднюю зарплату по вакансиям")
    print("4 - Получить список всех вакансий, у которых зарплата выше средней по всем вакансиям")
    print("5 - Получает список всех вакансий, в названии которых содержатся переданные в метод слова")
    print("q - выход")


def print_result(result):
    """
    Выводит результат в консоль
    """
    if isinstance(result, list):
        for i in result:
            if isinstance(i, list):
                print_result(i)
            elif isinstance(i, tuple):
                str_result = ""
                for value in i:
                    str_result += f"{value} " 
                print(f'  {str_result}')        
    elif isinstance(result, tuple):
        str_result = ""
        for value in i:
            str_result += f"{value} " 
            print(f'  {str_result}\n') 