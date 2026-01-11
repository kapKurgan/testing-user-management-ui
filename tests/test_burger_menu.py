import allure
import pytest
from playwright.sync_api import expect

from locators.locators import LOGO_PAGE_PRODUCTS, VALUE_BUTTON_LOGIN
from utils.checks import check_locator, attach_screenshot

def _open_burger_menu(login_page):
    """
        Открывает бургер-меню и возвращает список кнопок.
    """
    check_locator(login_page.button_product_bm_open, "Кнопка 'Открыть бургер меню'", login_page.page)
    with allure.step("Нажать кнопку: 'Открыть бургер меню'"):
        login_page.button_product_bm_open.click()
    return login_page.buttons_product_bm_list


def _collect_button_data(buttons_product_bm_list):
    """
        Собирает названия и локаторы кнопок бургер-меню.
    """
    with allure.step("Cобрать названия всех кнопок 'Бургер меню' в список"):
        buttons_list = buttons_product_bm_list.all_inner_texts()
        assert len(buttons_list) == 4, f"Неверное количество кнопок в 'бургер меню' -> ожидалось: 4, получено: {len(buttons_list)}"
        with allure.step(f"Получен список с названиями кнопок в 'Бургер меню': {buttons_list}"):
            print("    🍔 Список с названиями кнопок в 'Бургер меню':", buttons_list)
    with allure.step("Cобрать локаторы всех кнопок 'Бургер меню' в список"):
        buttons_product_bm_list_locator = [buttons_product_bm_list.nth(i).get_attribute("id") for i in range(buttons_product_bm_list.count())]
        assert len(buttons_product_bm_list_locator) == 4, f"Неверное количество кнопок в 'бургер меню' -> ожидалось: 4, получено: {len(buttons_product_bm_list_locator)}"
        with allure.step(f"Получен список с локаторами кнопок в 'Бургер меню': {buttons_product_bm_list_locator}"):
            print("    🍔 Список с локаторами кнопок в 'Бургер меню':", buttons_product_bm_list_locator)
    return buttons_list, buttons_product_bm_list_locator


def _login_and_navigate_to_products(login_page, user: str = "standard_user", pwd: str = "secret_sauce"):
    """
        Выполняет логин и переход на страницу Products.
    """
    login_page.page_login(user, pwd)
    with allure.step(f"Нажать кнопку: {VALUE_BUTTON_LOGIN}"):
        login_page.button_login.click()


def _close_burger_menu(login_page):
    """
        Закрывает бургер-меню.
    """
    check_locator(login_page.button_product_bm_close, "Кнопка 'Закрыть бургер меню'", login_page.page)
    with allure.step("Нажать кнопку: 'Закрыть бургер меню'"):
        login_page.button_product_bm_close.click()



@pytest.mark.order(3)
@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.burger_menu
@pytest.mark.all
@allure.epic("Дополнительно к техническому заданию: AQA Python")
@allure.feature(f"Тестирование 'Бургер меню' на странице '{LOGO_PAGE_PRODUCTS}'")
@allure.story("Позитивный сценарий")
@allure.title("Получение списков 'Названия' и 'Локаторы' кнопок в 'Бургер меню'")
@allure.tag("positive")
@allure.description("Получение списков 'Названия' и 'Локаторы' кнопок в 'Бургер меню'")
def test_burger_menu(open_home_page) -> None:

    print("▶️ Позитивный сценарий - Получение списков 'Названия' и 'Локаторы' кнопок в 'Бургер меню'")

    login_page = open_home_page
    _login_and_navigate_to_products(login_page)

    buttons_list = _open_burger_menu(login_page)
    _collect_button_data(buttons_list)

    with allure.step(f"Сделать скриншот 'бургер меню' на странице '{LOGO_PAGE_PRODUCTS}'"):
        login_page.page.wait_for_load_state('networkidle')
        attach_screenshot(login_page.page, f"Скриншот 'бургер меню' на странице '{LOGO_PAGE_PRODUCTS}'")

    _close_burger_menu(login_page)

    expect(login_page.button_product_bm_close).not_to_be_visible(timeout=5000)
    attach_screenshot(login_page.page, f"Скриншот: Тест 'Бургер меню' окончен")
    print(f"🏁 Тест окончен")


@pytest.mark.order(4)
@pytest.mark.regression
@pytest.mark.positive
@pytest.mark.burger_menu
@pytest.mark.all
@allure.epic("Дополнительно к техническому заданию: AQA Python")
@allure.feature(f"Тестирование 'Бургер меню' на странице '{LOGO_PAGE_PRODUCTS}'")
@allure.story("Позитивный сценарий")
@allure.title("Получение информации о сайте (пункт 'About' в 'Бургер меню')")
@allure.tag("positive")
@allure.description("Получение информации о сайте (пункт 'About' в 'Бургер меню')")
def test_burger_menu_about(open_home_page) -> None:

    print("▶️ Позитивный сценарий - Получение информации о сайте (пункт 'About' в 'Бургер меню')")

    login_page = open_home_page
    _login_and_navigate_to_products(login_page)

    buttons_list = _open_burger_menu(login_page)
    _, buttons_product_bm_list_locator = _collect_button_data(buttons_list)

    login_page.page.locator(f"#{buttons_product_bm_list_locator[1]}").click()

    with allure.step("Сделать скриншот информация о сайте (пункт 'About' в 'Бургер меню')"):
        attach_screenshot(login_page.page, "Скриншот информация о сайте (пункт 'About' в 'Бургер меню')")

    print(f"🏁 Тест окончен")
