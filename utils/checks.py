import allure
from playwright.sync_api import Locator, Page, Error as PWError


def check_attr(locator: Locator, expected: str, page: Page, attr_name: str = "placeholder") -> None:
    """
        Универсальная проверка атрибута у поля.
        При ошибке делает скриншот и прикрепляет его к Allure-отчёту.
    """
    with allure.step(f'Проверить {attr_name} поля "{expected}"'):
        actual = locator.get_attribute(attr_name)
        if actual != expected:
            allure.attach(
                page.screenshot(full_page=True),
                name=f"{attr_name} не соответствует {expected.lower()}",
                attachment_type=allure.attachment_type.PNG,
            )
            raise AssertionError(
                f"Ожидаемый {attr_name}: {expected}, фактический: {actual}"
            )


def check_text(locator: Locator, expected: str, page: Page) -> None:
    """
        Универсальная проверка текста у поля.
        При ошибке делает скриншот и прикрепляет его к Allure-отчёту.
    """
    with allure.step(f'Проверить название: "{expected}"'):
        actual = locator.text_content()
        if actual != expected:
            allure.attach(
                page.screenshot(full_page=True),
                name=f"Название: {actual} не соответствует: {expected.lower()}",
                attachment_type=allure.attachment_type.PNG,
            )
            raise AssertionError(
                f"Ожидаемое название: {expected}, фактическое: {actual}"
            )


def check_url(page: Page, expected: str) -> None:
    """
        Универсальная проверка текущего URL.
        При ошибке делает скриншот и прикрепляет его к Allure-отчёту.
    """
    with allure.step(f'Проверить URL: "{expected}"'):
        actual = page.url
        if actual != expected:
            allure.attach(
                page.screenshot(full_page=True),
                name=f"url_error_{expected.replace('/', '_').replace(':', '')}",
                attachment_type=allure.attachment_type.PNG,
            )
            raise AssertionError(f"Ожидаемый URL: {expected}, фактический: {actual}")


def open_page(page: Page, url: str, *, wait_until: str = "load", timeout: int = 10_000) -> None:
    """
        Универсальный переход на страницу с allure-шагом и базовой обработкой ошибок.
    """
    with allure.step(f"Открыть страницу: {url}"):
        try:
            page.goto(url, wait_until=wait_until, timeout=timeout)
        except PWError as e:
            # прикрепляем скриншот сразу
            allure.attach(
                page.screenshot(full_page=True),
                name=f"navigation_error_{url.replace('/', '_').replace(':', '')}",
                attachment_type=allure.attachment_type.PNG,
            )
            raise AssertionError(f"Не удалось перейти на {url}: {e}") from e

def attach_screenshot(page: Page, name: str = "Скриншот"):
    """
        Прикрепляет скриншот страницы к Allure-отчету
    """
    screenshot = page.screenshot()
    allure.attach(screenshot, name=name, attachment_type=allure.attachment_type.PNG)
