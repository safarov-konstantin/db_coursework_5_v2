import requests
import json


class HeadHunterAPI:
    """
    Класс для работы с API HeadHunter
    """
    url_vacancies = 'https://api.hh.ru/vacancies'
    url_employers = 'https://api.hh.ru/employers'

    def get_vacancies(self, params):
        """
        Получает данные по вакансиям с hh.ru по параметрам (params)
        """
        # Посылаем запрос к API
        req = requests.get(HeadHunterAPI.url_vacancies, params)  
        
        # если статус не 200 возвращем пустой список
        if not req.status_code == 200:
            req.close()
            return []

         # Декодируем его ответ, чтобы Кириллица отображалась корректно
        data = req.content.decode() 
        req.close()
        data = json.loads(data)

        return data['items']

    def get_employer(self, employer_id):
        """
        Получет данные по работодателю с hh.ru
        """
        url = f"{HeadHunterAPI.url_employers}/{employer_id}"
         # Посылаем запрос к API
        req = requests.get(url) 

        # если статус не 200 возвращем None
        if not req.status_code == 200:
            req.close()
            return None

        # Декодируем его ответ, чтобы Кириллица отображалась корректно
        data = req.content.decode()  
        req.close()
        data = json.loads(data)

        return data

    @staticmethod
    def get_solary_representation(salary_hh):
        """
        Преобразует структуру из сервиса hh.ru в число
        беря только начальную зарплату из структуры
        """
        if salary_hh is None:
            return 0
        salary_from = salary_hh['from']
        if salary_from is not None:
            return salary_from
        else:
            return 0

