import pytest
from src.vacancy import Vacancy

# === Тесты для Vacancy::_validate_salary ===
class TestVacancy:
    """
    Набор тестов для проверки корректности работы класса Vacancy.

    Тестируются:
    - инициализация основных полей;
    - обработка различных вариантов поля salary;
    - добавление дополнительных атрибутов через **kwargs;
    - валидация типов данных;
    - методы сравнения и строкового представления.
    """

    def test_init_basic_fields(self):
        """
        Проверяет корректную инициализацию обязательных полей объекта Vacancy.

        Сценарий:
        - Создаётся экземпляр Vacancy с базовыми полями (name, salary, url, description).
        - Проверяется соответствие сохранённых значений переданным при инициализации.

        Ожидаемый результат:
        Все основные атрибуты объекта соответствуют переданным значениям.
        """
        vac = Vacancy(
            name="Python Dev",
            salary={"from": 100000, "to": 150000},
            url="https://example.com",
            description="Разработка на Python"
        )

        assert vac.name == "Python Dev"
        assert vac.salary_from == 100000
        assert vac.salary_to == 150000
        assert vac.url == "https://example.com"
        assert vac.description == "Разработка на Python"

    def test_salary_none(self):
        """
        Проверяет обработку случая, когда salary=None.

        Сценарий:
        - Создаётся экземпляр Vacancy с salary=None.
        - Проверяется, что salary_from и salary_to установлены в 0.

        Ожидаемый результат:
        При salary=None атрибуты salary_from и salary_to равны 0.
        """
        vac = Vacancy(
            name="No Salary",
            salary=None,
            url="https://example.com",
            description="Нет зарплаты"
        )

        assert vac.salary_from == 0
        assert vac.salary_to == 0

    def test_salary_missing_from_or_to(self):
        """
        Проверяет обработку отсутствующих ключей 'from' или 'to' в словаре salary.

        Сценарий:
        - Создаются два экземпляра Vacancy:
          - первый без ключа 'from';
          - второй без ключа 'to'.
        - Проверяется, что отсутствующее значение заменяется на 0.

        Ожидаемый результат:
        Отсутствующий ключ ('from' или 'to') приводит к установке соответствующего атрибута в 0.
        """
        # Нет 'from'
        vac1 = Vacancy(
            name="Missing From",
            salary={"to": 80000},
            url="",
            description=""
        )
        assert vac1.salary_from == 0
        assert vac1.salary_to == 80000

        # Нет 'to'
        vac2 = Vacancy(
            name="Missing To",
            salary={"from": 60000},
            url="",
            description=""
        )
        assert vac2.salary_from == 60000
        assert vac2.salary_to == 0

    def test_salary_none_values(self):
        """
        Проверяет обработку значений None внутри словаря salary.

        Сценарий:
        - Создаётся экземпляр Vacancy с salary={"from": None, "to": None}.
        - Проверяется, что оба атрибута (salary_from, salary_to) установлены в 0.

        Ожидаемый результат:
        Значения None в словаре salary приводят к установке соответствующих атрибутов в 0.
        """
        vac = Vacancy(
            name="None Values",
            salary={"from": None, "to": None},
            url="",
            description=""
        )

        assert vac.salary_from == 0
        assert vac.salary_to == 0

    def test_extra_fields_via_kwargs(self):
        """
        Проверяет сохранение дополнительных полей, переданных через **kwargs.

        Сценарий:
        - Создаётся экземпляр Vacancy с дополнительными ключевыми аргументами (city, experience, id).
        - Проверяется наличие и корректность значений этих атрибутов.

        Ожидаемый результат:
        Все дополнительные поля из **kwargs сохраняются как атрибуты объекта.
        """
        vac = Vacancy(
            name="Extra Fields",
            salary={"from": 50000},
            url="",
            description="",
            city="Москва",
            experience="middle",
            id=123
        )

        assert hasattr(vac, "city") and vac.city == "Москва"
        assert hasattr(vac, "experience") and vac.experience == "middle"
        assert hasattr(vac, "id") and vac.id == 123

    def test_invalid_salary_type(self):
        """
        Проверяет валидацию типа поля salary.

        Сценарий:
        - Попытка создать экземпляр Vacancy с некорректным типом salary (строка вместо dict/None).
        - Проверка на возникновение исключения TypeError.

        Ожидаемый результат:
        При некорректном типе salary поднимается TypeError с сообщением о требуемом типе.
        """
        with pytest.raises(TypeError) as excinfo:
            Vacancy(
                name="Invalid Salary",
                salary="not a dict",
                url="",
                description=""
            )

        assert "salary должен быть dict или None" in str(excinfo.value)

    def test_lt_comparison(self):
        """
        Проверяет работу метода __lt__ (меньше) для сравнения вакансий.

        Сценарий:
        - Создаются две вакансии с разными значениями salary_from.
        - Проверяется корректность сравнения через оператор <.

        Ожидаемый результат:
        Сравнение осуществляется по атрибуту salary_from (меньшая зарплата → меньшая вакансия).
        """
        vac1 = Vacancy("A", {"from": 50000}, "", "")
        vac2 = Vacancy("B", {"from": 70000}, "", "")

        assert vac1 < vac2  # 50000 < 70000
        assert not (vac2 < vac1)

    def test_str_representation(self):
        """
        Проверяет строковое представление объекта Vacancy через метод __str__.

        Сценарий:
        - Создаётся экземпляр Vacancy с полным набором полей (включая валюту).
        - Сравнивается результат str(vac) с ожидаемым форматом строки.

        Ожидаемый результат:
        Метод __str__ возвращает строку с форматированным описанием вакансии, включающим:
        название, зарплату (от/до), валюту, ссылку и описание.
        """
        vac = Vacancy(
            name="Test Job",
            salary={"from": 40000, "to": 60000, "currency": "RUB"},
            url="https://test.com",
            description="Описание"
        )

        expected = (
            "Название вакансии: Test Job\n"
            "Зарплата: от 40000 до 60000\n"
            "Валюта: RUB\n"
            "Ссылка: https://test.com\n"
            "Описание вакансии: Описание"
        )

        assert str(vac) == expected
