from playwright.sync_api import Page
from pytest_playwright.pytest_playwright import page
from utils.checks import check_attr, check_text, check_url


# page_login
BASE_URL = 'https://www.saucedemo.com/'
LOGO_PAGE_HOME = 'Swag Labs'
PLACEHOLDER_INPUT_USERNAME = 'Username'
PLACEHOLDER_INPUT_PASSWORD = 'Password'
VALUE_BUTTON_LOGIN = 'Login'
 # 'Epic sadface: Username and password do not match any user in this service' ('#login_button_container > div > form > div.error-message-container.error')
 # 'Epic sadface: Username is required'                                        ('#login_button_container > div > form > div.error-message-container.error')
 # 'Epic sadface: Sorry, this user has been locked out.'                       ('#login_button_container > div > form > div.error-message-container.error')

# page_products
PATH_PRODUCTS = 'inventory.html'
LOGO_PAGE_PRODUCTS = 'Products'


class Locators:
    def __init__(self, page: Page):
        self.page = page
        self.input_user_name = page.locator('#user-name')
        self.input_password = page.locator('#password')
        self.button_login = page.locator('#login-button')
        self.logo_url = page.locator('#root > div > div.login_logo')
        self.logo_product = page.locator('#header_container > div.header_secondary_container > span')
        self.error_text = page.locator('#login_button_container > div > form > div.error-message-container.error')


    def page_login(self, user_name: str, password: str):
        """
            Выполняет вход с заданными учетными данными.
        """
        check_attr(self.input_user_name, PLACEHOLDER_INPUT_USERNAME, self.page, "placeholder")
        check_attr(self.input_password, PLACEHOLDER_INPUT_PASSWORD, self.page, "placeholder")
        check_attr(self.button_login, VALUE_BUTTON_LOGIN, self.page, "value")

        self.input_user_name.fill(user_name)
        self.input_password.fill(password)

    def page_products(self):
        """
            Выполняет проверку перехода на страницу Products
        """
        check_url(self.page, BASE_URL + PATH_PRODUCTS)
        check_text(self.logo_product, LOGO_PAGE_PRODUCTS, self.page)
