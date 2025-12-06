# 1. получить с HH.ru JSON как есть превратить его в список словарей all_vacancies
# 2. вытащить из all_vacancies только те поля, которые нам нужны для анализа
vacancies.append({
    "name": vacancy["name"],
    # проверяем поле name:
    # - поле везде существует?
    # - поле не None?
    # - поле строка?
    "salary": vacancy["salary"],
    # проверяем поле salary:
    # - поле везде существует?
    # - поле не None?
    # - поле словарь?
    "description": vacancy["snippet"]["responsibility"],
    # проверяем snippet:
    # - поле везде существует?
    # - поле не None?
    # - поле словарь?
    # - в поле есть responsibility?
    # проверяем responsibility:
    # - поле везде существует?
    # - поле не None?
    # - поле строка?

    "url": vacancy["alternate_url"]









    # для каждого словаря для каждого поля проверить:
    #     - существует ли это поле в структуре словаря
    #                                          - это поле None или нет