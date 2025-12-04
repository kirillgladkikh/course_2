# Пример класса HHVacancies с необходимыми методами
class HHVacancies:
    def __init__(self):
        self.vacancies = []

    def get_vacancies(self, query):
        # Логика получения вакансий из источника
        pass

    def display_vacancies(self, vacancies=None):
        if vacancies is None:
            vacancies = self.vacancies
        for vacancy in vacancies:
            print(f"Название: {vacancy['title']}")
            print(f"Компания: {vacancy['company']}")
            print(f"Зарплата: {vacancy['salary']}")
            print(f"Опыт: {vacancy['experience']}\n")

    def sort_vacancies(self, key):
        self.vacancies.sort(key=lambda x: x[key.lower()])

    def filter_vacancies(self, **kwargs):
        # Логика фильтрации вакансий
        pass

    def add_vacancy(self, title, company, salary, experience):
        new_vacancy = {
            'title': title,
            'company': company,
            'salary': salary,
            'experience': experience
        }
        self.vacancies.append(new_vacancy)

    def remove_vacancy(self, title):
        self.vacancies = [vac for vac in self.vacancies if vac['title'] != title]
