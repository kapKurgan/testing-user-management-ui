# pytest --headed --slowmo 1000 -v --alluredir=reports/allure-results --html=reports/pytest_report.html --capture=tee-sys --self-contained-html
# allure serve reports/allure-results


import allure
import pytest
from locators.locators import VALUE_BUTTON_LOGIN, LOGO_PAGE_PRODUCTS
from utils.read_data import read_test_data_json
from utils.checks import attach_screenshot


# [user, password, title, story, description, severity, tag]
login_data = read_test_data_json("data_tests/login_date_positive.json")


def run_login_test(open_home_page, input_value: list) -> None:
    """
        Единый тест, покрывающий все 5 сценариев.
        Аннотации формируются из параметров.
    """
    user, password, title, story, description, severity, tag = input_value
    print(f"▶️ {story} - {title} - {description}")

    # динамические аннотации Allure
    allure.dynamic.story(story)
    allure.dynamic.title(title)
    allure.dynamic.description(description)
    allure.dynamic.severity(getattr(allure.severity_level, severity))
    allure.dynamic.tag(tag)

    login_page = open_home_page
    with allure.step(f"Ввести учётные данные: {user} / {password}"):
        login_page.page_login(user, password)

    with allure.step(f"Нажать кнопку: {VALUE_BUTTON_LOGIN}"):
        login_page.button_login.click()

    if login_page.error_text.is_visible():
        actual_msg = login_page.error_text.locator('h3').text_content()
        print(f"  ⚠️ Ошибка: {actual_msg}")
        with allure.step(f"Появилось сообщение об ошибке: {actual_msg}"):
            attach_screenshot(login_page.page, "Скриншот с ошибкой")
            # для негативных сценариев считаем ошибку ОК
            if tag == "negative":
                assert actual_msg, "Ожидали текст ошибки"
            else:
                pytest.fail(f"Не ожидали ошибку, но получили: {actual_msg}")
    else:
        with allure.step(f"Ошибки нет, проверяем переход на '{LOGO_PAGE_PRODUCTS}'"):
            login_page.page_products()
            attach_screenshot(login_page.page, f"Скриншот '{LOGO_PAGE_PRODUCTS}'")
    print(f"🏁 Тест окончен")


@allure.epic("Техническое задание: AQA Python")
@allure.feature("Авторизация на https://www.saucedemo.com")
class TestsLogin:
    """
        Параметризованные тесты логина с динамическими аннотациями Allure.
    """

    @pytest.mark.order(1)
    @pytest.mark.smoke
    @pytest.mark.positive
    @pytest.mark.login
    @pytest.mark.all
    @pytest.mark.parametrize("input_value", [login_data[0]])  # standard_user
    def test_login_smoke(self, open_home_page, input_value: list) -> None:
        run_login_test(open_home_page, input_value)

    @pytest.mark.order(2)
    @pytest.mark.regression
    @pytest.mark.login
    @pytest.mark.all
    @pytest.mark.parametrize("input_value", login_data[1:])
    def test_login_full(self, open_home_page, input_value: list) -> None:
        run_login_test(open_home_page, input_value)
