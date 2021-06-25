from allure_commons.types import AttachmentType
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pytest
import allure

remote_url = "http://localhost:4444/wd/hub"  # This is the hub url
def get_data():
    return [
        ("standard_user", "secret_sauce"),
        ("locked_out_user", "secret_sauce"),
        ("problem_user", "secret_sauce"),
        ("performance_glitch_user", "secret_sauce")
    ]


def setup_function():
    global driver  # driver is defined globally so that it can be accessed by other functions
    # this is to open the url in remote node browser, in this case in different port
    driver = webdriver.remote(command_executor= remote_url,desired_capabilities = {"browserName": "chrome"})
    driver.get("https://www.saucedemo.com/")
    driver.implicitly_wait(5)
    driver.maximize_window()


def teardown_function():
    driver.quit()


@pytest.mark.parametrize("username, password", get_data())
def test_login(username, password):
    username_box = driver.find_element(By.ID, "user-name")
    username_box.clear()
    username_box.send_keys(username)
    password_box = driver.find_element(By.ID, "password")
    password_box.clear()
    password_box.send_keys(password)
    # below line will add the screenshot in the allure report
    allure.attach(driver.get_screenshot_as_png(), name="dologin", attachment_type=AttachmentType.PNG)
    password_box.submit()
    actual_title = "Swag Labs"
    expected_title = driver.title
    assert actual_title == expected_title, "Title matches with expected title"

# To run all the tests parallel we need to execute below command in terminal
# "pytest <filename> -n 4(number of repetition)"
# To generate html report we need to execute below command in the argument
# "pytest <filename> --html=htmlreport.html"
# To generate allure JSON below command is required
# "pytest <filename> --alluredir= "./allure_reports/"
# To generate the actual html report execute below command in terminal
# "allure serve ./allure_reports/"
