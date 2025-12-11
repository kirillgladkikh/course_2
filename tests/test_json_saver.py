import pytest
import json
import os
from src.json_saver import JSONSaver
from src.vacancy import Vacancy


# === Тесты для get_vacancies ===
@pytest.fixture
def temp_json_file():
    """Временный файл для тестов. Удаляется после использования."""
    filename = "test_vacancies.json"

    def _create_file(content=None):
        with open(filename, "w", encoding="utf-8") as f:
            if content is not None:
                json.dump(content, f, ensure_ascii=False, indent=2)
            else:
                f.write("")  # пустой файл
        return filename

    def _cleanup():
        if os.path.exists(filename):
            os.remove(filename)

    yield _create_file
    _cleanup()



@pytest.fixture
def json_saver(temp_json_file):
    """Экземпляр JSONSaver с временным файлом."""
    return JSONSaver(temp_json_file())



def test_get_vacancies_file_not_found(json_saver):
    """Файл не существует → возвращается пустой список."""
    # Убедимся, что файла нет
    if os.path.exists(json_saver._filename):
        os.remove(json_saver._filename)

    result = json_saver.get_vacancies()
    assert result == []
    assert isinstance(result, list)



def test_get_vacancies_empty_file(temp_json_file, json_saver):
    """Пустой файл → возвращается пустой список."""
    temp_json_file()  # создаём пустой файл
    result = json_saver.get_vacancies()
    assert result == []
    assert isinstance(result, list)



def test_get_vacancies_invalid_json(temp_json_file, json_saver):
    """Файл с невалидным JSON → возвращается пустой список."""
    with open(json_saver._filename, "w", encoding="utf-8") as f:
        f.write("не JSON")
    result = json_saver.get_vacancies()
    assert result == []
    assert isinstance(result, list)



def test_get_vacancies_empty_array(temp_json_file, json_saver):
    """JSON: [] → возвращается пустой список."""
    temp_json_file([])
    result = json_saver.get_vacancies()
    assert result == []



def test_get_vacancies_one_vacancy(temp_json_file, json_saver):
    """Одна вакансия в JSON → возвращается [Vacancy] с корректными полями."""
    sample_data = [
        {
            "name": "Python-разработчик",
            "salary": {"from": 100000, "to": 150000, "currency": "RUB"},
            "url": "https://hh.ru/123",
            "description": "Разработка на Python"
        }
    ]
    temp_json_file(sample_data)

    result = json_saver.get_vacancies()

    assert len(result) == 1
    assert isinstance(result[0], Vacancy)

    vac = result[0]
    assert vac.name == "Python-разработчик"
    assert vac.salary_from == 100000
    assert vac.salary_to == 150000
    assert vac.url == "https://hh.ru/123"
    assert vac.description == "Разработка на Python"



def test_get_vacancies_multiple_vacancies(temp_json_file, json_saver):
    """Несколько вакансий в JSON → список из N объектов Vacancy."""
    sample_data = [
        {"name": "A", "salary": None, "url": "url1", "description": "Desc1"},
        {"name": "B", "salary": {"from": 50000}, "url": "url2", "description": "Desc2"},
        {"name": "C", "salary": {"to": 80000}, "url": "url3", "description": "Desc3"}
    ]
    temp_json_file(sample_data)

    result = json_saver.get_vacancies()

    assert len(result) == 3
    for i, vac in enumerate(result):
        assert isinstance(vac, Vacancy)
        assert vac.name == sample_data[i]["name"]
        assert vac.url == sample_data[i]["url"]



def test_get_vacancies_extra_fields(temp_json_file, json_saver):
    """Дополнительные поля в JSON → сохраняются в объекте Vacancy."""
    sample_data = [
        {
            "name": "Test",
            "salary": {"from": 70000},
            "url": "url",
            "description": "Desc",
            "id": 123,
            "city": "Москва",
            "experience": "middle"
        }
    ]
    temp_json_file(sample_data)

    result = json_saver.get_vacancies()
    vac = result[0]

    assert hasattr(vac, "id") and vac.id == 123
    assert hasattr(vac, "city") and vac.city == "Москва"
    assert hasattr(vac, "experience") and vac.experience == "middle"



def test_get_vacancies_salary_none(temp_json_file, json_saver):
    """salary: null в JSON → salary_from=0, salary_to=0."""
    sample_data = [
        {"name": "No Salary", "salary": None, "url": "url", "description": "No salary info"}
    ]
    temp_json_file(sample_data)

    result = json_saver.get_vacancies()
    vac = result[0]

    assert vac.salary_from == 0
    assert vac.salary_to == 0


