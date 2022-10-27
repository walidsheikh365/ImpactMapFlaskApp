import multiprocessing
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome, ChromeOptions
from time import sleep


@pytest.fixture(scope='class')
def chrome_driver(request):
    """ Selenium webdriver with options to support running in GitHub actions
    Note:
        For CI: `headless` and `disable-gpu` not commented out
        For running on your computer: `headless` and `disable-gpu` to be commented out
    """
    options = ChromeOptions()
    #options.add_argument("--headless")  # use for GitHub Actions CI
    #options.add_argument('--disable-gpu') # use for GitHub Actions CI
    options.add_argument("--window-size=1920,1080")
    chrome_driver = Chrome(options=options)
    request.cls.driver = chrome_driver
    yield
    chrome_driver.close()


"""
@pytest.mark.usefixtures('chrome_driver')
class TestAppBrowser:

    Class containing Selenium tests.
    This does not need to be a python class, it is written this way to give you an example of a test class.

    def test_app_is_running(self):

        Check the app is running

        sleep(5)
        self.driver.get('http://127.0.0.1:5000/')
        assert self.driver.title == 'Home page'

    def test_signup_is_successful(self):

        Test that a user can create an account using the signup form if all fields are filled out correctly,
        and that they are redirected to the index page.

        # Go to the home page
        self.driver.get('http://127.0.0.1:5000/')

        # Click signup menu link
        self.driver.implicitly_wait(5)
        self.driver.find_element(By.ID, "navbarDropdownMenu").click()
        self.driver.find_element(By.ID, "nav-signup").click()

        # Test person data
        first_name = "Driver"
        last_name = "Test"
        email = "email@ucl.ac.uk"
        password = "1"
        password_repeat = "1"

        # Fill in registration form
        self.driver.find_element(By.ID, "first_name").send_keys(first_name)
        self.driver.find_element(By.ID, "last_name").send_keys(last_name)
        self.driver.find_element(By.ID, "email").send_keys(email)
        self.driver.find_element(By.ID, "password").send_keys(password)
        self.driver.find_element(By.ID, "password_repeat").send_keys(password_repeat)
        self.driver.find_element(By.ID, "btn-signup").click()

        # Assert that browser redirects to index page
        self.driver.implicitly_wait(10)
        assert self.driver.current_url == 'http://127.0.0.1:5000/'

        # Assert success message is flashed on the index page
        message = self.driver.find_element(By.ID, "flash-messages").text
        assert f"Hello, {first_name}." in message

    def test_logout_is_successful(self):
        self.driver.implicitly_wait(5)
        self.driver.find_element(By.ID, "navbarDropdownMenu").click()
        self.driver.find_element(By.ID, "nav-logout").click()
        message = self.driver.find_element(By.ID, "flash-messages").text
        assert "See you next time!" in message

    def test_login_is_successful(self):
        self.driver.implicitly_wait(5)
        self.driver.find_element(By.ID, "navbarDropdownMenu").click()
        self.driver.find_element(By.ID, "nav-login").click()

        email = "email@ucl.ac.uk"
        password = "1"

        self.driver.find_element(By.ID, "email").send_keys(email)
        self.driver.find_element(By.ID, "password").send_keys(password)
        self.driver.find_element(By.ID, "btn-login").click()

        message = self.driver.find_element(By.ID, "flash-messages").text
        assert "Login successful." in message

    def test_account_deletion_is_successful(self):
        self.driver.implicitly_wait(5)
        self.driver.find_element(By.ID, "navbarDropdownMenu").click()
        self.driver.find_element(By.ID, "nav-delete-account").click()

        self.driver.implicitly_wait(5)
        self.driver.find_element(By.ID, "btn-delete-account").click()

        message = self.driver.find_element(By.ID, "flash-messages").text
        assert "Account has been successfully deleted." in message


def document_initialised(driver):
    return driver.execute_script("return initialised")

"""
