# Техническое задание: AQA Python

Полное развёртывание процесса автотестирования с нуля.

---

## Задача

Автоматизировать тестирование логина на сайте с использованием Python.
Тестовый стенд:
```bash
https://www.saucedemo.com/
```

---

### Написать **5 тестов**, проверяющих разные сценарии авторизации:

- Успешный логин (standard_user / secret_sauce)
- Логин с неверным паролем
- Логин заблокированного пользователя (locked_out_user)
- Логин с пустыми полями
- Логин пользователем performance_glitch_user (проверить корректный переход и что страница открывается несмотря на возможные задержки)

---

### Требования:

- Использовать Selenium или Playwright
- Использовать Page Object
- Подключить Allure
- Проверять корректность URL и отображение элементов
- Добавить Dockerfile для запуска тестов в контейнере
- Python 3.10
- Все зависимости — в requirements.txt
- Короткая инструкция по запуску — в README.md

---

## Дополнительно к заданию реализованы тесты с 'Бургер меню' на странице 'Products'

- Получение списков 'Названия' и 'Локаторы' кнопок в 'Бургер меню'
- Получение информации о сайте (пункт 'About' в 'Бургер меню') 

---

## Оглавление

- [Реализовано](#реализовано)
- [Начало работы](#начало-работы)
- [Docker](#docker)
- [CI/CD](#cicd)
- [URL отчетов GitHub Pages](#url-отчетов-github-pages)
- [Интеграция с GitHub Actions](#интеграция-с-github-actions)

---

## Реализовано

- проверка всех локаторов для используемых веб-элементов

### для фикстуры:

- проверка перехода на страницу. При ошибке делает скриншот и прикрепляет его к Allure-отчёту.
- проверка текущего URL. При ошибке делает скриншот и прикрепляет его к Allure-отчёту.
- проверка текста логотипа на стартовой странице. При ошибке делает скриншот и прикрепляет его к Allure-отчёту.

### для тестов:

- перед вводом логина/пароля проводится проверка placeholder. При ошибке делает скриншот и прикрепляет его к Allure-отчёту.
- тестовые данные хранятся в файле [login_date_positive.json](./data_tests/login_date_positive.json) в формате: 
```bash
[user, password, title, description]
```
- перед нажатием на кнопку **Login** проверить текст не ней. При ошибке делает скриншот и прикрепляет его к Allure-отчёту.
- делается проверка на ошибки при невалидном вводе **логин**/**пароль**. При ошибке делает скриншот и прикрепляет его к Allure-отчёту.
- при валидном вводе делается переход на страницу с товаром
- проверка текущего URL. При ошибке делает скриншот и прикрепляет его к Allure-отчёту.
- проверка текста логотипа на странице с товаром. При ошибке делает скриншот и прикрепляет его к Allure-отчёту.
- при успешном завершении теста делает скриншот и прикрепляет его к Allure-отчёту.

--- 

## Начало работы

### 1. Клонировать репозиторий

```bash
git clone https://github.com/kapKurgan/testing-user-management-ui.git
cd testing-user-management-ui
```

### 2. Создать виртуальную среду

#### Linux / MacOS

```bash
python3 -m venv venv
source venv/bin/activate
```

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Устанавить зависимости

```bash
pip install -r requirements.txt
```

### 4. Запуск тестов

```bash
pytest
```

- полная команда

```bash
pytest --headed --slowmo 1000 -v --alluredir=reports/allure-results --html=reports/pytest_report.html --capture=tee-sys --self-contained-html
```

- запуск по маркерам

```bash
pytest -m smoke		# критичные быстрые тесты
pytest -m regression	# полный набор тестов
pytest -m positive	# позитивные сценарии
pytest -m login		# тестирование логина
pytest -m all		# все тесты
pytest -m burger_menu	# тестирование 'Бургер меню'
```

### 5. Просмотр Allure отчетов

```bash
allure serve reports/allure-results
```

---

## Docker

В этом проекте реализован запуск тестов в контейнере. 

Конфигурацию можно найти в [Dockerfile](./Dockerfile).

### Команда: запустить сборку образа **aqa-py** на основе инструкций из **Dockerfile**

```bash
docker build -t aqa-py .
```

### Команда: создать новый контейнер из образа **aqa-py** и сразу запустить его

```bash
docker run --rm -p 8080:8080 -p 5252:5252 -v ${PWD}/reports:/app/reports aqa-py
```

Команда запускает изолированный контейнер с тестами, пробрасывает порты для доступа к HTML и Allure-отчётам, монтирует папку reports, а после остановки удаляет контейнер, оставляя только отчёты на хосте.

---

## CI/CD

В этом проекте включена интеграция с GitHub Actions. 

Конфигурации:
- автоматического запуска тестов в [ui-tests-auto.yml](./.github/workflows/ui-tests-auto.yml)
- ручного запуска тестов в [ui-tests-manual.yml](./.github/workflows/ui-tests-manual.yml)

Ручной запуск через интерфейс GitHub:
- [Перейдите в Actions > UI Tests manual > Run workflow](https://github.com/kapKurgan/testing-user-management-ui/actions/workflows/ui-tests-manual.yml)
- Выберите сценарий тестов (например, **-m login**)
- Нажмите **workflow**


---

## URL отчетов GitHub Pages

### HTML

```bash
https://kapKurgan.github.io/testing-user-management-ui/<run_id>/pytest-report.html
```

Например:
https://kapKurgan.github.io/testing-user-management-ui/21823455741/pytest_report.html

### ALLURE 

```bash
https://kapKurgan.github.io/testing-user-management-ui/<run_id>/allure-report/index.html
```

Например:
https://kapKurgan.github.io/testing-user-management-ui/21823455741/allure-report/index.html

---

## Требования
- Python 3.10
- GitHub account (для CI/CD и GitHub Pages)

--- 

## Интеграция с GitHub Actions

Workflow автоматически:
- Устанавливает Python 3.10
- Устанавливает зависимости
- Запускает тесты к реальному UI
- Генерирует HTML-отчеты
- Публикует отчеты в GitHub Pages

---
