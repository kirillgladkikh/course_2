import pytest
import json
import os
from src.json_saver import JSONSaver
from src.vacancy import Vacancy



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
