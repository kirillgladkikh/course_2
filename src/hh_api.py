import requests
from abc import ABC, abstractmethod
# from src.utils import is_field_exist, is_field_dict


class AbstractAPI(ABC):
    @abstractmethod
    def _connect(self, keyword):
        pass

    @abstractmethod
    def get_vacancies(self, keyword):
        pass


class HHApi(AbstractAPI):
    def __init__(self):
        self.__url = "https://api.hh.ru/vacancies"
        self.__params = {"per_page": 20}

    def _connect(self, keyword):
        self.__params["text"] = keyword
        response = requests.get(self.__url, params=self.__params)
        # взять код через if из урока по api
        response.raise_for_status()
        return response.json()

    def get_vacancies(self, keyword):
        response = self._connect(keyword)
        print(f'\nresponse["items"]: {response["items"]}')
        return self.filter_vacancies(response["items"])

    @staticmethod
    def filter_vacancies(all_vacancies):
        vacancies = []
        for vacancy in all_vacancies:

            # 1. Проверяем наличие 'snippet' и 'responsibility'
            responsibility = None
            if (
                # is_field_exist(vacancy, "snippet") and
                vacancy.get("snippet") and
                # is_field_dict(vacancy, "snippet") and
                isinstance(vacancy["snippet"], dict) and
                "responsibility" in vacancy["snippet"]
            ):
                responsibility = vacancy["snippet"]["responsibility"]

            # 2. Проверка поля 'salary'
            salary_info = None

            # Сценарий 1: salary присутствует в вакансии
            if "salary" in vacancy:
                salary = vacancy["salary"]

                # Сценарий 2: salary — словарь (корректный формат)
                if isinstance(salary, dict):
                    salary_info = {
                        "from": salary.get("from"),
                        "to": salary.get("to"),
                        "currency": salary.get("currency")
                    }

            vacancies.append(
                {
                    "name": vacancy["name"],
                    "salary": salary_info,  #vacancy["salary"],
                    "description": responsibility or "Обязанности не указаны",
                    "url": vacancy.get("alternate_url", "Нет ссылки"),  # Проверяем наличие "alternate_url"

                }
            )
        return vacancies


hh = HHApi()
vacs = hh.get_vacancies("python")
print(vacs)
# print([vac["salary"] for vac in hh.filter_vacancies(vacs)])
