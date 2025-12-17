import pytest
import json

# from pathlib import Path
from src.vacancy import Vacancy
from src.json_saver import JSONSaver


# === Тесты для JSONSaver::_load_existing_vacancies ===
# Создание фикстур для упрощения тестирования
@pytest.fixture
def temp_dir(tmp_path):
    """Временная директория для тестов."""
    return tmp_path


@pytest.fixture
def saver(temp_dir):
    """Экземпляр JSONSaver с путём во временной директории."""
    return JSONSaver(temp_dir / "vacancies.json")


def test_load_existing_vacancies_success(saver, temp_dir):
    """
    Проверяет успешную загрузку вакансий из корректного JSON‑файла.

    Сценарий теста:
    1. Создаётся тестовый JSON‑файл с двумя вакансиями в рабочей директории.
    2. Вызывается метод `_load_existing_vacancies()` для чтения данных.
    3. Проверяется:
       - количество загруженных объектов (должно быть 2);
       - тип каждого объекта (должен быть `Vacancy`);
       - корректность заполнения всех полей каждой вакансии:
         * название (`name`);
         * диапазоны зарплаты (`salary_from`, `salary_to`);
         * отсутствие валюты зарплаты (`salary_currency is None`);
         * URL вакансии (`url`);
         * описание вакансии (`description`).

    Аргументы:
        saver: экземпляр класса JSONSaver, используемый для загрузки данных.
        temp_dir: временная директория (фикстура), где создаётся тестовый файл.

    Ожидаемый результат:
        Метод возвращает список из двух объектов `Vacancy` с корректно заполненными полями.
    """
    # Создаём тестовый JSON‑файл
    test_data = [
        {
            "name": "Разработчик Python",
            "salary": {"from": 100000, "to": 150000},
            "url": "https://job1.com",
            "description": "Ищем Python‑разработчика",
        },
        {
            "name": "Frontend‑специалист",
            "salary": {"from": 80000, "to": 120000},
            "url": "https://job2.com",
            "description": "Верстка и JS",
        },
    ]
    with open(saver._filename, "w", encoding="utf-8") as f:
        json.dump(test_data, f, ensure_ascii=False, indent=2)

    # Выполняем загрузку
    result = saver._load_existing_vacancies()

    # Проверки
    assert len(result) == 2
    assert isinstance(result[0], Vacancy)
    assert result[0].name == "Разработчик Python"

    # Проверяем поля зарплаты отдельно (вместо result[0].salary)
    assert result[0].salary_from == 100000
    assert result[0].salary_to == 150000
    assert result[0].salary_currency is None  # Так как в JSON не указана валюта

    assert result[0].url == "https://job1.com"
    assert result[0].description == "Ищем Python‑разработчика"

    # Проверка второй вакансии
    assert result[1].name == "Frontend‑специалист"
    assert result[1].salary_from == 80000
    assert result[1].salary_to == 120000
    assert result[1].salary_currency is None
    assert result[1].url == "https://job2.com"
    assert result[1].description == "Верстка и JS"


def test_load_existing_vacancies_file_not_found(saver):
    """
    Проверяет, что метод _load_existing_vacancies возвращает пустой список,
    если файл с вакансиями не найден.

    Сценарий:
    - Вызывается метод _load_existing_vacancies экземпляра JSONSaver.
    - Файл, из которого должны загружаться вакансии, отсутствует на диске.

    Ожидаемый результат:
    - Метод возвращает пустой список ([]).
    - Тест успешно проходит проверку assert result == [].

    Аргументы:
        saver: экземпляр класса JSONSaver, используемый для тестирования.
    """
    result = saver._load_existing_vacancies()
    assert result == []


def test_load_existing_vacancies_invalid_json(saver, temp_dir):
    """
    Проверяет обработку файла с некорректным JSON при загрузке существующих вакансий.

    Сценарий:
    - Создаётся файл с синтаксической ошибкой в JSON (незакрытый объект).
    - Вызывается метод _load_existing_vacancies().
    - Ожидается, что метод корректно обработает ошибку и вернёт пустой список.

    Шаги:
    1. Записывает в файл заведомо некорректный JSON (пропущено значение после "salary":).
    2. Вызывает метод _load_existing_vacancies() у объекта saver.
    3. Проверяет, что результатом является пустой список (обработка ошибки прошла штатно).

    Ожидаемый результат:
    - Метод не выбрасывает исключение.
    - Возвращается пустой список [], что сигнализирует об ошибке чтения/парсинга.
    """
    # Создаём файл с некорректным JSON
    with open(saver._filename, "w", encoding="utf-8") as f:
        f.write('{"name": "Job", "salary": }')  # Незакрытый объект

    result = saver._load_existing_vacancies()
    assert result == []


