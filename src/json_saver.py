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
        """
        Возвращает список объектов Vacancy из JSON‑файла.
        Если файл не существует или пуст — возвращает пустой список.
        """
        try:
            with open(self._filename, encoding="utf-8") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []  # Возвращаем пустой список при отсутствии файла или ошибке парсинга

        vacancies = []
        for vacancy in data:
            vacancies.append(Vacancy(**vacancy))
        return vacancies

    def filter_new_vacancies(self, new_vacancies: list[dict], existing_urls: set[str]) -> list[dict]:
        """
        Фильтрует новые вакансии по следующим критериям:
        - наличие поля "url";
        - значение "url" не пустое и не равно "Нет ссылки";
        - "url" отсутствует в наборе existing_urls.

        Args:
            new_vacancies: список новых вакансий (словарей).
            existing_urls: набор URL уже существующих вакансий для проверки уникальности.

        Returns:
            Список отфильтрованных вакансий, удовлетворяющих всем критериям.
        """
        filtered_vacancies = []

        for vacancy in new_vacancies:
            # Проверяем наличие поля "url"
            if "url" not in vacancy:
                continue

            url_value = vacancy["url"]

            # Проверяем, что URL — строка, не пустая (даже по пробелам) и не равен "Нет ссылки"
            if (
                    not isinstance(url_value, str) or
                    not url_value.strip() or  # пустая строка + учитывает пробелы
                    url_value.strip() == "Нет ссылки"  # нормализация перед сравнением
            ):
                continue

            # Проверяем уникальность URL
            if url_value not in existing_urls:
                filtered_vacancies.append(vacancy)
                existing_urls.add(url_value)  # Обновляем набор для последующих проверок

        return filtered_vacancies

    def write_vacancies(self, vacancies: list[dict]):
        """Основной метод записи вакансий с фильтрацией."""
        # 1. Получаем существующие вакансии (объекты Vacancy)
        existing_vacancy_objects = self.get_vacancies()

        # 2. Создаём набор URL существующих вакансий для быстрого поиска
        existing_urls = {
            vac.url for vac in existing_vacancy_objects
            if hasattr(vac, "url") and vac.url and vac.url != "Нет ссылки"
        }

        # 3. Фильтруем новые вакансии через отдельный метод
        new_vacancies_to_add = self.filter_new_vacancies(vacancies, existing_urls)

        # 4. Формируем итоговый список: существующие + новые
        updated_vacancies = [
            {
                "name": vac.name,
                "salary": vac.salary,
                "url": vac.url,
                "description": vac.description,
                **{k: getattr(vac, k) for k in vac.__dict__
                 if k not in ["name", "salary_from", "salary_to", "url", "description"]}
            }
            for vac in existing_vacancy_objects
            if hasattr(vac, "url") and vac.url and vac.url != "Нет ссылки"
        ]
        updated_vacancies.extend(new_vacancies_to_add)

        # 5. Сохраняем в файл
        with open(self._filename, "w", encoding="utf-8") as f:
            json.dump(updated_vacancies, f, indent=4, ensure_ascii=False)


    def delete_vacancies(self):
        open(self._filename, "w").close()
