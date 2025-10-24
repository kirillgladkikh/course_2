from abc import ABC, abstractmethod
from typing import Dict, Any


class VacancyAPI(ABC):
    """
    Абстрактный класс для работы с API сервисов вакансий.
    Определяет контракт для получения данных о вакансиях.
    """

    @abstractmethod
    def _connect(self) -> None:
        """
        Приватный метод подключения к API.
        Должен быть реализован в наследниках.
        """
        pass

    @abstractmethod
    def get_vacancies(self, query: str, per_page: int = 10) -> list[Dict[str, Any]]:
        """
        Получает вакансии по поисковому запросу.

        Args:
            query: поисковый запрос
            per_page: количество вакансий на страницу (по умолчанию 10)

        Returns:
            Список словарей с данными о вакансиях
        """
        pass