def test_load_existing_vacancies_missing_fields(saver, temp_dir):
    """
    Проверяет корректность загрузки вакансий из JSON‑файла при отсутствии обязательных полей.

    Сценарий:
    - Создаётся JSON‑файл с вакансиями, у которых пропущены некоторые поля
      (например, `salary`, `description` или `name`).
    - Вызывается метод `_load_existing_vacancies()` для загрузки данных.
    - Проверяется, что:
      * все записи успешно загружены (количество совпадает);
      * отсутствующие поля заменяются значениями по умолчанию:
        - `name` → пустая строка `""`;
        - `description` → пустая строка `""`;
        - `salary_from` и `salary_to` → `0`;
        - `salary_currency` → `None`.

    Тестовые данные:
    1. Вакансия с отсутствующими `salary` и `description` (есть `name`, `url`).
    2. Вакансия с отсутствующим `name` (есть `url`, `description`).

    Ожидаемый результат:
    - Загружено 2 вакансии.
    - Все отсутствующие поля заполнены значениями по умолчанию.
    """
    test_data = [
        {"name": "Без зарплаты и описания", "url": "https://job3.com"},  # Нет salary, description
        {"url": "https://job4.com", "description": "Нет названия"},  # Нет name
    ]
    with open(saver._filename, "w", encoding="utf-8") as f:
        json.dump(test_data, f, ensure_ascii=False, indent=2)

    result = saver._load_existing_vacancies()

    assert len(result) == 2

    # Первая вакансия: есть name и url, нет salary и description
    assert result[0].name == "Без зарплаты и описания"
    assert result[0].url == "https://job3.com"
    assert result[0].description == ""  # По умолчанию
    assert result[0].salary_from == 0  # По дефолту при отсутствии salary
    assert result[0].salary_to == 0  # По дефолту
    assert result[0].salary_currency is None  # По дефолту

    # Вторая вакансия: нет name, есть url и description
    assert result[1].name == ""  # По умолчанию при отсутствии
    assert result[1].url == "https://job4.com"
    assert result[1].description == "Нет названия"
    assert result[1].salary_from == 0
    assert result[1].salary_to == 0
    assert result[1].salary_currency is None


def test_load_existing_vacancies_permission_error(saver, temp_dir, mocker):
    """
    Проверяет обработку ошибки доступа к файлу (PermissionError) в методе _load_existing_vacancies.

    Сценарий:
    - Мокируется встроенная функция `open` так, чтобы при попытке открытия файла
      возникала ошибка PermissionError («Нет доступа»).
    - Вызывается метод `_load_existing_vacancies` у объекта saver.
    - Проверяется, что метод корректно обрабатывает исключение и возвращает пустой список.

    Ожидаемое поведение:
    - При возникновении PermissionError метод должен:
      * не падать с необработанным исключением;
      * вернуть пустой список ([]), сигнализируя об отсутствии загруженных вакансий.

    Параметры:
    - saver: экземпляр класса JSONSaver, предоставляющий метод _load_existing_vacancies.
    - temp_dir: временный каталог (предоставляется фикстурой), используемый в контексте теста.
    - mocker: объект для мокирования (предоставляется фикстурой pytest-mock), позволяющий
      подменять поведение встроенных функций.

    Утверждения:
    - Результат вызова _load_existing_vacancies равен пустому списку ([]).
    """
    # Мокируем open, чтобы вызвать PermissionError
    mocker.patch("builtins.open", side_effect=PermissionError("Нет доступа"))

    result = saver._load_existing_vacancies()
    assert result == []


# === Тесты для JSONSaver::add_vacancies ===
# Создание фикстур для упрощения тестирования
@pytest.fixture
def existing_vacancies():
    return [
        Vacancy(name="Вакансия 1", url="url1", salary={"from": 100, "to": 200}, description="Описание вакансии 1"),
        Vacancy(name="Вакансия 2", url="url2", salary={"from": 300, "to": 400}, description="Описание вакансии 2"),
    ]


@pytest.fixture
def new_vacancies():
    return [
        Vacancy(name="Вакансия 3", url="url3", salary={"from": 500, "to": 600}, description="Описание вакансии 3"),
        Vacancy(name="Вакансия 4", url="url4", salary={"from": 700, "to": 800}, description="Описание вакансии 4"),
    ]


