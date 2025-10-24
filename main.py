from src.classes import HHVacancies


def main():
    hh = HHVacancies()

    print("\n1. Получить вакансии")
    print("2. Показать вакансии")
    print("3. Сортировать вакансии")
    print("4. Фильтровать вакансии")
    print("5. Добавить вакансию")
    print("6. Удалить вакансию")
    print("7. Выход\n")

    while True:
        choice = input("Выберите действие (1-7): ")

        if choice in ('1', '2', '3', '4', '5', '6', '7'):
            if choice == '1':
                query = input("Введите поисковый запрос: ")
                hh.get_vacancies(query)
                hh.display_vacancies()

            elif choice == '2':
                hh.display_vacancies()

            elif choice == '3':
                key = input("Введите ключ для сортировки (title, company, salary, experience): ")
                hh.sort_vacancies(key=key)

            elif choice == '4':
                experience = input("Введите опыт работы (junior, middle, senior и т.д.): ")
                salary_from = input("Введите нижнюю границу зарплаты (если нет, нажмите Enter): ")
                if salary_from.strip() == "":
                    salary_from = None
                salary_to = input("Введите верхнюю границу зарплаты (если нет, нажмите Enter): ")
                if salary_to.strip() == "":
                    salary_to = None

                # Фильтрация вакансий по указанным параметрам
                filtered_vacancies = hh.filter_vacancies(experience=experience,
                                                         salary_from=salary_from,
                                                         salary_to=salary_to)
                hh.display_vacancies(filtered_vacancies)

            elif choice == '5':
                title = input("Введите название вакансии: ")
                company = input("Введите название компании: ")
                salary = input("Введите зарплату: ")
                experience = input("Введите требуемый опыт: ")
                hh.add_vacancy(title, company, salary, experience)
                print("Вакансия успешно добавлена!")

            elif choice == '6':
                title = input("Введите название вакансии для удаления: ")
                hh.remove_vacancy(title)
                print("Вакансия успешно удалена!")

            elif choice == '7':
                print("До свидания!")
                break

        else:
            print("Неверный выбор. Попробуйте снова.")

main()