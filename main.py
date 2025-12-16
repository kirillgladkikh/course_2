from collections import OrderedDict
import pprint
from src.hh_api import HHApi
from src.vacancy import Vacancy
from src.json_saver import JSONSaver
from src.utils import debug_print_vacancy_obj, input_with_default, get_valid_per_page, get_valid_top_n, get_valid_currency, vacancy_objects_for_json, filter_vacancies, get_vacancies_by_salary, sort_vacancies


from src.utils import print_vacancies


# # Создание экземпляра класса для работы с API сайтов с вакансиями
# hh = HHApi()
# # Получение filtered_vacancies: !!!список словарей!!! УЖЕ ОТФИЛЬТРОВАННЫХ ПОЛЕЙ (name, salary, url, description) вакансий с hh.ru
# filtered_vacancies = hh.hh_api_get_vacancies("python")
#
# # Вывод на экран filtered_vacancies
# print("Найденные вакансии:")
# print("=" * 40)
#
# for i, vac in enumerate(filtered_vacancies, 1):
#     print(f"\n[{i}]")
#     ordered_vac = OrderedDict([
#         ("name", vac["name"]),
#         ("salary", vac["salary"]),
#         ("description", vac["description"]),
#         ("url", vac["url"])
#     ])
#     pprint.pprint(ordered_vac, indent=2, width=60)
#
# # Формируем vacancies_for_json: список объектов Vacancy (не словарей!) с корректно обработанными полями salary_from/salary_to
# vacancies_for_json = []
# for vac_dict in filtered_vacancies:
#     vac = Vacancy(
#         name=vac_dict["name"],
#         salary=vac_dict["salary"],
#         url=vac_dict["url"],
#         description=vac_dict["description"]
#     )
#     vacancies_for_json.append(vac)
# # Теперь список объектов Vacancy (не словарей!) имеет корректно обработанные поля salary_from/salary_to
#
# # Выводим vacancies_for_json на экран
# j = 1
# for vac in vacancies_for_json:
#     print(f"[={j}=]")
#     j += 1
#     print(vac)  # Использует метод __str__
#     print("-" * 10)
#
# # Формируем saver для последующей фильтрации и сортировки по введенным пользователей условиям
# saver = JSONSaver("data/vacancies.json")  # Создаём экземпляр (файл сохранится в data/vacancies.json)
#
# # Открываем существующий JSON
# # + Добавляем новые вакансии из vacancies_for_json
# # + Сохраняем "старое"+"новое" в all_vacancies
# all_vacancies = saver.add_vacancies(vacancies_for_json)
#
# # Записываем all_vacancies в JSON-файл (предварительно преобразуя объекты Vacancy в словари!)
# saver.save_vacancies_to_json(all_vacancies)

# Возможен поиск по следующим валютам:
VALID_CURRENCY = [
    "rur",
    "kzt",
    "uzs"
]

