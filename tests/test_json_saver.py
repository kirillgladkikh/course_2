import pytest
import json
from pathlib import Path
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
    """Проверяет загрузку корректного JSON‑файла с вакансиями."""
    # Создаём тестовый JSON‑файл
    test_data = [
        {
            "name": "Разработчик Python",
            "salary": {"from": 100000, "to": 150000},
            "url": "https://job1.com",
            "description": "Ищем Python‑разработчика"
        },
        {
            "name": "Frontend‑специалист",
            "salary": {"from": 80000, "to": 120000},
            "url": "https://job2.com",
            "description": "Верстка и JS"
        }
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
    """Проверяет возврат пустого списка, если файла не существует."""
    result = saver._load_existing_vacancies()
    assert result == []

def test_load_existing_vacancies_invalid_json(saver, temp_dir):
    """Проверяет обработку некорректного JSON (синтаксическая ошибка)."""
    # Создаём файл с некорректным JSON
    with open(saver._filename, "w", encoding="utf-8") as f:
        f.write('{"name": "Job", "salary": }')  # Незакрытый объект

    result = saver._load_existing_vacancies()
    assert result == []


def test_load_existing_vacancies_missing_fields(saver, temp_dir):
    """Проверяет загрузку JSON с отсутствующими полями (используются значения по умолчанию)."""
    test_data = [
        {"name": "Без зарплаты и описания", "url": "https://job3.com"},  # Нет salary, description
        {"url": "https://job4.com", "description": "Нет названия"}  # Нет name
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
    assert result[0].salary_to == 0   # По дефолту
    assert result[0].salary_currency is None  # По дефолту


    # Вторая вакансия: нет name, есть url и description
    assert result[1].name == ""  # По умолчанию при отсутствии
    assert result[1].url == "https://job4.com"
    assert result[1].description == "Нет названия"
    assert result[1].salary_from == 0
    assert result[1].salary_to == 0
    assert result[1].salary_currency is None


def test_load_existing_vacancies_permission_error(saver, temp_dir, mocker):
    """Проверяет обработку ошибки доступа к файлу (PermissionError)."""
    # Мокируем open, чтобы вызвать PermissionError
    mocker.patch("builtins.open", side_effect=PermissionError("Нет доступа"))


    result = saver._load_existing_vacancies()
    assert result == []


# === Тесты для JSONSaver::add_vacancies ===
# Создание фикстур для упрощения тестирования
@pytest.fixture
def existing_vacancies():
    return [
        Vacancy(
            name="Вакансия 1",
            url="url1",
            salary={"from": 100, "to": 200},
            description="Описание вакансии 1"
        ),
        Vacancy(
            name="Вакансия 2",
            url="url2",
            salary={"from": 300, "to": 400},
            description="Описание вакансии 2"
        ),
    ]

@pytest.fixture
def new_vacancies():
    return [
        Vacancy(
            name="Вакансия 3",
            url="url3",
            salary={"from": 500, "to": 600},
            description="Описание вакансии 3"
        ),
        Vacancy(
            name="Вакансия 4",
            url="url4",
            salary={"from": 700, "to": 800},
            description="Описание вакансии 4"
        ),
    ]

@pytest.fixture
def duplicate_vacancy():
    return Vacancy(
        name="Вакансия 1",
        url="url1",
        salary={"from": 100, "to": 200},
        description="Описание вакансии 1"
    )

def test_add_vacancies_no_duplicates(existing_vacancies, new_vacancies):
    """Проверяет добавление новых вакансий без дубликатов."""
    saver = JSONSaver()
    saver._load_existing_vacancies = lambda: existing_vacancies
    result = saver.add_vacancies(new_vacancies)


    assert len(result) == 4
    assert all(vac in result for vac in existing_vacancies + new_vacancies)


def test_add_vacancies_with_duplicates(existing_vacancies, duplicate_vacancy):
    """Проверяет обработку дубликатов."""
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
    return [
        Vacancy(
            name="Разработчик Python",
            salary={"from": 100000, "to": 150000, "currency": "RUB"},
            url="https://job1.com",
            description="Ищем Python-разработчика"
        ),
        Vacancy(
            name="Frontend-специалист",
            salary={"from": 80000, "to": 120000, "currency": "RUB"},
            url="https://job2.com",
            description="Верстка и JS"
        )
    ]

# Фикстура для временного файла
@pytest.fixture
def temp_file(tmp_path):
    return tmp_path / "test_vacancies.json"

# Тест на сохранение списка вакансий
def test_save_vacancies_to_json(temp_file):
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
            "description": "Ищем Python-разработчика"
        },
        {
            "name": "Frontend-специалист",
            "salary": {"from": 80000, "to": 120000, "currency": "RUB"},
            "url": "https://job2.com",
            "description": "Верстка и JS"
        }
    ]

    assert data == expected_data

# Тест на сохранение пустого списка
def test_save_empty_list(temp_file):
    """Тест на сохранение пустого списка вакансий в JSON-файл."""
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
    """Тест на сохранение одной вакансии."""
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
            "description": "Ищем Python-разработчика"
        }
    ]

    assert data == expected_data


# Тест на сохранение вакансий с отсутствующими полями
def test_save_vacancies_with_missing_fields(temp_file):
    saver = JSONSaver(temp_file)
    vacancies = [
        Vacancy(
            name="Вакансия без зарплаты",
            salary=None,
            url="https://job3.com",
            description="Без указания зарплаты"
        )
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
            "description": "Без указания зарплаты"
        }
    ]

    assert data == expected_data
