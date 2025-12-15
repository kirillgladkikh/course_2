from src.vacancy import Vacancy

# === Тесты для Vacancy::_validate_salary ===
import pytest


class TestVacancy:

    def test_init_basic_fields(self):
        """Проверка инициализации обязательных полей."""
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
        """salary=None → salary_from=0, salary_to=0."""
        vac = Vacancy(
            name="No Salary",
            salary=None,
            url="https://example.com",
            description="Нет зарплаты"
        )

        assert vac.salary_from == 0
        assert vac.salary_to == 0

    def test_salary_missing_from_or_to(self):
        """Отсутствие 'from'/'to' в словаре salary → значение=0."""
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
        """Значения 'from'='None' или 'to'='None' → значение=0."""
        vac = Vacancy(
            name="None Values",
            salary={"from": None, "to": None},
            url="",
            description=""
        )

        assert vac.salary_from == 0
        assert vac.salary_to == 0

    def test_extra_fields_via_kwargs(self):
        """Дополнительные поля из **kwargs сохраняются как атрибуты."""
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
        """Некорректный тип salary (не dict и не None) → TypeError."""
        with pytest.raises(TypeError) as excinfo:
            Vacancy(
                name="Invalid Salary",
                salary="not a dict",
                url="",
                description=""
            )

        assert "salary должен быть dict или None" in str(excinfo.value)

    def test_lt_comparison(self):
        """__lt__ сравнивает по salary_from."""
        vac1 = Vacancy("A", {"from": 50000}, "", "")
        vac2 = Vacancy("B", {"from": 70000}, "", "")

        assert vac1 < vac2  # 50000 < 70000
        assert not (vac2 < vac1)

    def test_str_representation(self):
        """__str__ возвращает корректный формат строки."""
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
