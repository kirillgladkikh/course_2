class Vacancy:
    __slots__ = ("name", "salary_from", "salary_to", "currency", "url", "description", "__dict__")

    def __init__(self, name, salary, url, description, **kwargs):
        self.name = name
        self.url = url
        self.description = description
        self._validate_salary(salary)

        # Сохраняем дополнительные поля
        for key, value in kwargs.items():
            setattr(self, key, value)

    def _validate_salary(self, salary: dict):
        if salary is None:
            self.salary_from = 0
            self.salary_to = 0
            self.salary_currency = None
        elif isinstance(salary, dict):

            from_value = salary.get("from")
            self.salary_from = 0 if from_value is None else from_value

            to_value = salary.get("to")
            self.salary_to = 0 if to_value is None else to_value

            self.salary_currency = salary.get("currency")

        else:
            raise TypeError(
                f"salary должен быть dict или None, получено: {type(salary).__name__}"
            )

    def __lt__(self, other):
        return self.salary_from < other.salary_from

    def __str__(self):
        return (
            f"Название вакансии: {self.name}\n"
            f"Зарплата: от {self.salary_from} до {self.salary_to}\n"
            f"Валюта: {self.salary_currency}\n"
            f"Ссылка: {self.url}\n"
            f"Описание вакансии: {self.description}"
        )


if __name__ == "__main__":
    vac = Vacancy("qwerty", {"from": 1, "to": 10, "currency": "RUR"}, 1, 1)
    print(vac)
