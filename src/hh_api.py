import requests
from typing import Dict, Any, List
from api_base import VacancyAPI


class HeadHunterAPI(VacancyAPI):
    """
    Класс для работы с API hh.ru.
    Реализует методы получения вакансий с платформы hh.ru.
    """

    def __init__(self):
        self._base_url = "https://api.hh.ru/vacancies"
        self._headers = {"User-Agent": "VacancyApp/1.0"}

    def _connect(self) -> None:
        """
        Приватный метод подключения к API hh.ru.
        Проверяет доступность API.
        """
        try:
            response = requests.get(self._base_url, headers=self._headers, timeout=5)
            if response.status_code != 200:
                raise ConnectionError(f"Не удалось подключиться к API: {response.status_code}")
        except requests.RequestException as e:
            raise ConnectionError(f"Ошибка подключения к API: {e}")

    def get_vacancies(self, query: str, per_page: int = 10) -> List[Dict[str, Any]]:
        """
        Получает вакансии с hh.ru по поисковому запросу.

        Args:
            query: поисковый запрос
            per_page: количество вакансий на страницу

        Returns:
            Список словарей с данными о вакансиях

        Raises:
            ConnectionError: если не удалось подключиться к API
        """
        self._connect()

        params = {
            "text": query,
            "per_page": per_page,
            "page": 0
        }

        try:
            response = requests.get(
                self._base_url,
                headers=self._headers,
                params=params,
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            return data.get("items", [])
        except requests.RequestException as e:
            raise ConnectionError(f"Ошибка при получении данных: {e}")
