class Vacancy:
    __slots__ = ["name", "salary_from", "salary_to", "url", "description"]

    def __init__(self, name, salary, url, description):
        self.name = name
        self.url = url
        self.description = description

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
        return f"Название вакансии: {self.name}"

vac = Vacancy(1, 1, 1, 1) #----
print(vac) #---