# Функция для взаимодействия с пользователем
def user_interaction():
    """ """
    # ВВОД ПОЛЬЗОВАТЕЛЕМ ИСХОДНЫХ ДАННЫХ

    # Запрашивает у пользователя необходимость очистки существующего JSON-файла Вакансий.
    # по-умолчанию clear_json = "0"
    clear_json = input_with_default("Очистить текущий JSON с Вакансиями? (0 - НЕТ, любой символ - ДА): ", "0")
    print(f"clear_json = {clear_json}")

    # Запрашивает у пользователя поисковый запрос.
    # по-умолчанию search_query = "python"
    search_query = input_with_default("Введите поисковый запрос: ", "python").lower()
    print(f"search_query = {search_query}")

    # Запрашивает у пользователя количество вакансий на 1 странице API-запроса (1–100) с валидацией.
    # по-умолчанию per_page = 20
    per_page = get_valid_per_page()
    print(f"per_page = {per_page}")

    # Запрашивает у пользователя количество вакансий для вывода в топ N (1–100) с валидацией.
    # по-умолчанию per_page = 20
    top_n = get_valid_top_n()
    print(f"top_n = {top_n}")

    # Запрашивает у пользователя ключевые слова для фильтрации вакансий - по ВАЛЮТЕ (RUR/KZT/UZS) с валидацией.
    # по-умолчанию per_page = 20
    filter_currency = get_valid_currency(VALID_CURRENCY)
    print(f"filter_currency = {filter_currency}")

    # -----------------filter_words = input_with_default("Введите ключевые слова для фильтрации вакансий - по описанию: ", "")
    # -----------------print(filter_words)

    # ОБРАБОТКА ЗАПРОСОВ ПОЛЬЗОВАТЕЛЯ

    # ОЧИСТКА JSON - если таков выбор пользователя
    # - cоздаём экземпляр saver (файл сохранится в data/vacancies.json)
    saver = JSONSaver("data/vacancies.json")
    # - очищаем JSON если таков выбор пользователя
    if clear_json != "0":
        saver.delete_vacancies()

    # Создание экземпляра класса для работы с API сайтов с вакансиями
    hh = HHApi()
    # Получение filtered_vacancies: !!!список словарей!!! УЖЕ ОТФИЛЬТРОВАННЫХ ПОЛЕЙ (name, salary, url, description) вакансий с hh.ru
    hh_api_filtered_vacancies = hh.hh_api_get_vacancies(search_query, per_page)

    # Формируем vacancies_for_json: список объектов Vacancy (не словарей!) с корректно обработанными полями salary_from/salary_to/currency
    vacancies_for_json = vacancy_objects_for_json(hh_api_filtered_vacancies)

    # По введенным пользователей условиям: search_query, per_page
    # - открываем существующий JSON
    # - добавляем новые вакансии из vacancies_for_json
    # - сохраняем "старое"+"новое" в all_vacancies
    all_vacancies = saver.add_vacancies(vacancies_for_json)

    # - записываем all_vacancies в JSON-файл (предварительно преобразуя объекты Vacancy в словари!)
    saver.save_vacancies_to_json(all_vacancies)

    # ФИЛЬТРУЕМ, СОРТИРУЕМ, ВЫВОДИМ ТОП ВАКАНСИЙ

    filtered_vacancies = filter_vacancies(all_vacancies, filter_currency)  # Оставляем только выбранную пользователем валюту зарплаты
    debug_print_vacancy_obj(filtered_vacancies)
    ranged_vacancies = get_vacancies_by_salary(filtered_vacancies)  # Убираем из списка вакансии с нулями в зарплате
    debug_print_vacancy_obj(ranged_vacancies)
    sorted_vacancies = sort_vacancies(ranged_vacancies)  # Сортируем вакансии по убыванию
    debug_print_vacancy_obj(sorted_vacancies)
    # top_vacancies = get_top_vacancies(sorted_vacancies, top_n)  # Формируем TOP-N список вакансий
    # print_vacancies(top_vacancies)  # Выводим в консоль список вакансий сформированный по запросам пользователч

    return


if __name__ == "__main__":
    user_interaction()




















# # Преобразование набора данных из JSON в список объектов
# vacancies_list = JSONSaver.write_vacancies(hh_vacancies)
# print(vacancies_list)

# # Пример работы контструктора класса с одной вакансией
# vacancy = Vacancy("Python Developer", "<https://hh.ru/vacancy/123456>", "100 000-150 000 руб.", "Требования: опыт работы от 3 лет...")
#
# # Сохранение информации о вакансиях в файл
# # Создаём экземпляр JSONSaver
# json_saver = JSONSaver()
# # Получаем список объектов Vacancy
# vacancies = json_saver.get_vacancies()
# # Выводим каждую вакансию
# for vacancy in vacancies:
#     print(f"Название: {vacancy.title}")
#     print(f"Ссылка: {vacancy.url}")
#     print(f"Зарплата: {vacancy.salary}")
#     print(f"Требования: {vacancy.requirements}")
#     print("-" * 40)  # разделитель между вакансиями
# #


# json_saver = JSONSaver()  # создаём объект
# json_saver.write_vacancies(hh_vacancies)  # вызываем метод у объекта
# print(json_saver.write_vacancies(hh_vacancies) )


# json_saver = JSONSaver()
# json_saver.add_vacancy(vacancy)
# json_saver.delete_vacancy(vacancy)
#
# # Функция для взаимодействия с пользователем
# def user_interaction():
#     platforms = ["HeadHunter"]
#     search_query = input("Введите поисковый запрос: ")
#     top_n = int(input("Введите количество вакансий для вывода в топ N: "))
#     filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
#     salary_range = input("Введите диапазон зарплат: ") # Пример: 100000 - 150000
#
#     filtered_vacancies = filter_vacancies(vacancies_list, filter_words)
#
#     ranged_vacancies = get_vacancies_by_salary(filtered_vacancies, salary_range)
#
#     sorted_vacancies = sort_vacancies(ranged_vacancies)
#     top_vacancies = get_top_vacancies(sorted_vacancies, top_n)
#     print_vacancies(top_vacancies)


# if __name__ == "__main__":
#     user_interaction()


# print("1====================")
# text = "python"
# hh = HHApi()
# vacs = hh.get_vacancies(text)
# # print(vacs)
#
# print("2====================")
# js = JSONSaver()
# js.write_vacancies(vacs)
#
# print("3====================")
# vacancies = js.get_vacancies()
# print_vacancies(vacancies)
