import json
from abc import ABC, abstractmethod
from pathlib import Path
from src.vacancy import Vacancy


class AbstractFile(ABC):
    """ """

    # Методы добавления, записи, удаления Вакансий
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
                        name=item.get("name", ""),  # Значение по умолчанию
                        salary=item.get("salary", {}),  # Значение по умолчанию
                        # name=item["name"],
                        # salary=item.get("salary", {}),
                        url=item["url"],  # Обязательное поле
                        description=item.get("description", "")  # Значение по умолчанию
                        # description=item.get("description", "")
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

        # Объединяем старые и новые вакансии в единый файл (без записи в JSON!)
        all_vacancies = existing_vacancies + new_vacancies
        # self._save_vacancies_to_json(all_vacancies)

        return all_vacancies


    def save_vacancies_to_json(self, vacancies: list[Vacancy]):
        """Метод для сохранения списка Vacancy в JSON."""
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

        print(f"\nОбновленный перечень Вакансий успешно сохранен в файл: {self._filename}")


    def delete_vacancies(self):
        """ """
        open(self._filename, "w").close()

        print(f"\nВакансии успешно удалены из {self._filename}")
