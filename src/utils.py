from src.vacancy import Vacancy


def print_vacancies(vacancies: list[Vacancy]):
    for vac in vacancies:
        print(vac)


def is_field_exist(dictionary: dict, field: str) -> bool:
    return dictionary.get(field)


def is_field_dict(dictionary: dict, field: str):
    return isinstance(dictionary["field"], dict)


def is_sub_field_in_field():
    pass
