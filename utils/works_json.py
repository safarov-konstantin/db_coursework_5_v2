import json


def get_ids_employers(path):
    """
    Получение id работодателей из файла по пути path 
    """
    try:
        with open(path, 'r', encoding='utf8') as file:
            ids_employers = json.loads(file.read())
        return ids_employers['employer_id']
    except:
        return []
