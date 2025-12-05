import json
from abc import ABC, abstractmethod
from src.vacancy import Vacancy


class AbstractFile(ABC):
    """ """
    # Методы добавления, записи, удаления Вакансий
    @abstractmethod
    def get_vacancies(self):
        pass

    @abstractmethod
    def write_vacancies(self, vacancies: list[dict]):
        pass

    @abstractmethod
    def delete_vacancies(self):
        pass


class JSONSaver(AbstractFile):
    def __init__(self, path="data/vacancies.json"):
        """ """
        self._filename = path

    def get_vacancies(self) -> list[Vacancy]:
        """ """
        with open(self._filename, encoding="utf-8") as f:
            data = json.load(f)
        vacancies = []
        for vacancy in data:
            vacancies.append(Vacancy(**vacancy))
        return vacancies

    def write_vacancies(self, vacancies: list[dict]):
        """
        1) Получаем вакансии из файла
        2) Проходимся по списку vacancies
        3) Если среди вакансий, нет вакансии из файла, то добавляем её.
        """
        with open(self._filename, "w", encoding="utf-8") as f:
            json.dump(vacancies, f, indent=4, ensure_ascii=False)

    def delete_vacancies(self):
        open(self._filename, "w").close()