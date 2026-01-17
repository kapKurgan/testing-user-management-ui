# pytest --headed --slowmo 1000 -v --alluredir=reports/allure-results --html=reports/pytest_report.html --capture=tee-sys --self-contained-html
# allure serve reports/allure-results


import allure
import pytest
from playwright.sync_api import expect

from pages.site_pages import VALUE_BUTTON_LOGIN, LOGO_PAGE_PRODUCTS
from utils.read_data import read_test_data_json
from utils.checks import attach_screenshot, expect_visible

# [user, password, title, story, description, severity, tag]
login_date_positive = read_test_data_json("data_tests/login_date_positive.json")
login_date_negative = read_test_data_json("data_tests/login_date_negative.json")

def run_login_test(open_home_page, input_value: list) -> None:
    """
        Единый тест, покрывающий все 5 сценариев.
        Аннотации формируются из параметров.
    """
    user, password, title, description = input_value
    print(f"▶️ {title} - {description}")

    # динамические аннотации Allure
    allure.dynamic.title(title)
    allure.dynamic.description(description)
    # allure.dynamic.severity(getattr(allure.severity_level, severity))

    login_page = open_home_page
    with allure.step(f"Ввести учётные данные: {user} / {password}"):
        login_page.page_login(user, password)
    with allure.step(f"Нажать кнопку: {VALUE_BUTTON_LOGIN}"):
        login_page.button_login.click()


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
    @allure.story("Позитивный сценарий")
    @allure.tag("positive")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("input_value", login_date_positive)  # standard_user
    def test_login_positive(self, open_home_page, input_value: list) -> None:
        run_login_test(open_home_page, input_value)

        with allure.step(f'Проверить видимость элемента с текстом об ошибке'):
            expect(open_home_page.error_text).not_to_be_visible()
        with allure.step(f"Ошибки нет, проверяем переход на '{LOGO_PAGE_PRODUCTS}'"):
            open_home_page.page_products()
            attach_screenshot(open_home_page.page, f"Скриншот '{LOGO_PAGE_PRODUCTS}'")
        print(f"🏁 Тест окончен")


    @pytest.mark.order(2)
    @pytest.mark.regression
    @pytest.mark.negative
    @pytest.mark.login
    @pytest.mark.all
    @allure.story("Негативный сценарий")
    @allure.tag("negative")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.xfail(strict=True)
    @pytest.mark.parametrize("input_value", login_date_negative)
    def test_login_negative(self, open_home_page, input_value: list) -> None:
        run_login_test(open_home_page, input_value)

        expect_visible(open_home_page.error_text, open_home_page.error_text)
        actual_msg = open_home_page.error_text.locator('h3').text_content()
        print(f"  ⚠️ Ошибка: {actual_msg}")
        with allure.step(f"Появилось сообщение об ошибке: {actual_msg}"):
            attach_screenshot(open_home_page.page, "Скриншот с ошибкой")
        with allure.step(f"Проверяем переход на '{LOGO_PAGE_PRODUCTS}'"):
            open_home_page.page_products()

        print(f"🏁 Тест окончен")