@pytest.fixture
def duplicate_vacancy():
    return Vacancy(name="Вакансия 1", url="url1", salary={"from": 100, "to": 200}, description="Описание вакансии 1")


def test_add_vacancies_no_duplicates(existing_vacancies, new_vacancies):
    """
    Проверяет корректность добавления новых вакансий в случае, когда нет дубликатов.

    Сценарий:
    - Имеется набор существующих вакансий (existing_vacancies).
    - Поступает набор новых вакансий (new_vacancies), ни одна из которых
      не является дубликатом существующих.
    - Ожидаем, что все новые вакансии будут добавлены, а общее количество
      вакансий станет равным сумме существующих и новых.

    Параметры:
        existing_vacancies (list[Vacancy]): список существующих объектов вакансий.
        new_vacancies (list[dict]): список новых вакансий в виде словарей.

    Шаги теста:
        1. Создаётся экземпляр JSONSaver.
        2. Метод _load_existing_vacancies подменяется лямбдой, возвращающей
           existing_vacancies.
        3. Вызывается метод add_vacancies с new_vacancies.
        4. Проверяется, что:
           - итоговое количество вакансий равно 4 (сумма существующих и новых);
           - все исходные и новые вакансии присутствуют в результате.

    Ожидаемый результат:
        - Метод возвращает объединённый список без потери данных.
        - Ни одна вакансия не отфильтрована как дубликат.
    """
    saver = JSONSaver()
    saver._load_existing_vacancies = lambda: existing_vacancies
    result = saver.add_vacancies(new_vacancies)

    assert len(result) == 4
    assert all(vac in result for vac in existing_vacancies + new_vacancies)


def test_add_vacancies_with_duplicates(existing_vacancies, duplicate_vacancy):
    """
    Проверяет поведение метода add_vacancies при добавлении вакансий-дубликатов.

    Сценарий:
    - Имеется список существующих вакансий (existing_vacancies).
    - Пытаемся добавить вакансию (duplicate_vacancy), которая является дубликатом одной из существующих.
    - Ожидается, что дубликат не будет добавлен в итоговый список.

    Условия теста:
    - JSONSaver инициализируется и настраивается так, чтобы возвращать существующие вакансии
      через _load_existing_vacancies.
    - В метод add_vacancies передаётся список из одной вакансии-дубликата.

    Ожидаемый результат:
    - Длина возвращаемого списка равна 2 (исходные вакансии без изменений).
    - Переданная вакансия-дубликат отсутствует в итоговом списке.

    Параметры:
        existing_vacancies (list[Vacancy]): список существующих объектов вакансий,
            используемый для имитации загруженных данных.
        duplicate_vacancy (dict): словарь с данными вакансии, являющейся
            дубликатом одной из существующих.

    Проверки:
        - assert len(result) == 2: проверяет, что количество вакансий
          в результате соответствует исходному (дубликат не добавлен).
        - assert duplicate_vacancy not in result: убеждается, что
          конкретная вакансия-дубликат отсутствует в итоговом списке.
    """
    saver = JSONSaver()
    saver._load_existing_vacancies = lambda: existing_vacancies

    result = saver.add_vacancies([duplicate_vacancy])

    assert len(result) == 2
    assert duplicate_vacancy not in result


def test_add_vacancies_empty_existing(new_vacancies):
    """
    Проверяет добавление вакансий в ситуацию, когда существующих вакансий нет (пустой файл/отсутствие данных).

    Сценарий:
    - Инициализируется JSONSaver.
    - Имитируется отсутствие существующих вакансий (метод _load_existing_vacancies возвращает пустой список).
    - В систему добавляются новые вакансии.

    Ожидаемое поведение:
    - Результат должен содержать ровно те вакансии, которые были переданы в add_vacancies.
    - Все новые вакансии должны присутствовать в итоговом списке.
    - Длина итогового списка должна совпадать с длиной списка новых вакансий.

    Параметры:
    new_vacancies (list[Vacancy]): список новых вакансий для добавления (предоставляется через фикстуру).

    Проверки:
    1. Длина результирующего списка равна длине списка новых вакансий.
    2. Каждая вакансия из new_vacancies присутствует в результате.
    """
    saver = JSONSaver()
    saver._load_existing_vacancies = lambda: []
    result = saver.add_vacancies(new_vacancies)

    assert len(result) == len(new_vacancies)
    assert all(vac in result for vac in new_vacancies)


