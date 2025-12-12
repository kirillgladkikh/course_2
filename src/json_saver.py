import json
from abc import ABC, abstractmethod
from src.vacancy import Vacancy


class AbstractFile(ABC):
    """ """

    # Методы добавления, записи, удаления Вакансий
    @abstractmethod
    def json_get_vacancies(self):
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


    def json_get_vacancies(self) -> list[Vacancy]:
        """
        Возвращает список объектов Vacancy из JSON‑файла.
        Если файл не существует или пуст — возвращает шаблон с одной пустой вакансией.
        """
        try:
            with open(self._filename, encoding="utf-8") as f:
                data = json.load(f)
                # Если файл существует, но пуст (например, [] или {}), считаем ошибкой
                if not data:
                    raise json.JSONDecodeError("Empty JSON file", "", 0)
        except (FileNotFoundError, json.JSONDecodeError):
            # Возвращаем шаблон с одной пустой вакансией
            data = [
                {
                    "name": "",
                    "salary": {
                        "from": 0,
                        "to": 0
                    },
                    "url": "",
                    "description": ""
                }
            ]

        vacancies = []
        for vacancy in data:
            vacancies.append(Vacancy(**vacancy))
        return vacancies

        # """
        # Возвращает список объектов Vacancy из JSON‑файла.
        # Если файл не существует или пуст — возвращает пустой список.
        # """
        # try:
        #     with open(self._filename, encoding="utf-8") as f:
        #         data = json.load(f)
        # except (FileNotFoundError, json.JSONDecodeError):
        #     return []  # Возвращаем пустой список при отсутствии файла или ошибке парсинга
        #
        # vacancies = []
        # for vacancy in data:
        #     vacancies.append(Vacancy(**vacancy))
        # return vacancies

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

    def _is_duplicate(self, new_vacancy: dict, existing_vacancy: 'Vacancy') -> bool:
        # Сравниваем название (без учёта регистра)
        if (new_vacancy.get("name") or "").lower() != (existing_vacancy.name or "").lower():
            return False

        # Если у новой вакансии есть salary — сравниваем
        if "salary" in new_vacancy:
            # Если salary в новой вакансии — None, считаем, что поля совпадают
            if new_vacancy["salary"] is None:
                # Проверяем, есть ли атрибут salary у существующего объекта и не None ли он
                if hasattr(existing_vacancy, "salary") and existing_vacancy.salary is not None:
                    return False
            else:
                # salary не None — проверяем поля
                if not hasattr(existing_vacancy, "salary") or existing_vacancy.salary is None:
                    return False
                new_salary = new_vacancy["salary"]
                existing_salary = existing_vacancy.salary
                if (new_salary.get("from") != existing_salary.get("from") or
                        new_salary.get("to") != existing_salary.get("to")):
                    return False

        # Сравниваем описание с обработкой None (без учёта регистра)
        if (new_vacancy.get("description") or "").lower() != (existing_vacancy.description or "").lower():
            return False

        return True

    def filter_duplicates(self, new_vacancies: list[dict], existing_objects: list['Vacancy']) -> list[dict]:
        """
        Фильтрует новые вакансии, удаляя дубликаты по содержанию (name + salary + description).

        Args:
            new_vacancies: список новых вакансий (словарей)
            existing_objects: список существующих объектов Vacancy

        Returns:
            Список вакансий без дубликатов по содержанию.
        """
        filtered = []
        for new_vac in new_vacancies:
            is_duplicate = False
            for exist_vac in existing_objects:
                if self._is_duplicate(new_vac, exist_vac):
                    is_duplicate = True
                    break
            if not is_duplicate:
                filtered.append(new_vac)
        return filtered

    def write_vacancies(self, vacancies: list[Vacancy]):
        """Записывает список объектов Vacancy в JSON-файл."""
        # Преобразуем в словари
        vacancies_for_json = []
        for vac in vacancies:
            vacancies_for_json.append({
                "name": vac.name,
                "salary": {
                    "from": vac.salary_from,
                    "to": vac.salary_to
                },
                "url": vac.url,
                "description": vac.description,
                **{k: getattr(vac, k) for k in vac.__dict__
                   if k not in ["name", "salary_from", "salary_to", "url", "description"]}
            })

        # Передаем словари в save_to_json
        self.save_to_json(vacancies_for_json)

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
                    "to": vac.salary_to
                },
                "url": vac.url,
                "description": vac.description,
                # Добавляем дополнительные поля (если есть)
                **{k: getattr(vac, k) for k in vac.__dict__
                   if k not in ["name", "salary_from", "salary_to", "url", "description"]}
            })

        # 2) Сохраняем в файл
        with open(self._filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        print(f"Данные успешно сохранены в {self._filename}")
