
import allure
from appium.webdriver.common.touch_action import TouchAction
from poium.common import logging
from poium.common.exceptions import FindElementTypesError
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from poium import Page, Element, Browser
import time
from libs.utils.misc import Misc
from libs.utils.xf_ocr import extract_verification_code


class BasePage(Page):

    captcha_path = Misc.get_file_absolute_path("verification_code.png", "resources", "test_data")

    # shared object， can be used cross pages
    accept_btn = Element(css=r'div.btn button', describe="accept use of cookie button")
    verification_notice_popup = Element(css=r'div.ivu-message-notice', describe="invalid verification code notice")
    current_language = Element(css=r'div.ivu-dropdown-rel span', describe="current page display language")
    chinese = Element(css=r'ul.ivu-dropdown-menu li', describe="language list", index=0)
    english = Element(css=r'ul.ivu-dropdown-menu li', describe="language list", index=1)

    def __init__(self, driver, config):
        self.contents = Misc.load_json_file(Misc.get_file_absolute_path("content.json", "resources", "test_data"))
        self.config = config
        super().__init__(driver, self.config["url"])

    @classmethod
    def find_web_element(cls, element: Element):
        """
        Judge element positioning way, and returns the element.
        """
        by = element.k
        value = element.v

        # selenium
        if by == "id_":
            elem = Browser.driver.find_elements_by_id(value)[element.index]
        elif by == "name":
            elem = Browser.driver.find_elements_by_name(value)[element.index]
        elif by == "class_name":
            elem = Browser.driver.find_elements_by_class_name(value)[element.index]
        elif by == "tag":
            elem = Browser.driver.find_elements_by_tag_name(value)[element.index]
        elif by == "link_text":
            elem = Browser.driver.find_elements_by_link_text(value)[element.index]
        elif by == "partial_link_text":
            elem = Browser.driver.find_elements_by_partial_link_text(value)[element.index]
        elif by == "xpath":
            elem = Browser.driver.find_elements_by_xpath(value)[element.index]
        elif by == "css":
            elem = Browser.driver.find_elements_by_css_selector(value)[element.index]
        else:
            raise FindElementTypesError(
                "Please enter the correct targeting elements")

        return elem

    @classmethod
    def wait_for_element_visible(cls, element, time_out=30, poll_frequency=0.5, ignored_exceptions=None):
        start_time = time.time()
        while time.time() - start_time <= time_out:
            try:
                if element.is_displayed():
                    return True
                else:
                    time.sleep(poll_frequency)
            except:
                time.sleep(poll_frequency)
        if not ignored_exceptions:
            raise TimeoutError("element " + str(element) + " not visible in " + str(time_out) + "s")
        else:
            return False


    @classmethod
    def wait_for_element_invisible(cls, element, time_out=30, poll_frequency=0.5,
                                   ignored_exceptions=None):
        start_time = time.time()
        while time.time() - start_time <= time_out:
            try:
                if element.is_displayed():
                    time.sleep(poll_frequency)
                else:
                    return True
            except:
                return True
        if not ignored_exceptions:
            raise TimeoutError("element " + str(element) + " still visible in " + str(time_out) + "s")
        else:
            return False

    @classmethod
    def is_element_visible(cls, element):
        try:
            display = cls.find_web_element(element).is_displayed()

            logging.info("check element display: " + element.desc + " : " + str(display))
            return display
        except Exception as err:
            logging.info("check element display: " + element.desc + " is not in the dom ")
            return False

    @classmethod
    def element_screenshots(cls, element, path):
        """
        choose a element to take a screenshot, and save to the path
        """
        time.sleep(1)
        screenshot_scope = element._Element__get_element(element.k, element.v)
        screenshot_scope.screenshot(path)

    @allure.step("accept the use of cookie：")
    def accept_use_of_cookie(self):
        if not self.config["accepted_cookie"]:
            if self.is_element_visible(self.accept_btn):
                self.accept_btn.click()
                self.config["accepted_cookie"] = True

    @allure.step("change the page display language：")
    def change_language(self, is_english=True):
        """
        change the page display language
        """
        if self.is_element_visible(self.current_language):
            if is_english:
                if self.current_language.text != r'English':
                    self.current_language.click()
                    self.english.click()
            else:
                if self.current_language.text != r'中文':
                    self.current_language.click()
                    self.chinese.click()

    @allure.step("screenshot for the captcha and save to local path：")
    def save_captcha(self):
        """
        verification_picture
        """
        time.sleep(1)
        self.element_screenshots(self.captcha, self.captcha_path)

    @allure.step("input captcha")
    def submit_captcha(self):
        self.save_captcha()
        for _ in range(20):
            verification_code = extract_verification_code(self.captcha_path)
            # verification_code = '0000'
            if not verification_code:
                self.captcha.click()
                self.save_captcha()
            else:
                self.captcha_input.clear()
                self.captcha_input.input(verification_code)
                time.sleep(1)
                self.swipe_down_screen(800)
                self.submit_btn.click()
                if self.check_captcha():
                    return True
                else:
                    self.save_captcha()
        else:
            raise TimeoutError("Try to input verification code 20 times, but still failed")

    def check_captcha(self):
        """
        check the verification code is valid or not
        """
        time.sleep(2)
        for _ in range(5):
            if not self.is_element_visible(self.submit_btn):
                return True
            else:
                if not self.is_element_visible(self.verification_notice_popup):
                    time.sleep(1)
                else:
                    if self.contents["common"]["captcha_invalid"] in self.verification_notice_popup.text:
                        return False
                    else:
                        return True
        else:
            return False

    def swipe_down_screen(self, base_size=1):
        element = "document.documentElement.childNodes[1].childNodes[0].childNodes[0].scrollTop={}"
        self.swipe_page_screen(element, base_size)

    def swipe_page_screen(self, element, base_size=1):
        """
        swipe the screen, the bigger the base_size, the deeper the browser swiped down
        """
        time.sleep(1)
        for i in range(1, 11):
            js = element.format(i * 100 * base_size)
            self.driver.execute_script(js)
            time.sleep(0.1)
        time.sleep(1)
