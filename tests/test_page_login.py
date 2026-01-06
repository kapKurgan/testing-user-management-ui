# pytest --headed --slowmo 1000 -v --alluredir=reports/allure-results --html=reports/pytest_report.html --capture=tee-sys --self-contained-html
# allure serve reports/allure-results


import allure
import pytest
from locators.locators import VALUE_BUTTON_LOGIN
from utils.read_data import read_test_data_json
from utils.checks import attach_screenshot


# [user, password, title, story, description, severity, tag]
login_data = read_test_data_json("data_tests/login_date_positive.json")


@allure.epic("Техническое задание: AQA Python")
@allure.feature("Авторизация на https://www.saucedemo.com")
class TestsLogin:
    """
        Параметризованные тесты логина с динамическими аннотациями Allure.
    """

    @pytest.mark.parametrize("input_value", login_data)
    def test_login(self, open_home_page, input_value: list) -> None:
        """
            Единый тест, покрывающий все 5 сценариев.
            Аннотации формируются из параметров.
        """
        user, password, title, story, description, severity, tag = input_value

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
            with allure.step(f"Появилось сообщение об ошибке: {actual_msg}"):
                attach_screenshot(login_page.page, "Скриншот с ошибкой")
                # для негативных сценариев считаем ошибку ОК
                if tag == "negative":
                    assert actual_msg, "Ожидали текст ошибки"
                else:
                    pytest.fail(f"Не ожидали ошибку, но получили: {actual_msg}")
        else:
            with allure.step("Ошибки нет, проверяем переход на Products"):
                login_page.page_products()
                attach_screenshot(login_page.page, "Скриншот Products")