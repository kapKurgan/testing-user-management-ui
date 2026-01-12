import allure
from playwright.sync_api import Locator, Page, expect, Error as PWError
# import logging
# logging.info(f"✅ Открыта страница: {url}")

def expect_visible(locator: Locator, name: str) -> None:
    """
        Нативный expect: элемент виден.
    """
    with allure.step(f'Проверить видимость элемента «{name}»'):
        expect(locator).to_be_visible()


def expect_text(locator: Locator, expected: str) -> None:
    """
        Нативный expect: точное совпадение текста.
    """
    with allure.step(f'Проверить текст элемента: «{expected}»'):
        expect(locator).to_have_text(expected)


def expect_attr(locator: Locator, attr: str, expected: str) -> None:
    """
        Нативный expect: значение атрибута.
    """
    with allure.step(f'Проверить атрибут {attr} = «{expected}»'):
        expect(locator).to_have_attribute(attr, expected)


def expect_url(page: Page, expected: str) -> None:
    """
        Нативный expect: URL страницы.
    """
    with allure.step(f'Проверить URL: «{expected}»'):
        expect(page).to_have_url(expected)


def expect_count(locator: Locator, count: int) -> None:
    """
        Нативный expect: количество элементов в списке.
    """
    with allure.step(f'Проверить количество элементов: {count}'):
        expect(locator).to_have_count(count)


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
    # page.wait_for_load_state('networkidle')
    screenshot = page.screenshot()
    allure.attach(screenshot, name=name, attachment_type=allure.attachment_type.PNG)
    print(f"  📸 Сделан: {name}")
