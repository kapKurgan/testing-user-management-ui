import allure
from playwright.sync_api import Locator, Page, Error as PWError
# import logging
# logging.info(f"✅ Открыта страница: {url}")


def check_attr(locator: Locator, expected: str, page: Page, attr_name: str = "placeholder") -> None:
    """
        Универсальная проверка атрибута у поля.
        При ошибке делает скриншот и прикрепляет его к Allure-отчёту.
    """
    with allure.step(f'Проверить {attr_name} поля "{expected}"'):
        actual = locator.get_attribute(attr_name)
        if actual != expected:
            print(f"  ❌ Ожидаемый атрибут {attr_name} поля {expected} не соответствует фактическому: {expected}")
            allure.attach(
                page.screenshot(full_page=True),
                name=f"{attr_name} не соответствует {expected.lower()}",
                attachment_type=allure.attachment_type.PNG,
            )
            print(f"  📸 Сделан скриншот с ошибкой")
            raise AssertionError(
                f"Ожидаемый {attr_name}: {expected}, фактический: {actual}"
            )
        else:
            print(f"  ✅ Успешная проверка атрибута {attr_name} у поля: {expected}")


def check_text(locator: Locator, expected: str, page: Page) -> None:
    """
        Универсальная проверка текста у поля.
        При ошибке делает скриншот и прикрепляет его к Allure-отчёту.
    """
    with allure.step(f'Проверить название: "{expected}"'):
        actual = locator.text_content()
        if actual != expected:
            print(f"  ❌ Ожидаемое название: {actual} не соответствует фактическому: {expected}")
            allure.attach(
                page.screenshot(full_page=True),
                name=f"Название: {actual} не соответствует: {expected.lower()}",
                attachment_type=allure.attachment_type.PNG,
            )
            print(f"  📸 Сделан скриншот с ошибкой")
            raise AssertionError(
                f"Ожидаемое название: {expected}, фактическое: {actual}"
            )
        else:
            print(f"  ✅ Успешная проверка названия: {expected}")


def check_url(page: Page, expected: str) -> None:
    """
        Универсальная проверка текущего URL.
        При ошибке делает скриншот и прикрепляет его к Allure-отчёту.
    """
    with allure.step(f'Проверить URL: "{expected}"'):
        actual = page.url
        if actual != expected:
            print(f"  ❌ Ожидаемый URL: {expected} не соответствует фактическому: {actual}")
            allure.attach(
                page.screenshot(full_page=True),
                name=f"url_error_{expected.replace('/', '_').replace(':', '')}",
                attachment_type=allure.attachment_type.PNG,
            )
            print(f"  📸 Сделан скриншот с ошибкой")
            raise AssertionError(f"Ожидаемый URL: {expected}, фактический: {actual}")
        else:
            print(f"  ✅ Успешная проверка URL: {expected}")


def open_page(page: Page, url: str, *, wait_until: str = "load", timeout: int = 10_000) -> None:
    """
        Универсальный переход на страницу с allure-шагом и базовой обработкой ошибок.
    """
    with allure.step(f"Открыть страницу: {url}"):
        try:
            page.goto(url, wait_until=wait_until, timeout=timeout)
            print(f"  ✅ Открыта страница: {url}")
        except PWError as e:
            print(f"  ❌ Не удалось перейти на: {url}")
            # прикрепляем скриншот сразу
            allure.attach(
                page.screenshot(full_page=True),
                name=f"navigation_error_{url.replace('/', '_').replace(':', '')}",
                attachment_type=allure.attachment_type.PNG,
            )
            print(f"  📸 Сделан скриншот с ошибкой")
            raise AssertionError(f"Не удалось перейти на {url}: {e}") from e


def attach_screenshot(page: Page, name: str = "Скриншот"):
    """
        Прикрепляет скриншот страницы к Allure-отчету
    """
    page.wait_for_load_state('networkidle')
    screenshot = page.screenshot()
    allure.attach(screenshot, name=name, attachment_type=allure.attachment_type.PNG)
    print(f"  📸 Сделан: {name}")


def check_locator(locator: Locator, expected: str, page: Page) -> None:
    """
        Универсальная проверка локатора.
        При ошибке делает скриншот и прикрепляет его к Allure-отчёту.
    """
    test_locator = locator.is_visible()
    with allure.step(f'Проверить локатор для: "{expected}"'):
        if test_locator:
            print(f"  ✅ Успешная проверка локатора для: {expected}")
        else:
            print(f"  ❌ Локатор для: {expected} не обнаружен")
            assert test_locator, f"Локатор для: {expected} не обнаружен"