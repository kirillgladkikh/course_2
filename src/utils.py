from collections import defaultdict

from src.vacancy import Vacancy


def print_vacancies(vacancies: list[Vacancy]):
    for vac in vacancies:
        print(vac)


def print_vacancy_obj(obj_for_print: list[Vacancy]):
    # Выводим список объектов Vacancy на экран - для отладки
    j = 1
    for vac in obj_for_print:
        print(f"[={j}=]")
        j += 1
        print(vac)  # Использует метод __str__
        print("-" * 10)
    return


def input_with_default(prompt, default):
    user_input = input(prompt)
    return user_input if user_input else default


def get_valid_per_page():
    """Запрашивает у пользователя количество вакансий на странице (1–100) с валидацией."""
    while True:
        try:
            per_page = int(input_with_default(
                "Введите количество вакансий на 1 странице API-запроса (1–100): ",
                "20"
            ))
            if 1 <= per_page <= 100:
                return per_page
            else:
                print("Значение должно быть от 1 до 100.")
        except ValueError:
            print("Пожалуйста, введите целое число.")
    return per_page


def get_valid_top_n():
    while True:
        top_n = int(input_with_default("Введите количество вакансий для вывода в топ N (1–100): ", "20"))
        if 1 <= top_n <= 100:
            break
        else:
            print("Значение должно быть от 1 до 100.")
    return top_n


def get_valid_currency(VALID_CURRENCY: list):
    while True:
        filter_currency = input_with_default(
            "Введите ключевые слова для фильтрации вакансий - по ВАЛЮТЕ (RUR/KZT/UZS): ", "RUR").lower()
        if filter_currency in VALID_CURRENCY:
            break
        else:
            print("Валюта должна быть: или RUR или KZT или UZS.")
    return filter_currency.upper()


def vacancy_objects_for_json(filtered_vacancies: list) -> list:
    vacancies_for_json = []
    for vac_dict in filtered_vacancies:
        vac = Vacancy(
            name=vac_dict["name"],
            salary=vac_dict["salary"],
            url=vac_dict["url"],
            description=vac_dict["description"]
        )
        vacancies_for_json.append(vac)
    return vacancies_for_json
    # Теперь список объектов Vacancy (не словарей!) имеет корректно обработанные поля salary_from/salary_to


def filter_vacancies(all_vacancies: list[Vacancy], filter_currency: str) -> list[Vacancy]:
    filtered = []
    for vacancy in all_vacancies:
        if vacancy.salary_currency == filter_currency.upper():
            filtered.append(vacancy)
    return filtered



def get_vacancies_by_salary(vacancies: list[Vacancy]) -> list[Vacancy]:
    result = []
    for vacancy in vacancies:
        if vacancy.salary_from > 0:
            result.append(vacancy)
    return result


def sort_vacancies(vacancies: list[Vacancy]) -> list[Vacancy]:
    return sorted(vacancies, reverse=True)


def get_top_vacancies(sorted_vacancies: list[Vacancy], top_n: int) -> list[Vacancy]:
    """
    Возвращает топ-N вакансий из отсортированного списка.

    Args:
        sorted_vacancies: список объектов Vacancy, предварительно отсортированный
                    (обычно по убыванию зарплаты)
        top_n: количество вакансий для включения в топ (целое положительное число)

    Returns:
        Список из top_n объектов Vacancy (или меньше, если исходный список короче)

    Raises:
        ValueError: если top_n отрицательное
        TypeError: если top_n не является целым числом
    """
    # Проверка типов и значений
    if not isinstance(top_n, int):
        raise TypeError("top_n должен быть целым числом")

    if top_n < 0:
        raise ValueError("top_n не может быть отрицательным")

    # Возвращаем срез списка: первые top_n элементов
    # Если список короче top_n, вернём всё, что есть
    return sorted_vacancies[:top_n]


def print_vacancy_count(top_vacancies: list[Vacancy]) -> None:
    # Получаем количество доступных вакансий
    total_available = len(top_vacancies)

    # Выводим информационное сообщение
    print(f"Всего нашлось {total_available} вакансий под заданные условия")

    return
