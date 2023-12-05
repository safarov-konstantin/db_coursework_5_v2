from utils.head_hunter_api import HeadHunterAPI


class Vacancy:
    """
    Класс для хранения данных об вакансиях
    """

    def __init__(self, id, name, url, salary, experience):
        self.id = id
        self.name = name
        self.url = url
        self.salary = salary
        self.experience = experience

    def __repr__(self):
        return f'Vacancy(id: {self.id}, name: {self.name}, url: {self.url}, salary: {self.salary}, experience: {self.experience})'

    def __str__(self):
        description_vacancy = f'{self.name} \ Зарплата: {self.salary} \ Опыт: {self.experience} \ url: {self.url}'
        return description_vacancy

    @classmethod
    def get_vacancy_hh_api(cls, hh_vacancies):
        """
        Возвращает экземпляры класса Vacancy по данным 
        из структуры вакансий с сервиса hh.ru
        """
        vacancies = []
        for hh_vacancy in hh_vacancies:
            id = hh_vacancy['id']
            name = hh_vacancy['name']
            url = hh_vacancy['alternate_url']
            salary = HeadHunterAPI.get_solary_representation(hh_vacancy['salary'])
            experience = hh_vacancy['experience']['name']
            vacancies.append(cls(id, name, url, salary, experience))
        return vacancies
