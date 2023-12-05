from configparser import ConfigParser
import psycopg2


class DBManager:
    """
    Класс для работы с postgresql
    """
    def __init__(self, path_database):
        self.params_db = self.__get_params_db(path_database)
        self.database_name = 'hh_api'

    def __get_params_db(self, path_database):
        """
        Получение параметров для подключение к ИБ
        """
        section = 'postgresql'
        # create a parser
        parser = ConfigParser()
        # read config file
        parser.read(path_database)
        db = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                db[param[0]] = param[1]
        else:
            raise Exception(
                'Section {0} is not found in the {1} file.'.format(section, path_database))
        return db

    def create_database(self):
        """
        Создание базы данных и таблиц для сохранения данных о компниях и вакансиях.
        """
        params = self.params_db
        conn = psycopg2.connect(dbname='postgres', **params)
        conn.autocommit = True
        cur = conn.cursor()

        try:
            cur.execute(f"DROP DATABASE {self.database_name }")
        except:
           pass

        cur.execute(f"CREATE DATABASE {self.database_name }")

        conn.close()

        conn = psycopg2.connect(dbname=self.database_name , **params)

        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE employers (
                    employers_id SERIAL PRIMARY KEY,
                    id_hh VARCHAR(255),
                    name VARCHAR NOT NULL,
                    url TEXT
                )
            """)

        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE vacancy (
                    vacancy_id SERIAL PRIMARY KEY,
                    employers_id INT REFERENCES employers(employers_id),
                    id_hh VARCHAR(255),
                    name VARCHAR NOT NULL,
                    url TEXT,
                    salary REAL,
                    experience TEXT
                )
            """)

        conn.commit()
        conn.close()

    def save_data_to_database(self, data):
        """
        Сохранение данных о каналах и видео в базу данных.
        """

        conn = psycopg2.connect(dbname=self.database_name, **self.params_db)

        with conn.cursor() as cur:
            for employer in data:
                cur.execute(
                    """
                    INSERT INTO employers (id_hh, name, url)
                    VALUES (%s, %s, %s)
                    RETURNING employers_id
                    """,
                    (employer.id, employer.name, employer.url,)
                )
                vacancies_data = employer.vacancies
                employers_id = cur.fetchone()[0]
                for vacancy in vacancies_data:
                    cur.execute(
                        """
                        INSERT INTO vacancy (employers_id, id_hh, name, url, salary, experience)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        """,
                        (employers_id, vacancy.id, vacancy.name, vacancy.url, vacancy.salary, vacancy.experience)
                    )

        conn.commit()
        conn.close()

    def get_companies_and_vacancies_count(self):
        """
        Получает список всех компаний и количество вакансий у каждой компании
        """
        conn = psycopg2.connect(dbname=self.database_name, **self.params_db)

        with conn.cursor() as cur:
            cur.execute(
                    """
                    SELECT employers.name, COUNT(employers.name)  
                    FROM vacancy
                    LEFT JOIN employers  USING(employers_id)
                    GROUP BY employers.name;
                    """
            )

            result = cur.fetchall()
        conn.close()
        return result

    def get_all_vacancies(self):
        """
        Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию.
        """
        conn = psycopg2.connect(dbname=self.database_name, **self.params_db)
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT 
                    employers.name as employers_name, 
                    vacancy.name as vacancy_name,
                    salary as salary, 
                    vacancy.url as vacancy_url
                FROM vacancy
                LEFT JOIN employers  USING(employers_id);
                """
            )

            result = cur.fetchall()
        conn.close()
        return result

    def get_avg_salary(self):
        """
        Получает среднюю зарплату по вакансиям
        """
        conn = psycopg2.connect(dbname=self.database_name, **self.params_db)
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT AVG(salary) 
                FROM vacancy;
                """
            )

            result = cur.fetchall()
        conn.close()
        return result

    def get_vacancies_with_higher_salary(self):
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям
        """
        conn = psycopg2.connect(dbname=self.database_name, **self.params_db)
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT * FROM vacancy
                WHERE salary > (SELECT AVG(salary) FROM vacancy);
                """
            )

            result = cur.fetchall()
        conn.close()
        return result

    def get_vacancies_with_keyword(self, word):
        """
        Получает список всех вакансий, в названии которых содержатся
        переданные в метод слова, например python
        """
        conn = psycopg2.connect(dbname=self.database_name, **self.params_db)
        with conn.cursor() as cur:

            text_query = ("SELECT * FROM vacancy\n"
                          + f"WHERE vacancy.name ILIKE '%{word}%'")
            cur.execute(text_query)
            result = cur.fetchall()
        conn.close()
        return result
