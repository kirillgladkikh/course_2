from src.vacancy import Vacancy


def print_vacancies(vacancies: list[Vacancy]):
    for vac in vacancies:
        print(vac)


def get_or_zero(dct, key):
    value = dct.get(key)
    return 0 if value is None else value