# === Тесты для filter_new_vacancies ===
class TestFilterNewVacancies:

    @pytest.fixture
    def saver(self):
        return JSONSaver("dummy.json")

    def test_empty_input_list(self, saver):
        """Пустой список new_vacancies → возвращается пустой список."""
        result = saver.filter_new_vacancies([], {"url1", "url2"})
        assert result == []

    def test_no_url_field(self, saver):
        """Вакансии без поля "url" пропускаются."""
        new_vacancies = [
            {"title": "Без URL"},
            {"name": "Другая", "url": ""},  # но тут есть url (пустой)
            {"company": "No URL here"}
        ]
        existing_urls = set()
        result = saver.filter_new_vacancies(new_vacancies, existing_urls)
        assert len(result) == 0  # только пустые/отсутствующие url

    def test_url_is_empty_string(self, saver):
        """URL — пустая строка → вакансия пропускается."""
        new_vacancies = [
            {"url": "", "name": "Empty URL"},
            {"url": "  ", "name": "Whitespace URL"},  # даже пробелы — считаем пустым
            {"url": None, "name": "None URL"}
        ]
        existing_urls = set()
        result = saver.filter_new_vacancies(new_vacancies, existing_urls)
        assert len(result) == 0

    def test_url_equals_no_link_strict(self, saver):
        """Строгое сравнение: только "Нет ссылки" блокируется."""
        new_vacancies = [
            {"url": "Нет ссылки", "name": "Blocked"},
            {"url": "Нет ссылки!", "name": "Allowed"},
            {"url": "НЕТ ССЫЛКИ", "name": "Allowed (uppercase)"}
        ]
        existing_urls = set()
        result = saver.filter_new_vacancies(new_vacancies, existing_urls)
        assert len(result) == 2
        assert result[0]["name"] == "Allowed"
        assert result[1]["name"] == "Allowed (uppercase)"

    def test_valid_url_not_in_existing(self, saver):
        """Валидный URL отсутствует в existing_urls → добавляется."""
        new_vacancies = [
            {"url": "https://job1.com", "name": "Job 1"},
            {"url": "https://job2.com", "name": "Job 2"}
        ]
        existing_urls = {"https://old.com"}
        result = saver.filter_new_vacancies(new_vacancies, existing_urls)

        assert len(result) == 2
        assert "https://job1.com" in existing_urls
        assert "https://job2.com" in existing_urls

    def test_valid_url_already_exists(self, saver):
        """Валидный URL уже есть в existing_urls → пропускается."""
        new_vacancies = [
            {"url": "https://dup.com", "name": "Duplicate"},
            {"url": "https://new.com", "name": "New"}
        ]
        existing_urls = {"https://dup.com"}
        result = saver.filter_new_vacancies(new_vacancies, existing_urls)
        assert len(result) == 1
        assert result[0]["name"] == "New"
        assert "https://new.com" in existing_urls


    def test_mixed_cases(self, saver):
        """Смешанный набор: разные случаи в одном списке."""
        new_vacancies = [
            {"url": "https://valid1.com", "name": "Valid 1"},          # пройдёт
            {"title": "No URL"},                                         # нет url → пропуск
            {"url": "", "name": "Empty"},                              # пустой → пропуск
            {"url": "Нет ссылки", "name": "No Link"},               # "Нет ссылки" → пропуск
            {"url": "https://valid2.com", "name": "Valid 2"},          # пройдёт
            {"url": "https://valid1.com", "name": "Dup"},            # дубликат → пропуск
            {"url": "  https://spaced.com  ", "name": "Spaced"},    # с пробелами → пройдёт?
        ]
        existing_urls = {"https://existing.com"}

        result = saver.filter_new_vacancies(new_vacancies, existing_urls)

        assert len(result) == 3
        urls_in_result = [item["url"] for item in result]
        assert "https://valid1.com" in urls_in_result
        assert "https://valid2.com" in urls_in_result
        assert "  https://spaced.com  " in urls_in_result  # пробелы сохранены

        # existing_urls должен обновиться
        assert "https://valid1.com" in existing_urls
        assert "https://valid2.com" in existing_urls
        assert "  https://spaced.com  " in existing_urls

    def test_existing_urls_modified(self, saver):
        """Метод должен добавлять новые URL в existing_urls (передача по ссылке)."""
        new_vacancies = [{"url": "new-url.com", "name": "New Job"}]
        existing_urls = {"old.com"}

        result = saver.filter_new_vacancies(new_vacancies, existing_urls)

        assert len(result) == 1
        assert "new-url.com" in existing_urls  # existing_urls изменён!
        assert len(existing_urls) == 2

    def test_url_with_whitespace(self, saver):
        """URL с пробелами в начале/конце — считается валидным, если не пустой."""
        new_vacancies = [
            {"url": "  https://space.com  ", "name": "With Spaces"},
            {"url": "\thttps://tab.com\n", "name": "With Tab/Newline"}
        ]
        existing_urls = set()
        result = saver.filter_new_vacancies(new_vacancies, existing_urls)
        assert len(result) == 2
        assert "  https://space.com  " in existing_urls
        assert "\thttps://tab.com\n" in existing_urls

    def test_non_string_url(self, saver):
        """Поле "url" не строка (например, число) → считается пустым/невалидным."""
        new_vacancies = [
            {"url": 123, "name": "Number URL"},
            {"url": None, "name": "None URL"},
            {"url": True, "name": "Boolean URL"}
        ]
        existing_urls = set()
        result = saver.filter_new_vacancies(new_vacancies, existing_urls)
        assert len(result) == 0  # все считаются невалидными


