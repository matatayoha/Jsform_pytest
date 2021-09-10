
import pytest
import allure
from libs.pages.login_page import LoginPage


@allure.story('Login')
class TestLogin:
    """TestLogin"""

    @pytest.fixture(scope="class", autouse="true")
    def setup_class(self, init):
        self = self.__class__
        self.driver, self.config = init
        self.login_page = LoginPage(self.driver, self.config)

    def setup(self):
        self.login_page.open()
        self.login_page.accept_use_of_cookie()
        self.login_page.change_language()

    @allure.title("Verify login by email successfully")
    @allure.description("""
        Steps:
            1. Open the login page
            2. Fill in fields with email and password
            3. Fill in the image verification code field
            4. Click the sign in button
        Expected:
            1. Login success
            2. Go to the home page
        """)
    def test_login_by_email(self):
        self.login_page.login(self.config["user_email"], self.config["password"])


