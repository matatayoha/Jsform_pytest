from poium.common import logging
from libs.common.base_page import BasePage, Element
import allure
from libs.utils.random_util import RandomUtil


class LoginPage(BasePage):
    """
    Login Page
    """

    accept_btn = Element(css=r'div.btn button', describe="accept use of cookie button")
    user_name_input = Element(css=r'input[placeholder="Please enter your email address or user name"]',
                              describe="user name input box")
    password_input = Element(css=r'div[class="login-box"] input[placeholder="Please enter your password"]',
                             describe="password input box")
    captcha_input = Element(css=r'div[class="login-box"] div.verification-box input',
                            describe="verification code input box")
    captcha = Element(css=r'div[class="login-box"] div.verification-identify img', describe="captcha")
    submit_btn = Element(css=r'div[class="login-box"] div.btn-login', describe="login button")
    register_btn = Element(css=r'div[class="login-box"] div.btn-register', describe="register button")
    forgot_password = Element(css=r'div.remember-pwd div', describe="forgot password link")
    login_page = Element(css=r'#app > div > div:nth-child(4)', describe="login page")
    cookie_banner = Element(css=r'body > div:nth-child(10) > div.ivu-modal-wrap', describe="cookie banner page")
    privacy_policy_link = Element(css=r'p:nth-child(1) > span:nth-child(4)', describe="Privacy Policy link")
    privacy_policy_page = Element(css=r'body > div:nth-child(8) > div.vertical-center-modal .ivu-modal-body'
                                  , describe="Privacy Policy page")
    imprint_link = Element(css=r'p.body-link > a:nth-child(2)', describe="Imprint link")
    cookie_settings_link = Element(css=r'div.footer > div.footera > a', describe="View and change cookie settings link")
    cookie_settings_page = Element(css=r'.ModelSetCookies2 > div.ivu-modal-wrap',
                                   describe="View and change cookie settings page")
    confirm_selection = Element(css=r'.ModelSetCookies2 button', describe="confirm selection button")
    technically_required_cookie_checkbox = Element(css=r'.ivu-checkbox-disabled > input',
                                                   describe="Technically required cookie checkbox")
    marketing_cookies_checkbox = Element(css=r'#body-content > div:nth-child(2) > label',
                                         describe="Performance & marketing cookies checkbox")
    terms_of_use_link = Element(css=r'.site-terms span:nth-child(5)', describe="terms of use link")
    terms_of_use_page = Element(css=r'body > div:nth-child(9) > .vertical-center-modal .ivu-modal-body',
                                describe="terms of use link page")

    @allure.step("Get the picture verification code source url")
    def get_verification_picture_url(self):
        """
        Get the picture verification code source url
        """
        return self.captcha.get_attribute("src")

    @allure.step("Open the login page")
    def open(self):
        """
        Open the login page
        """
        self.get("#/")

    @allure.step("Login the website")
    def login(self, user_name, password):
        """
        Login the website
        """
        self.user_name_input.input(user_name)
        self.password_input.input(password)
        self.submit_captcha()

    @allure.step("Open the home page and login an user")
    def open_and_login(self, user_name, password):
        """
        Open the home page and login an user
        """
        self.open()
        self.accept_use_of_cookie()
        self.change_language()
        self.login(user_name, password)

    @allure.step("Click the 'forgot password?' link to find password page")
    def goto_password_page(self):
        """
        Click the "forgot password?" link to find password page
        """
        self.forgot_password.move_to_element()
        self.forgot_password.click()

    @allure.step("click the 'create account' link to register")
    def goto_register_page(self):
        """
        click the "create account" link to register
        """
        js = "$('#app > div > div:nth-child(4) > form > div.btn-register.btn-default').click()"
        self.driver.execute_script(js)

    @allure.step("Username input  is required")
    def user_name_input_required(self):
        """
        Username input  is required
        """
        self.swipe_down_screen(1000)
        self.submit_btn.click()

    @allure.step("Password input is required")
    def password_input_required(self, user_name):
        """
        Password input is required
        """
        self.user_name_input.input(user_name)
        self.swipe_down_screen(1000)
        self.submit_btn.click()

    @allure.step("Captcha input is required")
    def captcha_input_required(self, user_name, password):
        """
        Captcha input is required
        """
        self.user_name_input.input(user_name)
        self.password_input.input(password)
        self.swipe_down_screen(1000)
        self.submit_btn.click()

    @allure.step("Format of captcha input is required")
    def captcha_invalid(self, user_name, password, captcha):
        """
        Format of captcha input is required
        """
        self.user_name_input.input(user_name)
        self.password_input.input(password)
        self.captcha_input.input(captcha)
        self.swipe_down_screen(1000)
        self.submit_btn.click()

    @allure.step("Get all the content")
    def get_text(self, text):
        """
        Get all the content about cookie banner etc.
        Pick up text
        """
        text = text.replace(" ", "").replace("\n", "").replace(".", "")
        return text

    @allure.step("Go the the Terms of Use page")
    def get_terms_of_use_text(self):
        """
        Go the the Terms of Use page
        """
        self.swipe_down_screen(1000)
        self.terms_of_use_link.click()
        text = self.get_text(self.terms_of_use_page.text)
        return text

    @allure.step("Go the the Privacy page")
    def get_privacy_text(self):
        """
        Go the the Privacy page
        """
        self.swipe_down_screen(1000)
        self.privacy_policy_link.click()
        text = self.get_text(self.privacy_policy_page.text)
        return text

    @allure.step("Compare the expected and result contents")
    def compare_texts(self, text1, text2):
        """
        Randomly select 200 characters check if it is in the expected or not
        """
        count = 0
        for _ in range(3):
            index = int(RandomUtil.generate_numbers(1))
            if text2[index:300] in text1:
                count += 1
        if count == 3:
            return True
        else:
            return False






