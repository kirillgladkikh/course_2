from vacancy import Vacancy
from json_saver import JSONSaver


def main():
    # 1. Создаём несколько вакансий
    vacancies = [
        Vacancy(
            title="Python-разработчик",
            company="TechCorp",
            salary=150000,
            city="Москва",
            url="https://example.com/vacancy/1"
        ),
        Vacancy(
            title="Frontend-разработчик",
            company="WebSoft",
            salary=120000,
            city="Санкт-Петербург",
            url="https://example.com/vacancy/2"
        )
    ]

    # 2. Создаём савер для работы с файлом "my_vacancies.json"
    saver = JSONSaver("my_vacancies.json")

    # 3. Сохраняем список вакансий в файл
    print("Сохраняем вакансии в файл...")
    saver.save(vacancies)
    print("Вакансии сохранены.\n")

    # 4. Загружаем вакансии из файла
    print("Загружаем вакансии из файла...")
    loaded_vacancies = saver.load()
    print(f"Загружено {len(loaded_vacancies)} вакансий:")
    for vac in loaded_vacancies:
        print(f"- {vac.title} в {vac.company}, {vac.salary} руб.")
    print()

    # 5. Добавляем новую вакансию
    new_vacancy = Vacancy(
        title="Data Scientist",
        company="AI Labs",
        salary=200000,
        city="Новосибирск",
        url="https://example.com/vacancy/3"
    )
    print("Добавляем новую вакансию...")
    saver.add(new_vacancy)
    print("Вакансия добавлена.\n")

    # 6. Снова загружаем и выводим все вакансии
    print("Проверяем обновлённый список:")
    updated_vacancies = saver.load()
    print(f"Теперь в файле {len(updated_vacancies)} вакансий:")
    for vac in updated_vacancies:
        print(f"- {vac.title} в {vac.company}, {vac.salary} руб.")
    print()

    # 7. Очищаем файл (опционально)
    print("Очищаем файл...")
    saver.clear()
    print("Файл очищен.")



if __name__ == "__main__":
    main()











# from src.classes import HHVacancies
#
#
# def main():
#     hh = HHVacancies()
#
#     print("\n1. Получить вакансии")
#     print("2. Показать вакансии")
#     print("3. Сортировать вакансии")
#     print("4. Фильтровать вакансии")
#     print("5. Добавить вакансию")
#     print("6. Удалить вакансию")
#     print("7. Выход\n")
#
#     while True:
#         choice = input("Выберите действие (1-7): ")
#
#         if choice in ('1', '2', '3', '4', '5', '6', '7'):
#             if choice == '1':
#                 query = input("Введите поисковый запрос: ")
#                 hh.get_vacancies(query)
#                 hh.display_vacancies()
#
#             elif choice == '2':
#                 hh.display_vacancies()
#
#             elif choice == '3':
#                 key = input("Введите ключ для сортировки (title, company, salary, experience): ")
#                 hh.sort_vacancies(key=key)
#
#             elif choice == '4':
#                 experience = input("Введите опыт работы (junior, middle, senior и т.д.): ")
#                 salary_from = input("Введите нижнюю границу зарплаты (если нет, нажмите Enter): ")
#                 if salary_from.strip() == "":
#                     salary_from = None
#                 salary_to = input("Введите верхнюю границу зарплаты (если нет, нажмите Enter): ")
#                 if salary_to.strip() == "":
#                     salary_to = None
#
#                 # Фильтрация вакансий по указанным параметрам
#                 filtered_vacancies = hh.filter_vacancies(experience=experience,
#                                                          salary_from=salary_from,
#                                                          salary_to=salary_to)
#                 hh.display_vacancies(filtered_vacancies)
#
#             elif choice == '5':
#                 title = input("Введите название вакансии: ")
#                 company = input("Введите название компании: ")
#                 salary = input("Введите зарплату: ")
#                 experience = input("Введите требуемый опыт: ")
#                 hh.add_vacancy(title, company, salary, experience)
#                 print("Вакансия успешно добавлена!")
#
#             elif choice == '6':
#                 title = input("Введите название вакансии для удаления: ")
#                 hh.remove_vacancy(title)
#                 print("Вакансия успешно удалена!")
#
#             elif choice == '7':
#                 print("До свидания!")
#                 break
#
#         else:
#             print("Неверный выбор. Попробуйте снова.")
#
# main()