# === Тесты для _is_duplicate ===
class TestIsDuplicate:

    @pytest.fixture
    def saver(self):
        return JSONSaver("dummy.json")

    @pytest.fixture
    def existing_vacancy(self):
        """Создаёт базовый объект Vacancy для тестов."""
        return Vacancy(
            name="Разработчик Python",
            salary={"from": 100000, "to": 150000},
            url="https://job1.com",
            description="Ищем опытного разработчика Python."
        )


    def test_name_differs(self, saver, existing_vacancy):
        """Название не совпадает → не дубликат (False)."""
        new_vacancy = {
            "name": "Аналитик данных",
            "salary": {"from": 100000, "to": 150000},
            "description": "Ищем опытного разработчика Python."
        }
        assert saver._is_duplicate(new_vacancy, existing_vacancy) is False

    def test_salary_from_differs(self, saver, existing_vacancy):
        """Отличается salary['from'] → не дубликат (False)."""
        new_vacancy = {
            "name": "Разработчик Python",
            "salary": {"from": 90000, "to": 150000},
            "description": "Ищем опытного разработчика Python."
        }
        assert saver._is_duplicate(new_vacancy, existing_vacancy) is False

    def test_salary_to_differs(self, saver, existing_vacancy):
        """Отличается salary['to'] → не дубликат (False)."""
        new_vacancy = {
            "name": "Разработчик Python",
            "salary": {"from": 100000, "to": 140000},
            "description": "Ищем опытного разработчика Python."
        }
        assert saver._is_duplicate(new_vacancy, existing_vacancy) is False

    def test_salary_missing_in_new(self, saver, existing_vacancy):
        """У новой вакансии нет salary → не сравниваем, но остальное совпадает → дубликат (True)."""
        new_vacancy = {
            "name": "Разработчик Python",
            "description": "Ищем опытного разработчика Python."
        }
        assert saver._is_duplicate(new_vacancy, existing_vacancy) is True


    def test_salary_missing_in_existing(self, saver):
        """У существующей вакансии нет salary → если у новой есть, то не дубликат."""
        existing_vacancy = Vacancy(
            name="Разработчик Python",
            salary=None,  # явно нет salary
            url="https://job1.com",
            description="Ищем опытного разработчика Python."
        )
        new_vacancy = {
            "name": "Разработчик Python",
            "salary": {"from": 100000, "to": 150000},
            "description": "Ищем опытного разработчика Python."
        }
        assert saver._is_duplicate(new_vacancy, existing_vacancy) is False


    def test_description_differs(self, saver, existing_vacancy):
        """Описание не совпадает → не дубликат (False)."""
        new_vacancy = {
            "name": "Разработчик Python",
            "salary": {"from": 100000, "to": 150000},
            "description": "Требуется junior-разработчик."
        }
        assert saver._is_duplicate(new_vacancy, existing_vacancy) is False


    def test_no_description_in_new(self, saver, existing_vacancy):
        """У новой вакансии нет description → считается несовпадением (False)."""
        new_vacancy = {
            "name": "Разработчик Python",
            "salary": {"from": 100000, "to": 150000}
        }
        assert saver._is_duplicate(new_vacancy, existing_vacancy) is False


    def test_none_values(self, saver):
        """Проверка на None в полях."""
        existing_vacancy = Vacancy(
            name=None,
            salary=None,
            url="https://job1.com",
            description=None
        )
        new_vacancy = {
            "name": None,
            "salary": None,
            "description": None
        }
        assert saver._is_duplicate(new_vacancy, existing_vacancy) is True

    def test_case_sensitivity(self, saver, existing_vacancy):
        """Сравнение чувствительно к регистру."""
        new_vacancy = {
            "name": "разработчик python",  # нижний регистр
            "salary": {"from": 100000, "to": 150000},
            "description": "ищем опытного разработчика python."  # нижний регистр
        }
        assert saver._is_duplicate(new_vacancy, existing_vacancy) is False  # регистр важен
