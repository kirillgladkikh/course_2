from collections import OrderedDict
import pprint
from src.hh_api import HHApi
from src.vacancy import Vacancy
from src.json_saver import JSONSaver

from src.utils import print_vacancies


# Создание экземпляра класса для работы с API сайтов с вакансиями
hh = HHApi()
# Получение УЖЕ ОТФИЛЬТРОВАННЫХ ПОЛЕЙ (name, salary, url, description) вакансий с hh.ru в список словарей
filtered_vacancies = hh.get_vacancies("python")

# Вывод на экран отфильтрованного списка словарей с вакансиями полученными по api
print("Найденные вакансии:")
print("=" * 40)

for i, vac in enumerate(filtered_vacancies, 1):
    print(f"\n[{i}]")
    ordered_vac = OrderedDict([
        ("name", vac["name"]),
        ("salary", vac["salary"]),
        ("description", vac["description"]),
        ("url", vac["url"])
    ])
    pprint.pprint(ordered_vac, indent=2, width=60)

# Формируем список словарей вакансий под формат JSON
vacancies_for_json = []
for vac_dict in filtered_vacancies:
    vac = Vacancy(
        name=vac_dict["name"],
        salary=vac_dict["salary"],
        url=vac_dict["url"],
        description=vac_dict["description"]
    )
    vacancies_for_json.append(vac)
# Теперь все объекты Vacancy имеют корректно обработанные поля salary_from/salary_to

# Выводим vacancies_for_json на экран
for vac in vacancies_for_json:
    print(vac)  # Использует метод __str__

# # Сохраняем отфильтрованный список словарей в JSON
# # --- Запись в JSON-файл ---
saver = JSONSaver("data/vacancies.json")  # Создаём экземпляр (файл сохранится в data/vacancies.json)
saver.write_vacancies(vacancies_for_json)  # Записываем список словарей в файл
#
# print("\nВакансии успешно сохранены в файл data/vacancies.json")




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
