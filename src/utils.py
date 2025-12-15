from src.vacancy import Vacancy


def print_vacancies(vacancies: list[Vacancy]):
    for vac in vacancies:
        print(vac)


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
