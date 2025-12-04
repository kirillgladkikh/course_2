from abc import ABC, abstractmethod
from typing import List, Dict, Any


class FileSaver(ABC):
    """
    Абстрактный класс для сохранения и получения данных о вакансиях.
    Определяет контракт для работы с различными форматами файлов.
    """

    @abstractmethod
    def add_vacancy(self, vacancy: 'Vacancy') -> None:
        """
        Добавляет вакансию в файл.

        Args:
            vacancy: объект вакансии
        """
        pass

    @abstractmethod
    def get_vacancies(self) -> List['Vacancy']:
        """
        Получает все вакансии из файла.

        Returns:
            Список объектов вакансий
        """
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy: 'Vacancy') -> bool:
        """
        Удаляет вакансию из файла.

        Args:
            vacancy: объект вакансии для удаления

        Returns:
            True, если вакансия была удалена, False иначе
        """
        pass
