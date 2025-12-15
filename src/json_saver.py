import json
from abc import ABC, abstractmethod
from pathlib import Path
from src.vacancy import Vacancy


class AbstractFile(ABC):
    """ """

    # Методы добавления, записи, удаления Вакансий
    # @abstractmethod
    # def json_get_vacancies(self):
    #     pass

    @abstractmethod
    def add_vacancies(self, vacancies: list[Vacancy]) -> list[Vacancy]:
        """
        Добавляет новые вакансии, исключая дубликаты (по URL или иному уникальному ключу).
        :param vacancies: список объектов Vacancy для добавления
        :return: объединённый список всех вакансий (старые + новые)
        """
        pass

    def save_vacancies_to_json(self, vacancies: list[Vacancy]):
        """Метод для сохранения (записи) списка Vacancy в JSON."""
        pass

    # @abstractmethod
    # def write_vacancies(self, vacancies: list[dict]):
    #     pass

    @abstractmethod
    def delete_vacancies(self):
        pass


class JSONSaver(AbstractFile):
    def __init__(self, path="data/vacancies.json"):
        """ """
        self._filename = Path(path)  # Преобразуем в Path!
        # self._filename = path

    def _load_existing_vacancies(self) -> list[Vacancy]:
        """
        Читает существующие вакансии из JSON‑файла.

        :return: список объектов Vacancy (пустой, если файла нет или он некорректен)
        """
        if not self._filename.exists():
            return []

        try:
            with open(self._filename, encoding="utf-8") as f:
                data = json.load(f)

            # Преобразуем словари в объекты Vacancy
            vacancies = []
            for item in data:
                vacancies.append(
                    Vacancy(
                        name=item["name"],
                        salary=item.get("salary", {}),
                        url=item["url"],
                        description=item.get("description", "")
                    )
                )
            return vacancies

        except (json.JSONDecodeError, KeyError, FileNotFoundError, PermissionError) as e:
            # Логируем ошибку (опционально)
            print(f"Ошибка при чтении файла {self._filename}: {e}")
            return []

    def add_vacancies(self, vacancies_for_json: list[Vacancy]) -> list[Vacancy]:
        """Добавляет новые вакансии, избегая дубликатов по URL."""
        # Читаем существующие вакансии
        existing_vacancies = self._load_existing_vacancies()

        # Собираем URL существующих вакансий
        existing_urls = {vac.url for vac in existing_vacancies}

        # Отбираем новые вакансии (которых нет в файле)
        new_vacancies = [
            vac for vac in vacancies_for_json
            if vac.url not in existing_urls
        ]

        # Объединяем и сохраняем
        all_vacancies = existing_vacancies + new_vacancies
        # self._save_vacancies_to_json(all_vacancies)

        return all_vacancies


    def save_vacancies_to_json(self, vacancies: list[Vacancy]):
        """Метод для сохранения списка Vacancy в JSON."""
    # def _save_vacancies_to_json(self, vacancies: list[Vacancy]):
    #     """Вспомогательный метод для сохранения списка Vacancy в JSON."""
        # Преобразуем объекты Vacancy в словари для JSON
        data = []
        for vac in vacancies:
            data.append({
                "name": vac.name,
                "salary": {
                    "from": vac.salary_from,
                    "to": vac.salary_to,
                    "currency": vac.salary_currency
                },
                "url": vac.url,
                "description": vac.description,
                # Добавляем дополнительные поля, если есть
                **{k: getattr(vac, k) for k in vac.__dict__
                   if k not in ["name", "salary_from", "salary_to", "salary_currency", "url", "description"]}
            })

        with open(self._filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)


    # def write_vacancies(self, vacancies: list[Vacancy]):
    #     """Записывает список объектов Vacancy в JSON-файл."""
    #     # Преобразуем в словари
    #     vacancies_for_json = []
    #     for vac in vacancies:
    #         vacancies_for_json.append({
    #             "name": vac.name,
    #             "salary": {
    #                 "from": vac.salary_from,
    #                 "to": vac.salary_to
    #             },
    #             "url": vac.url,
    #             "description": vac.description,
    #             **{k: getattr(vac, k) for k in vac.__dict__
    #                if k not in ["name", "salary_from", "salary_to", "url", "description"]}
    #         })
    #
    #     # Передаем словари в save_to_json
    #     self.save_to_json(vacancies_for_json)

    # def write_vacancies(self, vacancies: list[dict]):
    #     """Основной метод записи вакансий с фильтрацией."""
    #     # 1. Получаем существующие вакансии (объекты Vacancy)
    #     existing_vacancy_objects = self.get_vacancies()
    #
    #     # 2. Создаём набор URL существующих вакансий для быстрого поиска
    #     existing_urls = {
    #         vac.url for vac in existing_vacancy_objects
    #         if hasattr(vac, "url") and vac.url and vac.url != "Нет ссылки"
    #     }
    #
    #     # 3. Фильтруем новые вакансии через отдельный метод
    #     new_vacancies_to_add = self.filter_new_vacancies(vacancies, existing_urls)
    #
    #     # 4. Формируем итоговый список: существующие + новые
    #     updated_vacancies = [
    #         {
    #             "name": vac.name,
    #             "salary": {"from": vac.salary_from, "to": vac.salary_to},  # исправлено! было: "salary": vac.salary,
    #             "url": vac.url,
    #             "description": vac.description,
    #             **{k: getattr(vac, k) for k in vac.__dict__
    #              if k not in ["name", "salary_from", "salary_to", "url", "description"]}
    #         }
    #         for vac in existing_vacancy_objects
    #         if hasattr(vac, "url") and vac.url and vac.url != "Нет ссылки"
    #     ]
    #     updated_vacancies.extend(new_vacancies_to_add)
    #
    #     # 5. Сохраняем в файл
    #     with open(self._filename, "w", encoding="utf-8") as f:
    #         json.dump(updated_vacancies, f, indent=4, ensure_ascii=False)


    def delete_vacancies(self):
        open(self._filename, "w").close()


    def first_save_to_json(self, vacancies_for_json: list[Vacancy]):
        """
        Сохраняет список объектов Vacancy в JSON-файл.
        :param vacancies_for_json: список объектов Vacancy
        1) Преобразуем объекты Vacancy в словари
        2) Сохраняем в файл
        """
        # 1) Преобразуем объекты Vacancy в словари
        data = []
        for vac in vacancies_for_json:
            data.append({
                "name": vac.name,
                "salary": {
                    "from": vac.salary_from,
                    "to": vac.salary_to,
                    "currency": vac.salary_currency
                },
                "url": vac.url,
                "description": vac.description,
                # Добавляем дополнительные поля (если есть)
                **{k: getattr(vac, k) for k in vac.__dict__
                   if k not in ["name", "salary_from", "salary_to", "salary_currency", "url", "description"]}
            })

        # 2) Сохраняем в файл
        with open(self._filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        print(f"Данные успешно сохранены в {self._filename}")



