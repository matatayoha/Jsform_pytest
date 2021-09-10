from sys import platform

import pytest
from selenium import webdriver
import os
import allure
from libs.utils.misc import Misc


# init driver
@pytest.fixture(scope='class', autouse=False)
def init():
    print('init driver: ------------------')

    config = Misc.load_config()
    # defined some run time variables
    config["accepted_cookie"] = False
    driver = Misc.create_driver(config)

    yield driver, config
    print('Finish test case')
    driver.quit()


@pytest.fixture(scope='function', autouse=False)
def init_method():
    print('init driver: ------------------')

    config = Misc.load_config()
    # defined some run time variables
    config["accepted_cookie"] = False
    driver = Misc.create_driver(config)

    yield driver, config
    print('Finish test case')
    driver.quit()

@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    """
    Hook function to get the status of each use case
    :param item:
    :param call:
    :return:
    """
    # Get the call result of hook method
    outcome = yield
    print('Use case execution results', outcome)

    # Get test report from call result of hook method
    report = outcome.get_result()

    # It is a failure to get only the call execution result of the use case, excluding setup / teardown
    if report.when == "call" and report.failed:
        output_path = Misc.get_file_absolute_path(
            "output",
            "results",
        )
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        failed_path = Misc.get_file_absolute_path(
            "failures",
            "results",
            "output",

        )

        mode = "a" if os.path.exists(failed_path) else "w"

        with open(failed_path, mode) as f:
            # let's also access a fixture for the fun of it
            if "tmpdir" in item.fixturenames:
                extra = " (%s)" % item.funcargs["tmpdir"]
            else:
                extra = ""
            f.write(report.nodeid + extra + "\n")

        # Add a screenshot of allure Report
        if "init_method" in item.funcargs:
            current_driver = item.funcargs['init_method'][0]
        else:
            current_driver = item.funcargs['init'][0]
        if hasattr(current_driver, "get_screenshot_as_png"):
            with allure.step('Add failed screenshot...'):
                try:
                    allure.attach(current_driver.get_screenshot_as_png(), "Failed Screenshot",
                                  allure.attachment_type.PNG)
                except Exception as err:
                    print(err)
                    allure.attach("current_driver.get_screenshot_as_png()" + str(err), "Failed Screenshot",
                                  allure.attachment_type.TEXT)
