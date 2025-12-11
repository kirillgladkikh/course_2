class Vacancy:
    __slots__ = ["name", "salary_from", "salary_to", "url", "description"]

    def __init__(self, name, salary, url, description, **kwargs):
        self.name = name
        self.url = url
        self.description = description
        self._validate_salary(salary)
        # Остальные поля (например, 'id') сохраняются, но не используются
        for key, value in kwargs.items():
            setattr(self, key, value)

    def _validate_salary(self, salary: dict):
        if salary:
            self.salary_from = salary["from"] if salary["from"] else 0
            self.salary_to = salary["to"] if salary["to"] else 0
        else:
            self.salary_from = 0
            self.salary_to = 0

    def __lt__(self, other):
        return self.salary_from < other.salary_from

    def __str__(self):
        return (
            f"Название вакансии: {self.name}\n"
            f"Зарплата: от {self.salary_from} до {self.salary_to}\n"
            f"Ссылка: {self.url}\n"
            f"Описание вакансии: {self.description}"
        )


if __name__ == "__main__":
    vac = Vacancy("qwerty", {"from": 1, "to": 10}, 1, 1)
    print(vac)