def test_add_vacancies_empty_new(existing_vacancies):
    """
    Проверяет поведение метода add_vacancies при передаче пустого списка новых вакансий.

    Сценарий:
    - Инициализируется экземпляр JSONSaver.
    - Имитируется наличие существующих вакансий (метод _load_existing_vacancies возвращает предопределённый список).
    - В метод add_vacancies передаётся пустой список (нет новых вакансий для добавления).

    Ожидаемое поведение:
    - Результат должен полностью совпадать с существующим списком вакансий.
    - Длина итогового списка должна быть равна длине списка существующих вакансий.
    - Все существующие вакансии должны присутствовать в результате без изменений.
    - Новые вакансии не должны появиться в результате (так как входной список пуст).

    Параметры:
    existing_vacancies (list[Vacancy]): список существующих вакансий (предоставляется через фикстуру).

    Проверки:
    1. Длина результирующего списка равна длине списка существующих вакансий.
    2. Каждая вакансия из existing_vacancies присутствует в результате.
    3. В результате отсутствуют какие-либо дополнительные вакансии.
    """
    saver = JSONSaver()
    saver._load_existing_vacancies = lambda: existing_vacancies
    result = saver.add_vacancies([])

    assert len(result) == len(existing_vacancies)
    assert all(vac in result for vac in existing_vacancies)


# === Тесты для JSONSaver::save_vacancies_to_json ===
# Создание тестовых объектов Vacancy
def create_test_vacancies():
    """
    Создаёт список тестовых объектов Vacancy для использования в юнит‑тестах.

    Возвращает заранее определённый набор вакансий с реалистичными данными:
    - название позиции;
    - диапазон зарплаты и валюта;
    - URL вакансии;
    - краткое описание обязанностей.

    Returns:
        list[Vacancy]: Список из двух объектов Vacancy:
            1. Разработчик Python (зарплата 100000–150000 RUB)
            2. Frontend‑специалист (зарплата 80000–120000 RUB)
    """
    return [
        Vacancy(
            name="Разработчик Python",
            salary={"from": 100000, "to": 150000, "currency": "RUB"},
            url="https://job1.com",
            description="Ищем Python-разработчика",
        ),
        Vacancy(
            name="Frontend-специалист",
            salary={"from": 80000, "to": 120000, "currency": "RUB"},
            url="https://job2.com",
            description="Верстка и JS",
        ),
    ]


# Фикстура для временного файла
@pytest.fixture
def temp_file(tmp_path):
    return tmp_path / "test_vacancies.json"


