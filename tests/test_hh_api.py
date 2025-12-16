import pytest
from src.hh_api import HHApi


@pytest.mark.parametrize(
    "input_vacancies,expected_descriptions",
    [
        # Случай 1: snippet и responsibility присутствуют
        (
            [
                {
                    "name": "Dev1",
                    "salary": {"from": 100000},
                    "snippet": {"responsibility": "Писать код"},
                    "alternate_url": "https://job1",
                }
            ],
            ["Писать код"],
        ),
        # Случай 2: snippet есть, но responsibility отсутствует
        (
            [{"name": "Dev2", "salary": {"from": 80000}, "snippet": {}, "alternate_url": "https://job2"}],
            ["Обязанности не указаны"],
        ),
        # Случай 3: snippet отсутствует полностью
        ([{"name": "Dev3", "salary": {"from": 90000}, "alternate_url": "https://job3"}], ["Обязанности не указаны"]),
        # Случай 4: snippet есть, но не словарь (например, строка)
        (
            [
                {
                    "name": "Dev4",
                    "salary": {"from": 70000},
                    "snippet": "некоторая строка",
                    "alternate_url": "https://job4",
                }
            ],
            ["Обязанности не указаны"],
        ),
        # Случай 5: snippet — словарь, но без ключа responsibility
        (
            [
                {
                    "name": "Dev5",
                    "salary": {"from": 60000},
                    "snippet": {"other_key": "value"},
                    "alternate_url": "https://job5",
                }
            ],
            ["Обязанности не указаны"],
        ),
        # Случай 6: несколько вакансий, разные сценарии
        (
            [
                {  # есть responsibility
                    "name": "Dev6_1",
                    "salary": {"from": 50000},
                    "snippet": {"responsibility": "Тестировать"},
                    "alternate_url": "https://job6_1",
                },
                {  # нет responsibility
                    "name": "Dev6_2",
                    "salary": {"from": 40000},
                    "snippet": {},
                    "alternate_url": "https://job6_2",
                },
                {"name": "Dev6_3", "salary": {"from": 30000}, "alternate_url": "https://job6_3"},  # нет snippet
            ],
            ["Тестировать", "Обязанности не указаны", "Обязанности не указаны"],
        ),
    ],
)
def test_filter_vacancies_description(input_vacancies, expected_descriptions):
    """
    Проверяет, что filter_vacancies корректно обрабатывает разные варианты поля 'responsibility'.
    """
    result = HHApi.filter_vacancies(input_vacancies)  # Вызываем статический метод

    # Проверяем, что количество результатов совпадает
    assert len(result) == len(expected_descriptions)

    # Проверяем каждое описание
    for i, vacancy in enumerate(result):
        assert vacancy["description"] == expected_descriptions[i]

    # Дополнительно проверяем, что остальные поля тоже есть и не None
    for vacancy in result:
        assert "name" in vacancy
        assert "salary" in vacancy
        assert "url" in vacancy
        assert isinstance(vacancy["description"], str)


@pytest.mark.parametrize(
    "input_vacancy,expected_salary",
    [
        # Сценарий 1: salary присутствует и является словарём (корректный формат)
        (
            {
                "name": "Dev1",
                "salary": {"from": 100000, "to": 150000, "currency": "RUB"},
                "snippet": {"responsibility": "Писать код"},
                "alternate_url": "https://job1",
            },
            {"from": 100000, "to": 150000, "currency": "RUB"},
        ),
        # Сценарий 2: salary отсутствует в вакансии
        (
            {
                "name": "Dev2",
                # salary отсутствует
                "snippet": {"responsibility": "Тестировать"},
                "alternate_url": "https://job2",
            },
            None,  # Ожидаем None, если salary нет
        ),
        # Сценарий 3: salary есть, но это не словарь (например, строка)
        # В текущем коде такая ситуация приведёт к salary_info = None
        (
            {
                "name": "Dev3",
                "salary": "от 80000 до 120000 руб.",  # строка
                "snippet": {"responsibility": "Рефакторинг"},
                "alternate_url": "https://job3",
            },
            None,  # В текущей логике: не-словарь → salary_info = None
        ),
        # Дополнительный сценарий: salary-словарь без некоторых полей
        (
            {
                "name": "Dev4",
                "salary": {
                    "from": 90000
                    # "to" и "currency" отсутствуют
                },
                "snippet": {"responsibility": "Деплой"},
                "alternate_url": "https://job4",
            },
            {"from": 90000, "to": None, "currency": None},  # отсутствует → None  # отсутствует → None
        ),
        (
            {
                "name": "Dev4",
                "salary": {
                    # "from" отсутствуют
                    "to": 90000
                    # "currency" отсутствуют
                },
                "snippet": {"responsibility": "Деплой"},
                "alternate_url": "https://job4",
            },
            {"from": None, "to": 90000, "currency": None},  # отсутствует → None  # отсутствует → None
        ),
    ],
)
def test_filter_vacancies_salary(input_vacancy, expected_salary):
    """
    Проверяет, как filter_vacancies обрабатывает разные варианты поля 'salary':
    - присутствует и является словарём;
    - отсутствует;
    - не является словарём (например, строка).
    """
    # Вызываем статический метод класса
    result = HHApi.filter_vacancies([input_vacancy])

    # Проверяем, что вернулась ровно одна вакансия
    assert len(result) == 1
    vacancy = result[0]

    # Проверяем поле 'salary'
    assert vacancy["salary"] == expected_salary

    # Дополнительно проверяем другие обязательные поля
    assert "name" in vacancy
    assert "description" in vacancy
    assert "url" in vacancy
    assert isinstance(vacancy["description"], str)
    assert isinstance(vacancy["url"], str)
