import json
import os
from typing import List
from file_base import FileSaver
from vacancy import Vacancy


class JSONSaver(FileSaver):
    """
    Класс для сохранения вакансий в JSON-файл.
    Реализует методы работы с JSON-файлом.
    """

    def __init__(self, filename: str = "vacancies.json"):
        """
        Инициализация савера с указанием имени файла.

        :param filename: имя JSON-файла для сохранения данных
        """
        self.filename = filename

    def save(self, vacancies: List[Vacancy]) -> None:
        """
        Сохраняет список вакансий в JSON-файл.

        :param vacancies: список объектов Vacancy для сохранения
        """
        # Преобразуем объекты Vacancy в словари для JSON
        data = [vacancy.to_dict() for vacancy in vacancies]

        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def load(self) -> List[Vacancy]:
        """
        Загружает список вакансий из JSON-файла.

        :return: список объектов Vacancy
        :raises FileNotFoundError: если файл не найден
        :raises json.JSONDecodeError: если файл содержит некорректный JSON
        """
        if not os.path.exists(self.filename):
            raise FileNotFoundError(f"Файл {self.filename} не найден.")

        with open(self.filename, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Преобразуем словари обратно в объекты Vacancy
        return [Vacancy.from_dict(item) for item in data]

    def add(self, vacancy: Vacancy) -> None:
        """
        Добавляет одну вакансию в JSON-файл.

        :param vacancy: объект Vacancy для добавления
        """
        try:
            # Загружаем существующие вакансии
            vacancies = self.load()
        except (FileNotFoundError, json.JSONDecodeError):
            # Если файла нет или он пуст/некорректен — начинаем с пустого списка
            vacancies = []

        # Добавляем новую вакансию
        vacancies.append(vacancy)

        # Сохраняем обновлённый список
        self.save(vacancies)

    def clear(self) -> None:
        """
        Очищает файл (удаляет все данные).
        """
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump([], file, ensure_ascii=False, indent=4)
