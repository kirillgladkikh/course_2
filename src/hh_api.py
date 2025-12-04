from abc import ABC, abstractmethod
import requests

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
        response.raise_for_status()
        return response.json()

    @staticmethod
    def filter_vacancies(all_vacancies):
        vacancies = []
        for vacancy in all_vacancies:
            vacancies.append({
                "name": vacancy["name"],
                "salary": vacancy["salary"],
                "description": vacancy["snippet"]["responsibility"],
                "url": vacancy["alternate_url"]
            })
        return vacancies

# hh = HHApi()
# vacs = hh.get_vacancies("python")
# print([vac["salary"] for vac in hh.filter_vacancies(vacs)])