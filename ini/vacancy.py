# Работа с вакансиями
# Создан класс для работы с вакансиями.
# В классе используется __slots__ для экономии памяти.
# У каждого экземпляра вакансии есть минимум 4 атрибута.
# В классе реализованы методы сравнения вакансий по зарплате.
# Методы сравнения реализованы через магические методы.
# В классе реализованы методы для валидации данных.
# Методы валидации — приватные.
# Методы валидации используются при инициализации атрибутов.
#
# +++
# Создать класс для работы с вакансиями.
# В этом классе самостоятельно определить атрибуты, такие как^
# название вакансии, ссылка на вакансию, зарплата, краткое описание или требования и т.п.
# (всего не менее четырех атрибутов).
# Класс должен поддерживать методы сравнения вакансий между собой по зарплате
# и валидировать данные, которыми инициализируются его атрибуты.
# Способами валидации данных может быть проверка, указана или нет зарплата.
# В этом случае выставлять значение зарплаты 0 или «Зарплата не указана» в зависимости от структуры класса.


# Вариант ИИ
from typing import Optional
from dataclasses import dataclass


@dataclass
class Vacancy:
    """
    Класс представляющий вакансию.
    Содержит основные атрибуты вакансии и методы для их валидации и сравнения.
    """

    __slots__ = ("title", "url", "salary", "description")

    title: str
    url: str
    salary: Optional[str]
    description: str

    def __post_init__(self):
        """Валидация атрибутов после инициализации."""
        self.title = self._validate_title(self.title)
        self.url = self._validate_url(self.url)
        self.salary = self._validate_salary(self.salary)
        self.description = self._validate_description(self.description)

    def _validate_title(self, title: str) -> str:
        """Валидирует название вакансии."""
        if not title or not title.strip():
            raise ValueError("Название вакансии не может быть пустым")
        return title.strip()

    def _validate_url(self, url: str) -> str:
        """Валидирует URL вакансии."""
        if not url or not url.startswith("https://"):
            raise ValueError("URL вакансии должен быть корректным")
        return url

    def _validate_salary(self, salary: Optional[str]) -> Optional[str]:
        """Валидирует зарплату вакансии."""
        if salary is None or not salary.strip():
            return "Зарплата не указана"
        return salary.strip()

    def _validate_description(self, description: str) -> str:
        """Валидирует описание вакансии."""
        if not description or not description.strip():
            return "Описание отсутствует"
        return description.strip()

    def __lt__(self, other: 'Vacancy') -> bool:
        """Сравнение по зарплате (меньше)."""
        return self._parse_salary() < other._parse_salary()

    def __le__(self, other: 'Vacancy') -> bool:
        """Сравнение по зарплате (меньше или равно)."""
        return self._parse_salary() <= other._parse_salary()

    def __eq__(self, other: 'Vacancy') -> bool:
        """Сравнение по зарплате (равно)."""
        return self._parse_salary() == other._parse_salary()

    def __gt__(self, other: 'Vacancy') -> bool:
        """Сравнение по зарплате (больше)."""
        return self._parse_salary() > other._parse_salary()

    def __ge__(self, other: 'Vacancy') -> bool:
        """Сравнение по зарплате (больше или равно)."""
        return self._parse_salary() >= other._parse_salary()

    def _parse_salary(self) -> int:
        """
        Извлекает числовое значение зарплаты для сравнения.
        Возвращает 0, если зарплата не указана или не может быть определена.
        """
        if self.salary == "Зарплата не указана":
            return 0

        import re
        numbers = re.findall(r'\d+', self.salary)
        if numbers:
            # Берём первое число как базовое значение
            return int(numbers[0])
        return 0

    def to_dict(self) -> dict:
        """Преобразует объект вакансии в словарь."""
        return {
            "title": self.title,
            "url": self.url,
            "salary": self.salary,
            "description": self.description
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Vacancy':
        """Создаёт объект вакансии из словаря."""
        return cls(
            title=data["title"],
            url=data["url"],
            salary=data.get("salary"),
            description=data["description"]
        )