# Тест на сохранение списка вакансий
def test_save_vacancies_to_json(temp_file):
    """
    Тестирует сохранение списка вакансий в JSON‑файл через класс JSONSaver.

    Сценарий:
    1. Создаётся экземпляр JSONSaver с временным файлом.
    2. Генерируются тестовые вакансии (через вспомогательную функцию).
    3. Вакансии сохраняются в файл методом save_vacancies_to_json.
    4. Файл читается обратно, данные десериализуются из JSON.
    5. Содержимое файла сравнивается с ожидаемым словарём.

    Проверяется:
    - Корректность записи данных в файл.
    - Соответствие структуры сохранённых данных ожидаемому формату:
      * наличие полей name, salary, url, description;
      * правильная вложенность словаря salary (from, to, currency);
      * сохранение точных значений (суммы, URL, описания).

    Аргументы:
        temp_file (str): путь к временному файлу, предоставляемый фикстурой,
            куда будут записаны данные.

    Ожидаемый результат:
        Сохранённые в файл данные полностью совпадают с ожидаемым списком словарей.
        Тест проходит, если assert data == expected_data не вызывает исключение.
    """
    saver = JSONSaver(temp_file)
    vacancies = create_test_vacancies()
    saver.save_vacancies_to_json(vacancies)

    # Проверка содержимого файла
    with open(temp_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Сравнение с ожидаемыми данными
    expected_data = [
        {
            "name": "Разработчик Python",
            "salary": {"from": 100000, "to": 150000, "currency": "RUB"},
            "url": "https://job1.com",
            "description": "Ищем Python-разработчика",
        },
        {
            "name": "Frontend-специалист",
            "salary": {"from": 80000, "to": 120000, "currency": "RUB"},
            "url": "https://job2.com",
            "description": "Верстка и JS",
        },
    ]

    assert data == expected_data


# Тест на сохранение пустого списка
def test_save_empty_list(temp_file):
    """
    Проверяет корректность сохранения пустого списка вакансий в JSON‑файл.

    Сценарий теста:
    1. Создаётся экземпляр JSONSaver с временным файлом.
    2. Вызывается метод save_vacancies_to_json с пустым списком.
    3. Проверяется:
       - факт создания файла;
       - что содержимое файла — валидный JSON, представляющий пустой массив [];
       - текстовое представление файла точно равно "[]" (без лишних пробелов/символов).

    Аргументы:
        temp_file (pathlib.Path): временный файл для тестирования,
            предоставляется через фикстуру.

    Проверки:
        - Файл успешно создан (exists()).
        - При чтении через json.load получается пустой список [].
        - Текстовое содержимое файла строго равно "[]" (после strip).

    Ожидаемый результат:
        Все утверждения (assert) проходят, файл содержит ровно "[]".
    """
    saver = JSONSaver(temp_file)

    # Вызываем метод с пустым списком
    saver.save_vacancies_to_json([])

    # Проверяем, что файл создан
    assert temp_file.exists(), f"Файл {temp_file} не был создан"

    # Проверяем содержимое файла (все операции внутри with)
    with open(temp_file, "r", encoding="utf-8") as f:
        # Читаем данные через json.load
        data = json.load(f)
        assert data == [], "Содержимое файла должно быть пустым JSON-массивом []"

        # Возвращаемся к началу файла и читаем как текст
        f.seek(0)  # Перемещаем курсор в начало файла
        content = f.read().strip()
        assert content == "[]", "Файл должен содержать только '[]'"


# Тест на сохранение одной вакансии
def test_save_single_vacancy(temp_file):
    """
    Тест сохранения одной вакансии в JSON‑файл.

    Проверяет, что метод save_vacancies_to_json корректно:
    - записывает единственную вакансию в файл;
    - формирует JSON‑структуру с ожидаемыми полями;
    - сохраняет все ключевые атрибуты вакансии (название, зарплату, URL, описание).

    Сценарий:
    1. Создаётся экземпляр JSONSaver с временным файлом.
    2. Берётся первая вакансия из тестовых данных.
    3. Вакансия сохраняется через save_vacancies_to_json.
    4. Файл читается и сравнивается с ожидаемым JSON‑объектом.

    Ожидаемый результат:
    Содержимое файла полностью совпадает с expected_data — список из одного словаря
    с корректными значениями полей name, salary, url и description.

    Аргументы:
        temp_file (str): путь к временному файлу для тестирования (предоставляется фикстурой).
    """
    saver = JSONSaver(temp_file)

    # Берём первую вакансию из тестовых данных
    vacancies = [create_test_vacancies()[0]]

    saver.save_vacancies_to_json(vacancies)

    # Проверка содержимого файла
    with open(temp_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    expected_data = [
        {
            "name": "Разработчик Python",
            "salary": {"from": 100000, "to": 150000, "currency": "RUB"},
            "url": "https://job1.com",
            "description": "Ищем Python-разработчика",
        }
    ]

    assert data == expected_data


# Тест на сохранение вакансий с отсутствующими полями
def test_save_vacancies_with_missing_fields(temp_file):
    """
    Проверяет сохранение вакансий с отсутствующими полями (в частности, salary=None) в JSON‑файл.

    Сценарий:
    - Создаётся экземпляр JSONSaver с временным файлом.
    - Формируется список из одной вакансии, где salary=None.
    - Вызывается метод save_vacancies_to_json для сохранения данных.
    - Содержимое файла считывается и сравнивается с ожидаемым результатом.

    Ожидаемое поведение:
    - Поле salary=None должно быть преобразовано в словарь с дефолтными значениями:
      {"from": 0, "to": 0, "currency": None}.
    - Все остальные поля (name, url, description) сохраняются без изменений.
    - Данные в файле соответствуют ожидаемой структуре.

    Аргументы:
        temp_file (str): путь к временному файлу для тестирования (предоставляется фикстурой).

    Проверки:
        - Сохранённые данные полностью совпадают с expected_data.
    """
    saver = JSONSaver(temp_file)
    vacancies = [
        Vacancy(name="Вакансия без зарплаты", salary=None, url="https://job3.com", description="Без указания зарплаты")
    ]
    saver.save_vacancies_to_json(vacancies)

    # Проверка содержимого файла
    with open(temp_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    expected_data = [
        {
            "name": "Вакансия без зарплаты",
            "salary": {"from": 0, "to": 0, "currency": None},
            "url": "https://job3.com",
            "description": "Без указания зарплаты",
        }
    ]

    assert data == expected_data
