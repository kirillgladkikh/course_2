# Создать абстрактный класс для работы с API сервиса с вакансиями.
# Реализовать класс, наследующийся от абстрактного класса, для работы с платформой hh.ru.
# Класс должен уметь подключаться к API и получать вакансии.

# Код КВГ микс ИИ+задание
from abc import ABC, abstractmethod
import requests



class FileWorker:
    def save_to_json(self, data, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def save_to_csv(self, data, filename):
        # логика сохранения в CSV
        pass

    def read_json(self, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)


class Parser(ABC):
    """
    Абстрактный класс для работы с API сервисов с вакансиями.
    Определяет общий интерфейс для парсеров вакансий.
    """

    @abstractmethod
    def load_vacancies(self, keyword):
        """
        Абстрактный метод для загрузки вакансий по ключевому слову.
        Должен быть реализован в каждом конкретном парсере.

        :param keyword: ключевое слово для поиска вакансий
        :return: список вакансий (структура зависит от API)
        """
        pass


class HH(Parser):
    """
    Класс для работы с API HeadHunter.
    Реализует методы абстрактного класса Parser.
    """

    def __init__(self, file_worker):
        self.url = 'https://api.hh.ru/vacancies'
        self.headers = {'User-Agent': 'HH-User-Agent'}
        self.params = {'text': '', 'page': 0, 'per_page': 100}
        self.vacancies = []
        super().__init__(file_worker)

    def load_vacancies(self, keyword):
        """
        Загружает вакансии с HH.ru по заданному ключевому слову.

        :param keyword: ключевое слово для поиска
        """
        self.params['text'] = keyword
        self.vacancies = []  # очищаем список перед новой загрузкой

        while self.params.get('page') < 20:  # исправлено: было != 20
            response = requests.get(self.url, headers=self.headers, params=self.params)

            if response.status_code != 200:
                print(f"Ошибка при запросе: {response.status_code}")
                break

            data = response.json()
            vacancies = data.get('items', [])  # если ключа 'items' нет, вернётся пустой список []
            # программа продолжит работу без ошибок.

            if not vacancies:  # если вакансий больше нет
                break

            self.vacancies.extend(vacancies)
            self.params['page'] += 1


# Пример использования
if __name__ == '__main__':
    # Создаем экземпляр парсера
    parser = HH(None)

    # Загружаем вакансии по ключевому слову
    parser.load_vacancies('Python')

    # Выводим количество найденных вакансий
    print(f'Найдено вакансий: {len(parser.vacancies)}')

    # Выводим первые 5 вакансий (пример структуры)
    for i, vacancy in enumerate(parser.vacancies[:5]):
        print(f'{i + 1}. {vacancy["name"]} в {vacancy["employer"]["name"]}')
        print(f'   Зарплата: {vacancy.get("salary")}')
        print(f'   Ссылка: https://hh.ru/vacancy/{vacancy["id"]}')
        print('---')

# # КОД ИИ ABC+Класс
# from abc import ABC, abstractmethod
# import requests
#
#
# class Parser(ABC):
#     """
#     Абстрактный класс для работы с API сервисов с вакансиями.
#     Определяет общий интерфейс для парсеров вакансий.
#     """
#
#     @abstractmethod
#     def load_vacancies(self, keyword):
#         """
#         Абстрактный метод для загрузки вакансий по ключевому слову.
#         Должен быть реализован в каждом конкретном парсере.
#
#         :param keyword: ключевое слово для поиска вакансий
#         :return: список вакансий (структура зависит от API)
#         """
#         pass
#
#     @abstractmethod
#     def get_vacancies(self):
#         """
#         Абстрактный метод для получения списка загруженных вакансий.
#         Должен быть реализован в каждом конкретном парсере.
#
#         :return: список загруженных вакансий
#         """
#         pass
#
#
# class HH(Parser):
#     """
#     Класс для работы с API HeadHunter.
#     Реализует методы абстрактного класса Parser.
#     """
#
#     def __init__(self, file_worker):
#         self.url = 'https://api.hh.ru/vacancies'
#         self.headers = {'User-Agent': 'HH-User-Agent'}
#         self.params = {'text': '', 'page': 0, 'per_page': 100}
#         self.vacancies = []
#         super().__init__()
#         self.file_worker = file_worker  # сохраняем file_worker, если нужен
#
#     def load_vacancies(self, keyword):
#         """
#         Загружает вакансии с HH.ru по заданному ключевому слову.
#
#         :param keyword: ключевое слово для поиска
#         """
#         self.params['text'] = keyword
#         self.vacancies = []  # очищаем список перед новой загрузкой
#
#         while self.params.get('page') < 20:  # исправлено: было != 20
#             response = requests.get(self.url, headers=self.headers, params=self.params)
#
#             if response.status_code != 200:
#                 print(f"Ошибка при запросе: {response.status_code}")
#                 break
#
#             data = response.json()
#             vacancies = data.get('items', [])
#
#             if not vacancies:  # если вакансий больше нет
#                 break
#
#             self.vacancies.extend(vacancies)
#             self.params['page'] += 1
#
#     def get_vacancies(self):
#         """
#         Возвращает список загруженных вакансий.
#
#         :return: список вакансий
#         """
#         return self.vacancies


# # Код из ЗАДАНИЯ КУРСОВИКА
# import requests
#
#
# class HH(Parser):
#     """
#     Класс для работы с API HeadHunter
#     Класс Parser является родительским классом, который вам необходимо реализовать
#     """
#
#     def __init__(self, file_worker):
#         self.url = 'https://api.hh.ru/vacancies'
#         self.headers = {'User-Agent': 'HH-User-Agent'}
#         self.params = {'text': '', 'page': 0, 'per_page': 100}
#         self.vacancies = []
#         super().__init__(file_worker)
#
#     def load_vacancies(self, keyword):
#         self.params['text'] = keyword
#         while self.params.get('page') != 20:
#             response = requests.get(self.url, headers=self.headers, params=self.params)
#             vacancies = response.json()['items']
#             self.vacancies.extend(vacancies)
#             self.params['page'] += 1