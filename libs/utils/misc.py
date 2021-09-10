
import os
import configparser
import json
from sys import platform
from selenium import webdriver


class Misc:

    @staticmethod
    def load_config():
        config = configparser.ConfigParser()
        config.read(os.path.join(Misc.get_root_directory(), "config", "config.cfg"), encoding="utf-8")
        # url
        url = config.get("platform", "portal")
        api_host = config.get("platform", "api")
        info_dict = {"api_host": api_host, "url": url}
        test_accounts = Misc.load_json_file(Misc.get_file_absolute_path("test_account.json", "resources", "test_data"))
        info_dict["user_email"] = test_accounts["users"]["common_user"]["user_email"]
        info_dict["user_name"] = test_accounts["users"]["common_user"]["user_name"]
        info_dict["password"] = test_accounts["users"]["common_user"]["password"]
        return {**info_dict, **test_accounts}

    @staticmethod
    def load_json_file(file_name):
        with open(file_name, encoding="utf-8") as f:
            content = f.read()
            return json.loads(content)

    @staticmethod
    def load_tou(file_name):
        with open(Misc.get_file_absolute_path(file_name, "resources", "test_data"), "r", encoding="utf-8") as f:
            contents = f.readlines()
            content_list = list()
            for content in contents:
                content = content.strip().replace(" ", "").replace("⚫", "").replace("◼", "").replace(".", "")
                if len(content) > 0:
                    content_list.append(content)
        return content_list

    @staticmethod
    def get_root_directory():
        root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(root_path, "..")

    @staticmethod
    def get_file_absolute_path(file, *paths):
        return os.path.join(Misc.get_root_directory(), *paths, file)

    @staticmethod
    def create_driver(config):

        if platform.startswith("win"):
            chromedriver_name = "chromedriver.exe"
            max_size_window = '--start-maximized'
        elif platform.startswith("darwin"):
            chromedriver_name = "chromedriver_macos"
            max_size_window = '--start-kiosk'
        else:
            chromedriver_name = "chromedriver_linux"
            max_size_window = '--start-maximized'

        options = webdriver.ChromeOptions()
        # options.add_argument('--headless')
        # options.add_argument('--disable-gpu')
        # options.add_argument('–no-sandbox')
        options.add_argument(max_size_window)

        driver = webdriver.Chrome(executable_path=Misc.get_file_absolute_path(
            chromedriver_name,
            "resources", "driver"
        ), options=options)
        # driver = webdriver.Chrome(options=options, executable_path="/usr/bin/chromedriver")
        return driver
