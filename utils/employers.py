from utils.head_hunter_api import HeadHunterAPI
from utils.vacancy import Vacancy


class Employers:
    """
    Класс для хранения данных работодателей
    """
    hh_api = HeadHunterAPI()

    def __init__(self, id_employer):
        data_hh = self.hh_api.get_employer(id_employer)
        if data_hh is None:
            raise Exception(f"По id {id_employer} не найден работодатель!")
        self.id = data_hh['id']
        self.name = data_hh['name']
        self.url = data_hh['alternate_url']
        self.vacancies = self.get_vacancy_employer()

    def __repr__(self):
        return f'Vacancy(id: {self.id}, name: {self.name}, url: {self.url}, vacancies: {self.vacancies})'

    def __str__(self):
        description_employers = f'{self.name} \  url: {self.url}'
        return description_employers

    def get_vacancy_employer(self):
        """
        Получает 50 вакансий по работодателю
        """
        params = {
            'employer_id': self.id,
            'per_page': 50,
            'page': 0,
            'only_with_salary': True
        }
        vacancies_employer = Vacancy.get_vacancy_hh_api(self.hh_api.get_vacancies(params))
        return vacancies_employer
