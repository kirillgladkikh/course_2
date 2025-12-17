import pytest
from src.vacancy import Vacancy
from src.utils import (
    print_vacancy_obj,
    input_with_default,
    get_valid_per_page,
    get_valid_top_n,
    get_valid_currency,
    vacancy_objects_for_json,
    filter_vacancies_by_currency,
    filter_vacancies_by_words,
    get_vacancies_by_salary,
    sort_vacancies,
    get_top_vacancies,
    print_vacancy_count,
)


# Тестовые данные
@pytest.fixture
def sample_vacancies():
    """Создаёт список тестовых объектов Vacancy."""
    return [
        Vacancy(
            name="Разработчик Python",
            salary={"from": 100000, "to": 150000, "currency": "RUR"},
            url="https://example.com/1",
            description="Ищем Python-разработчика с опытом 3+ года. Знание Django обязательно."
        ),
        Vacancy(
            name="Frontend-специалист",
            salary={"from": 80000, "to": 120000, "currency": "KZT"},
            url="https://example.com/2",
            description="Требуется специалист по React и Vue. Опыт от 2 лет."
        ),
        Vacancy(
            name="Аналитик данных",
            salary=None,
            url="https://example.com/3",
            description="Анализ данных, построение дашбордов. Знание SQL и Python."
        )
    ]

@pytest.fixture
def valid_currency_list():
    return ["RUR", "KZT", "UZS"]


# Тесты для filter_vacancies_by_currency
def test_filter_vacancies_by_currency_rur(sample_vacancies, valid_currency_list):
    result = filter_vacancies_by_currency(sample_vacancies, "RUR")
    assert len(result) == 1
    assert result[0].name == "Разработчик Python"

def test_filter_vacancies_by_currency_kzt(sample_vacancies, valid_currency_list):
    result = filter_vacancies_by_currency(sample_vacancies, "KZT")
    assert len(result) == 1
    assert result[0].name == "Frontend-специалист"

def test_filter_vacancies_by_currency_empty(sample_vacancies, valid_currency_list):
    result = filter_vacancies_by_currency(sample_vacancies, "UZS")
    assert len(result) == 0


# Тесты для filter_vacancies_by_words
def test_filter_vacancies_by_words_single(sample_vacancies):
    result = filter_vacancies_by_words(sample_vacancies, ["Python"])
    assert len(result) == 2  # Python в названии и описании

def test_filter_vacancies_by_words_multiple(sample_vacancies):
    result = filter_vacancies_by_words(sample_vacancies, ["Python", "Django"])
    assert len(result) == 1  # Только где есть оба слова
    assert result[0].name == "Разработчик Python"

def test_filter_vacancies_by_words_no_match(sample_vacancies):
    result = filter_vacancies_by_words(sample_vacancies, ["Rust"])
    assert len(result) == 0

def test_filter_vacancies_by_words_empty_keywords(sample_vacancies):
    result = filter_vacancies_by_words(sample_vacancies, [])
    assert result == sample_vacancies  # Возвращает исходный список

def test_filter_vacancies_by_words_invalid_input():
    with pytest.raises(TypeError):
        filter_vacancies_by_words([], "not a list")

    with pytest.raises(TypeError):
        filter_vacancies_by_words([], [123])