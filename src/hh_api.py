# === Взаимодействие с API ===
#
# Создан абстрактный класс для работы с API.
# Реализован метод подключения к API в абстрактном классе.
# Реализован метод получения вакансий отдельно в абстрактном классе.
# Используется декоратор @abstract_method для методов абстрактного класса.
# Абстрактные методы не имеют реализации.
#
# Создан класс для работы с hh.ru.
# Класс для работы с hh.ru наследуется от абстрактного.
# Реализованы все методы абстрактного класса.
# Атрибуты экземпляра класса — приватные.
# Метод подключения к API hh.ru — приватный.
# В методе подключения к API отправляется запрос на базовый URL.
# В методе подключения к API происходит проверка статус-кода ответа.
# Метод подключения к API hh.ru вызывается в методе получения данных перед отправкой запроса.
# Метод получения данных принимает параметр — ключевое слово для поиска вакансий.
# Метод получения данных формирует параметры для запроса как минимум из text, per_page.
# Метод получения данных отправляет запрос на API hh.ru для получения данных о вакансиях по ключевому слову.
# Метод получения данных собирает данные ответа в формате списка словарей из ключа item.

# +++
# Создать абстрактный класс для работы с API сервиса с вакансиями.
# Реализовать класс, наследующийся от абстрактного класса, для работы с платформой hh.ru.
# Класс должен уметь подключаться к API и получать вакансии.


# Вариант ИИ
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
